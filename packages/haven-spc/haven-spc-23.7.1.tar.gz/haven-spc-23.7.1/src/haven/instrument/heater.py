from ophyd import PVPositioner, EpicsSignalRO, EpicsSignalWithRBV, Component as Cpt
from apstools.devices import (
    PTC10PositionerMixin,
    PTC10AioChannel as PTC10AioChannelBase,
    PTC10TcChannel,
)

from .._iconfig import load_config
from .instrument_registry import registry


# The apstools version uses "voltage_RBV" as the PVname
class PTC10AioChannel(PTC10AioChannelBase):
    """
    SRS PTC10 AIO module
    """

    voltage = Cpt(EpicsSignalRO, "output_RBV", kind="config")


@registry.register
class CapillaryHeater(PTC10PositionerMixin, PVPositioner):
    readback = Cpt(EpicsSignalRO, "2A:temperature", kind="hinted")
    setpoint = Cpt(EpicsSignalWithRBV, "5A:setPoint", kind="hinted")

    # Additional modules installed on the PTC10
    pid = Cpt(PTC10AioChannel, "5A:")
    tc = Cpt(PTC10TcChannel, "2A:")


def load_heaters(config=None):
    if config is None:
        config = load_config()
    # Load the heaters
    heaters = []
    for name, cfg in config["heater"].items():
        Cls = globals().get(cfg["device_class"])
        device = Cls(prefix=f"{cfg['prefix']}:", name=name)
        heaters.append(device)
    return heaters
