from typing import List
from AnyQt import QtWidgets

from ewoksorange.bindings import OWEwoksWidgetNoThread
from ewoksorange.bindings import ow_build_opts
from ewoksfluo.gui.data_viewer import DataViewer

from ewoksfluo.tasks.pick_scans import PickScansInFiles
from orangecontrib.ewoksfluo.pick_scans_widget import PickScansWidget

from ewokscore import missing_data


__all__ = ["OWPickScans"]


class OWPickScans(
    OWEwoksWidgetNoThread, **ow_build_opts, ewokstaskclass=PickScansInFiles
):
    name = "Pick scans"
    description = "Pick scans"

    def __init__(self):
        super().__init__()
        self.tabs: List[PickScansWidget] = []
        self._init_control_area()
        self._init_main_area()

    @property
    def n_tabs(self) -> int:
        return len(self.tabs)

    @property
    def plus_index(self) -> int:
        return self.n_tabs

    @property
    def minus_index(self) -> int:
        return self.n_tabs + 1

    def handle_special_tabs(self, i) -> None:
        """
        Handles clicks on special tabs (+ or -)
        """
        if i == self.plus_index:
            self.add_new_picking_tab()
            return

        if i == self.minus_index:
            self.remove_last_picking_tab()
            return

    def add_new_picking_tab(self, initial_values: dict = {}) -> None:
        # Insert the new tab before the + index
        new_tab_index = self.plus_index
        page_widget = PickScansWidget(
            lambda inputs: self.update_tab_inputs(inputs, new_tab_index),
            initial_values,
        )
        self.tabWidget.insertTab(new_tab_index, page_widget, f"File {new_tab_index+1}")
        self.tabs.insert(new_tab_index, page_widget)

        self.tabWidget.setCurrentIndex(new_tab_index)

    def remove_last_picking_tab(self) -> None:
        last_tab_index = self.plus_index - 1
        self.tabWidget.setCurrentIndex(last_tab_index)
        if last_tab_index == 0:
            return
        self.tabWidget.removeTab(last_tab_index)
        w = self.tabs.pop()
        filename = w.form.get_parameter_value("bliss_filename")
        if filename:
            self._viewer.closeFile(filename)
        del w
        self.update_inputs()

    def _init_main_area(self):
        super()._init_main_area()
        layout = self._get_main_layout()

        self._viewer = DataViewer(parent=self.mainArea)
        self._viewer.setVisible(True)
        layout.addWidget(self._viewer)
        layout.setStretchFactor(self._viewer, 1)

        self._refresh_files()

    def _init_control_area(self) -> None:
        super()._init_control_area()
        self.tabWidget = QtWidgets.QTabWidget(parent=self.controlArea)
        self.tabWidget.addTab(QtWidgets.QWidget(), "+")
        self.tabWidget.addTab(QtWidgets.QWidget(), "-")
        self.tabWidget.tabBar().setSelectionBehaviorOnRemove(
            QtWidgets.QTabBar.SelectionBehavior.SelectLeftTab
        )
        self.tabWidget.currentChanged.connect(lambda i: self.handle_special_tabs(i))

        self._get_control_layout().addWidget(self.tabWidget)

        initial_values = self.get_default_input_values(include_missing=False)

        if not initial_values:
            self.add_new_picking_tab()
        else:
            for filename, scan_range, exclude_scans in zip(
                initial_values["bliss_filenames"],
                initial_values["scan_ranges"],
                initial_values["exclude_scans"],
            ):
                scan_min, scan_max = scan_range if scan_range else (None, None)
                self.add_new_picking_tab(
                    {
                        "bliss_filename": filename,
                        "scan_min": scan_min,
                        "scan_max": scan_max,
                        "exclude_scans": exclude_scans,
                    }
                )

    def handleNewSignals(self) -> None:
        self._update_input_data()
        super().handleNewSignals()

    def _update_input_data(self) -> None:
        dynamic = self.get_dynamic_input_names()
        for name in self.get_input_names():
            self._default_inputs_form.set_parameter_enabled(name, name not in dynamic)

    def update_inputs(self):
        for i, tab in enumerate(self.tabs):
            self.update_tab_inputs(tab.form.get_parameter_values(), i)

    def update_tab_inputs(self, form_values: dict, index: int) -> None:
        values = self.get_default_input_values(include_missing=True)

        # Make values index match the tabs index
        for name in self.get_input_names():
            if not values.get(name, None):
                values[name] = []
            if len(values[name]) < len(self.tabs):
                values[name].extend(
                    [missing_data.MISSING_DATA] * (len(self.tabs) - len(values[name]))
                )
            if len(values[name]) > len(self.tabs):
                values[name] = values[name][: len(self.tabs)]

        # Update only if the new value is valid (i.e. not missing)
        if form_values["bliss_filename"]:
            values["bliss_filenames"][index] = form_values["bliss_filename"]
        if form_values["scan_min"] and form_values["scan_max"]:
            values["scan_ranges"][index] = (
                form_values["scan_min"],
                form_values["scan_max"],
            )
        if form_values["exclude_scans"]:
            values["exclude_scans"][index] = form_values["exclude_scans"]

        self.update_default_inputs(**values)
        self._refresh_files()

    def _refresh_files(self):
        filenames = self.get_task_input_value("bliss_filenames", [])

        for filename in filenames:
            if not filename:
                continue
            self._viewer.updateFile(filename)

    def _execute_ewoks_task(self, *args, **kw) -> None:
        self._viewer.closeAll()
        super()._execute_ewoks_task(*args, **kw)

    def closeEvent(self, event):
        self._viewer.closeEvent(event)
