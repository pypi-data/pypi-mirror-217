import json
import warnings
import logging
from typing import Optional, Mapping, Sequence

from pydm.widgets import PyDMEmbeddedDisplay
import haven

from firefly import display

# from .voltmeter import VoltmeterDisplay


log = logging.getLogger(__name__)


class VoltmetersDisplay(display.FireflyDisplay):
    _ion_chamber_displays = []

    def __init__(
        self,
        args: Optional[Sequence] = None,
        macros: Mapping = {},
        **kwargs,
    ):
        self.ion_chambers = list(haven.registry.findall(label="ion_chambers"))
        macros_ = macros.copy()
        if "SCALER" not in macros_.keys():
            macros_["SCALER"] = self.ion_chambers[0].scaler_prefix
        super().__init__(args=args, macros=macros_, **kwargs)

    def customize_ui(self):
        # Delete existing voltmeter widgets
        for idx in reversed(range(self.voltmeters_layout.count())):
            self.voltmeters_layout.takeAt(idx).widget().deleteLater()
        # Add embedded displays for all the ion chambers
        try:
            ion_chambers = self.ion_chambers
        except haven.exceptions.ComponentNotFound as e:
            warnings.warn(str(e))
            log.warning(e)
            ion_chambers = []
        scaler_prefix = "CPT NOT FOUND"
        self._ion_chamber_displays = []
        for ic in sorted(ion_chambers, key=lambda c: c.ch_num):
            # Create the display object
            disp = PyDMEmbeddedDisplay(parent=self)
            disp.macros = json.dumps({"IC": ic.name})
            disp.filename = "voltmeter.py"
            # Add the Embedded Display to the Results Layout
            self.voltmeters_layout.addWidget(disp)
            self._ion_chamber_displays.append(disp)

    def ui_filename(self):
        return "voltmeters.ui"
