from enum import IntEnum
from apstools.devices import CamMixin_V34, SingleTrigger_V34
from ophyd import (
    ADComponent as ADCpt,
    DetectorBase as OphydDetectorBase,
    SimDetectorCam,
    Lambda750kCam,
    EigerDetectorCam,
    SingleTrigger,
    Kind,
)
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.plugins import (
    HDF5Plugin_V34,
    HDF5Plugin_V31,
    ImagePlugin_V34,
    ImagePlugin_V31,
    PvaPlugin_V34,
    PvaPlugin_V31,
    TIFFPlugin_V34,
    TIFFPlugin_V31,
    ROIPlugin_V34,
    ROIPlugin_V31,
    StatsPlugin_V31 as OphydStatsPlugin_V31,
    StatsPlugin_V34 as OphydStatsPlugin_V34,
    OverlayPlugin,
)


from .._iconfig import load_config
from .instrument_registry import registry
from .. import exceptions


__all__ = ["Eiger500K", "Lambda250K", "SimDetector"]


class SimDetectorCam_V34(CamMixin_V34, SimDetectorCam):
    ...


class WriteModes(IntEnum):
    SINGLE = 0
    CAPTURE = 1
    STREAM = 2


class Capture(IntEnum):
    STOP = 0
    START = 1


