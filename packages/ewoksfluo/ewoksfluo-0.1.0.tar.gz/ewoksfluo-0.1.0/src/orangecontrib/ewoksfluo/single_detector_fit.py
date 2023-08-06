from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksfluo.tasks.single_detector_fit import SingleDetectorFit
from ewoksfluo.gui.data_viewer import DataViewer


__all__ = ["OWSingleDetectorFit"]


class OWSingleDetectorFit(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=SingleDetectorFit
):
    name = "Single-Detector Fit"
    description = "Fit 1 scan with multiple detectors"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        parameters = {
            "scan_uri": {
                "label": "Scan URI",
                "value_for_type": "",
            },
            "detector_name": {
                "label": "Detector name",
                "value_for_type": "",
            },
            "xrf_spectra_uri_template": {
                "label": "XRF spectra uri template",
                "value_for_type": "",
            },
            "config": {
                "label": "PyMca configuration URI",
                "value_for_type": "",
            },
            "quantification": {
                "label": "Quantification",
                "value_for_type": False,
            },
            "fast_fitting": {
                "label": "Fast Fitting",
                "value_for_type": False,
            },
            "energy_multiplier": {
                "label": "Energy multiplier",
                "value_for_type": 0.0,
            },
            "diagnostics": {
                "label": "Save Fit Diagnostics",
                "value_for_type": False,
            },
            "output_uri": {
                "label": "HDF5 output URI",
                "value_for_type": "",
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
        filename = self.get_task_input_value("output_uri")
        if filename:
            self._viewer.updateFile(filename.split("::")[0])

    def _close_output_file(self):
        filename = self.get_task_input_value("output_uri")
        if filename:
            self._viewer.closeFile(filename.split("::")[0])

    def closeEvent(self, event):
        self._viewer.closeEvent(event)
