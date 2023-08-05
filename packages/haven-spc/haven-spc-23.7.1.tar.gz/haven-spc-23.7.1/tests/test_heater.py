import time

from epics import caget, caput
from haven.instrument.heater import CapillaryHeater, load_heaters


def test_capillary_device(ioc_ptc10):
    # Set up the device and ensure connections match the IOC we have
    device = CapillaryHeater(ioc_ptc10.prefix, name="capillary_heater")
    device.wait_for_connection()
    # Check for status objects checking temperature properly
    status = device.set(200)
    assert not status.done
    caput(ioc_ptc10.pvs["tc1_temperature"], 200)
    new_temp = device.readback.get(use_monitor=False)
    assert new_temp == 200


def test_load_heaters(ioc_ptc10):
    heaters = load_heaters()
    assert len(heaters) == 1
    heater = heaters[0]
    print(heater)
    heaters[0].wait_for_connection()
    assert heaters[0].name == "capillary_heater"
