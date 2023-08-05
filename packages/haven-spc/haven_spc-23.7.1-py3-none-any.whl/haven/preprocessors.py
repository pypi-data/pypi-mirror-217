"""Tools for modifying plans and data streams as they are generated."""


from typing import Union, Sequence, Iterable
from collections import ChainMap
import pkg_resources
import os
import socket
import getpass
import warnings
import logging

from bluesky.preprocessors import (
    baseline_wrapper as bluesky_baseline_wrapper,
    finalize_wrapper,
    suspend_wrapper,
)
from bluesky.suspenders import SuspendBoolLow
from bluesky.utils import make_decorator, Msg
from bluesky.preprocessors import msg_mutator
import epics


from .instrument.instrument_registry import registry
from .exceptions import ComponentNotFound
from ._iconfig import load_config


log = logging.getLogger()


def baseline_wrapper(
    plan,
    devices: Union[Sequence, str] = [
        "motors",
        "power_supplies",
        "xray_sources",
        "APS",
        "baseline",
    ],
    name: str = "baseline",
):
    bluesky_baseline_wrapper.__doc__
    # Resolve devices
    devices = registry.findall(devices, allow_none=True)
    yield from bluesky_baseline_wrapper(plan=plan, devices=devices, name=name)


def get_version(pkg_name):
    return pkg_resources.get_distribution(pkg_name).version


VERSIONS = dict(
    apstools=get_version("apstools"),
    bluesky=get_version("bluesky"),
    databroker=get_version("databroker"),
    epics_ca=epics.__version__,
    epics=epics.__version__,
    haven=get_version("haven-spc"),
    h5py=get_version("h5py"),
    matplotlib=get_version("matplotlib"),
    numpy=get_version("numpy"),
    ophyd=get_version("ophyd"),
    pymongo=get_version("pymongo"),
)


def inject_haven_md_wrapper(plan):
    """Inject additional metadata into a run.

    This takes precedences over the original metadata dict in the event of
    overlapping keys, but it does not mutate the original metadata dict.
    (It uses ChainMap.)

    Parameters
    ----------
    plan : iterable or iterator
        a generator, list, or similar containing `Msg` objects

    """

    def _inject_md(msg):
        if msg.command != "open_run":
            return msg
        # Prepare the metadata dictionary
        config = load_config()
        md = {
            # Software versions
            "versions": VERSIONS,
            # Controls
            "EPICS_HOST_ARCH": os.environ.get("EPICS_HOST_ARCH"),
            "epics_libca": os.environ.get("PYEPICS_LIBCA"),
            "EPICS_CA_MAX_ARRAY_BYTES": os.environ.get("EPICS_CA_MAX_ARRAY_BYTES"),
            # Facility
            "beamline_id": config["beamline"]["name"],
            "facility_id": config["facility"]["name"],
            "xray_source": config["facility"]["xray_source"],
            # Computer
            "login_id": f"{getpass.getuser()}@{socket.gethostname()}",
            "pid": os.getpid(),
            # User supplied
            "sample_name": "",
            # Bluesky
            "parameters": "",
            "purpose": "",
        }
        # Get metadata from the beamline scheduling system (bss)
        try:
            bss = registry.find(name="bss")
        except ComponentNotFound:
            if config["beamline"]["is_connected"]:
                wmsg = "Could not find bss device, metadata may be missing."
                warnings.warn(wmsg)
                log.warning(wmsg)
            bss_md = None
        else:
            bss_md = bss.get()
            from pprint import pprint

            pprint(bss_md._asdict())
            # pprint({k: v for k, v in bss_md})
            md.update(
                {
                    "proposal_id": bss_md.proposal.proposal_id,
                    "proposal_title": bss_md.proposal.title,
                    "proposal_users": bss_md.proposal.user_last_names,
                    "proposal_user_badges": bss_md.proposal.user_badges,
                    "esaf_id": bss_md.esaf.esaf_id,
                    "esaf_title": bss_md.esaf.title,
                    "esaf_users": bss_md.esaf.user_last_names,
                    "esaf_user_badges": bss_md.esaf.user_badges,
                    "mail_in_flag": bss_md.proposal.mail_in_flag,
                    "proprietary_flag": bss_md.proposal.proprietary_flag,
                    "bss_aps_cycle": bss_md.esaf.aps_cycle,
                    "bss_beamline_name": bss_md.proposal.beamline_name,
                }
            )
        # Update the message
        msg = msg._replace(kwargs=ChainMap(msg.kwargs, md))
        return msg

    return (yield from msg_mutator(plan, _inject_md))


def shutter_suspend_wrapper(plan, shutter_signals=None):
    """
    Install suspenders to the RunEngine, and remove them at the end.

    Parameters
    ----------
    plan : iterable or iterator
        a generator, list, or similar containing `Msg` objects
    suspenders : suspender or list of suspenders
        Suspenders to use for the duration of the wrapper

    Yields
    ------
    msg : Msg
        messages from plan, with 'install_suspender' and 'remove_suspender'
        messages inserted and appended
    """
    if shutter_signals is None:
        shutters = registry.findall("shutters", allow_none=True)
        shutter_signals = [s.pss_state for s in shutters]
    # Create a suspender for each shutter
    suspenders = []
    for sig in shutter_signals:
        suspender = SuspendBoolLow(sig, sleep=3.0)
        suspenders.append(suspender)
    if not isinstance(suspenders, Iterable):
        suspenders = [suspenders]

    def _install():
        for susp in suspenders:
            yield Msg("install_suspender", None, susp)

    def _remove():
        for susp in suspenders:
            yield Msg("remove_suspender", None, susp)

    def _inner_plan():
        yield from _install()
        return (yield from plan)

    return (yield from finalize_wrapper(_inner_plan(), _remove()))


baseline_decorator = make_decorator(baseline_wrapper)
shutter_suspend_decorator = make_decorator(shutter_suspend_wrapper)
