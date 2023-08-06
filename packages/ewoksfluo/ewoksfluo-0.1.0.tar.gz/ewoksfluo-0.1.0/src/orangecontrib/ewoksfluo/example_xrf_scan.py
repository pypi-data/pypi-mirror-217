import json

from ewoksorange.bindings import OWEwoksWidgetNoThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksfluo.tasks.example_data import ExampleXRFScan
from ewoksfluo.gui.data_viewer import DataViewer


__all__ = ["OWExampleXRFScan"]


class OWExampleXRFScan(
    OWEwoksWidgetNoThread, **ow_build_opts, ewokstaskclass=ExampleXRFScan
):
    name = "Example XRF scan"
    description = "Example XRF data for a loopscan"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        parameters = {
            "output_filename": {
                "label": "HDF5 filename",
                "value_for_type": "",
                "select": "file",
            },
            "nscans": {
                "label": "Number of scans",
                "value_for_type": 1,
            },
            "emission_line_groups": {
                "label": "Line groups",
                "value_for_type": "",
                "serialize": json.dumps,
                "deserialize": json.loads,
            },
            "rois": {
                "label": "Regions of interest",
                "value_for_type": "",
                "serialize": json.dumps,
                "deserialize": json.loads,
            },
            "energy": {
                "label": "Energy (keV)",
                "value_for_type": 0.0,
            },
            "npoints": {
                "label": "Number of scan points",
                "value_for_type": 0,
            },
            "ndetectors": {
                "label": "Number of detectors",
                "value_for_type": 0,
            },
            "expo_time": {
                "label": "Exposure time (sec)",
                "value_for_type": 0.0,
            },
            "flux": {
                "label": "Flux (1/sec)",
                "value_for_type": 0.0,
            },
            "counting_noise": {
                "label": "Counting Noise",
                "value_for_type": False,
            },
            "integral_type": {
                "label": "Data as integers",
                "value_for_type": False,
            },
        }

        for name, kw in parameters.items():
            self._default_inputs_form.addParameter(
                name,
                value=values[name],
                value_change_callback=self._default_inputs_changed,
                **kw,
            )

    def _default_inputs_changed(self):
        self.update_default_inputs(**self._default_inputs_form.get_parameter_values())
        self._update_input_data()
        self._refresh_output_file()

    def handleNewSignals(self) -> None:
        self._update_input_data()
        super().handleNewSignals()

    def _execute_ewoks_task(self, *args, **kw) -> None:
        self._close_output_file()
        super()._execute_ewoks_task(*args, **kw)

    def task_output_changed(self):
        self._update_output_data()

    def _init_main_area(self):
        super()._init_main_area()
        layout = self._get_main_layout()

        self._viewer = DataViewer(parent=self.mainArea)
        self._viewer.setVisible(True)
        layout.addWidget(self._viewer)
        layout.setStretchFactor(self._viewer, 1)

        self._update_output_data()

    def _update_input_data(self):
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

    def _update_output_data(self):
        self._refresh_output_file()

    def _refresh_output_file(self):
        filename = self.get_task_input_value("output_filename")
        if filename:
            self._viewer.updateFile(filename)

    def _close_output_file(self):
        filename = self.get_task_input_value("output_filename")
        if filename:
            self._viewer.closeFile(filename)

    def closeEvent(self, event):
        self._viewer.closeEvent(event)
