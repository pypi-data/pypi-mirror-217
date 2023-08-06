import json

from ewoksorange.bindings import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewoksorange.gui.parameterform import ParameterForm

from ewoksfluo.tasks.sum_fit_results import SumFitResults
from ewoksfluo.gui.data_viewer import DataViewer


__all__ = ["OWSumFitResults"]


class OWSumFitResults(
    OWEwoksWidgetOneThread, **ow_build_opts, ewokstaskclass=SumFitResults
):
    name = "Sum Fit Results"
    description = "Add fit results of multiple detectors"

    def __init__(self):
        super().__init__()
        self._init_control_area()
        self._init_main_area()

    def _init_control_area(self):
        super()._init_control_area()
        self._default_inputs_form = ParameterForm(parent=self.controlArea)
        values = self.get_default_input_values(include_missing=True)

        parameters = {
            "fit_results_uri_template": {
                "label": "URI template of fit results",
                "value_for_type": "",
            },
            "scan_uri": {
                "label": "URI scan",
                "value_for_type": "",
            },
            "livetime_uri_template": {
                "label": "URI template of livetime datasets",
                "value_for_type": "",
            },
            "detector_names": {
                "label": "List of detector names",
                "value_for_type": "",
                "serialize": json.dumps,
                "deserialize": json.loads,
            },
            "livetime_reference_value": {
                "label": "",
                "value_for_type": 0,
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
        uri = self.get_task_input_value("output_uri")
        if uri:
            self._viewer.updateFile(uri.split("::")[0])

    def _close_output_file(self):
        uri = self.get_task_input_value("output_uri")
        if uri:
            self._viewer.closeFile(uri.split("::")[0])

    def closeEvent(self, event):
        self._viewer.closeEvent(event)