class StageCapture:
    """Mixin to prepare NDPlugin file capture mode.

    Sets the number of captures to zero (infinite), and starts
    capturing. Then when the device gets unstaged, capturing turns
    back off.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Stage the capture button as well
        self.stage_sigs[self.file_write_mode] = WriteModes.STREAM
        self.stage_sigs[self.capture] = Capture.START
        self.stage_sigs[self.num_capture] = 0


class MyHDF5Plugin(FileStoreHDF5IterativeWrite, HDF5Plugin_V34):
    """
    Add data acquisition methods to HDF5Plugin.
    * ``stage()`` - prepare device PVs befor data acquisition
    * ``unstage()`` - restore device PVs after data acquisition
    * ``generate_datum()`` - coordinate image storage metadata
    """

    def stage(self):
        self.stage_sigs.move_to_end("capture", last=True)
        super().stage()


class DetectorBase(OphydDetectorBase):
    def __init__(self, *args, description=None, **kwargs):
        super().__init__(*args, **kwargs)
        if description is None:
            description = self.name
        self.description = description

    overlays = ADCpt(OverlayPlugin, "Over1:")


class StatsMixin:
    _default_read_attrs = [
        "max_value",
        "min_value",
        "min_xy.x",
        "max_xy.x",
        "min_xy.y",
        "max_xy.y",
        "total",
        "net",
        "mean_value",
        "sigma_value",
    ]


class StatsPlugin_V31(StatsMixin, OphydStatsPlugin_V31):
    ...


class StatsPlugin_V34(StatsMixin, OphydStatsPlugin_V34):
    ...


class SimDetector(SingleTrigger_V34, DetectorBase):
    """
    ADSimDetector
    SingleTrigger:
    * stop any current acquisition
    * sets image_mode to 'Multiple'
    """

    cam = ADCpt(SimDetectorCam_V34, "cam1:")
    image = ADCpt(ImagePlugin_V34, "image1:")
    pva = ADCpt(PvaPlugin_V34, "Pva1:")
    hdf1 = ADCpt(
        type("HDF5Plugin", (StageCapture, HDF5Plugin_V34), {}),
        "HDF1:",
        # write_path_template="/tmp/",
        # read_path_template=READ_PATH_TEMPLATE,
    )
    roi1 = ADCpt(ROIPlugin_V34, "ROI1:", kind=Kind.config)
    roi2 = ADCpt(ROIPlugin_V34, "ROI2:", kind=Kind.config)
    roi3 = ADCpt(ROIPlugin_V34, "ROI3:", kind=Kind.config)
    roi4 = ADCpt(ROIPlugin_V34, "ROI4:", kind=Kind.config)
    stats1 = ADCpt(StatsPlugin_V34, "Stats1:", kind=Kind.normal)
    stats2 = ADCpt(StatsPlugin_V34, "Stats2:", kind=Kind.normal)
    stats3 = ADCpt(StatsPlugin_V34, "Stats3:", kind=Kind.normal)
    stats4 = ADCpt(StatsPlugin_V34, "Stats4:", kind=Kind.normal)
    stats5 = ADCpt(StatsPlugin_V34, "Stats5:", kind=Kind.normal)


class TIFFPlugin(StageCapture, TIFFPlugin_V31):
    _default_read_attrs = ["full_file_name"]


class HDF5Plugin(StageCapture, HDF5Plugin_V31):
    _default_read_attrs = ["full_file_name"]


class Lambda250K(SingleTrigger, DetectorBase):
    """
    A Lambda 250K area detector device.
    """

    cam = ADCpt(Lambda750kCam, "cam1:")
    image = ADCpt(ImagePlugin_V31, "image1:")
    pva = ADCpt(PvaPlugin_V31, "Pva1:")
    tiff = ADCpt(TIFFPlugin, "TIFF1:", kind=Kind.normal)
    hdf1 = ADCpt(HDF5Plugin, "HDF1:", kind=Kind.normal)
    roi1 = ADCpt(ROIPlugin_V31, "ROI1:", kind=Kind.config)
    roi2 = ADCpt(ROIPlugin_V31, "ROI2:", kind=Kind.config)
    roi3 = ADCpt(ROIPlugin_V31, "ROI3:", kind=Kind.config)
    roi4 = ADCpt(ROIPlugin_V31, "ROI4:", kind=Kind.config)
    stats1 = ADCpt(StatsPlugin_V31, "Stats1:", kind=Kind.normal)
    stats2 = ADCpt(StatsPlugin_V31, "Stats2:", kind=Kind.normal)
    stats3 = ADCpt(StatsPlugin_V31, "Stats3:", kind=Kind.normal)
    stats4 = ADCpt(StatsPlugin_V31, "Stats4:", kind=Kind.normal)
    stats5 = ADCpt(StatsPlugin_V31, "Stats5:", kind=Kind.normal)

    _default_read_attrs = [
        "stats1",
        "stats2",
        "stats3",
        "stats4",
        "stats5",
        "hdf1",
        "tiff",
    ]


class Eiger500K(SingleTrigger, DetectorBase):
    """
    A Eiger S 500K area detector device.
    """

    cam = ADCpt(EigerDetectorCam, "cam1:")
    image = ADCpt(ImagePlugin_V34, "image1:")
    pva = ADCpt(PvaPlugin_V34, "Pva1:")
    tiff = ADCpt(TIFFPlugin, "TIFF1:", kind=Kind.normal)
    hdf1 = ADCpt(HDF5Plugin, "HDF1:", kind=Kind.normal)
    roi1 = ADCpt(ROIPlugin_V34, "ROI1:", kind=Kind.config)
    roi2 = ADCpt(ROIPlugin_V34, "ROI2:", kind=Kind.config)
    roi3 = ADCpt(ROIPlugin_V34, "ROI3:", kind=Kind.config)
    roi4 = ADCpt(ROIPlugin_V34, "ROI4:", kind=Kind.config)
    stats1 = ADCpt(StatsPlugin_V34, "Stats1:", kind=Kind.normal)
    stats2 = ADCpt(StatsPlugin_V34, "Stats2:", kind=Kind.normal)
    stats3 = ADCpt(StatsPlugin_V34, "Stats3:", kind=Kind.normal)
    stats4 = ADCpt(StatsPlugin_V34, "Stats4:", kind=Kind.normal)
    stats5 = ADCpt(StatsPlugin_V34, "Stats5:", kind=Kind.normal)

    _default_read_attrs = [
        "stats1",
        "stats2",
        "stats3",
        "stats4",
        "stats5",
        "hdf1",
        "tiff",
    ]


def load_area_detectors(config=None):
    if config is None:
        config = load_config()
    # Create the area detectors defined in the configuration
    for name, adconfig in config.get("area_detector", {}).items():
        DeviceClass = globals().get(adconfig["device_class"])
        # Check that it's a valid device class
        if DeviceClass is None:
            msg = f"area_detector.{name}.device_class={adconfig['device_class']}"
            raise exceptions.UnknownDeviceConfiguration(msg)
        # Create the device
        det = DeviceClass(
            prefix=f"{adconfig['prefix']}:",
            name=name,
            labels={"area_detectors"},
        )
        registry.register(det)
