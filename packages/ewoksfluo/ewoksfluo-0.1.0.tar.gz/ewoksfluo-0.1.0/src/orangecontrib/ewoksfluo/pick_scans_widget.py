from typing import Callable, List
from AnyQt import QtWidgets
from ewoksorange.gui.parameterform import ParameterForm


def scan_numbers_serializer(value: List[int]) -> str:
    return ",".join([str(n) for n in value])


def scan_numbers_deserializer(value: str) -> List[int]:
    return [int(n) for n in value.split(",")]


class PickScansWidget(QtWidgets.QWidget):
    def __init__(self, default_inputs_change_callback: Callable, initial_values=None):
        super().__init__()

        if initial_values is None:
            initial_values = {}

        self.form = ParameterForm(parent=self)
        self.default_inputs_change_callback = default_inputs_change_callback

        parameters = {
            "bliss_filename": {
                "label": "HDF5 filename",
                "value_for_type": "",
                "select": "file",
            },
            "scan_min": {
                "label": "Minimum scan to include",
                "value_for_type": 1,
            },
            "scan_max": {
                "label": "Maximum scan to include",
                "value_for_type": 1,
            },
            "exclude_scans": {
                "label": "List of scans to exclude",
                "value_for_type": "",
                "serialize": scan_numbers_serializer,
                "deserialize": scan_numbers_deserializer,
            },
        }

        for name, kw in parameters.items():
            self.form.addParameter(
                name,
                value=initial_values.get(name, None),
                value_change_callback=self._default_inputs_changed,
                **kw,
            )

    def _default_inputs_changed(self):
        self.default_inputs_change_callback(self.form.get_parameter_values())
