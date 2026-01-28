# Copyright 2024 by ICF International, Inc.
#
# This file is part of AXE, the AFCARS XML Editor.
#
# AXE is free software: you can redistribute it and/or modify it under the terms
# of the GNU Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# AXE is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# AXE. If not, see <https://www.gnu.org/licenses/>.

from typing import Callable, Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidgetItem, QWidget

from dialogs import BaseDialog
from model import BaseChild
from model.models import ReportType, ReportingPeriod


class ChildDialog(BaseDialog):

    def __init__(self, parent: QWidget = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = self.load_ui('ui_child_dialog.ui')
        self._wire_ui()
        # self.ui.setModal(True)
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

        self._e1: str = ""
        self._agency_name: str = ""
        self._file_type: str = ""
        self._report_type: ReportType = ReportType.OOH
        self._reporting_period: str = ""
        self._reporting_periods: list[ReportingPeriod] = []
        self._child_data: list[BaseChild] = []

        self.on_add: Optional[Callable] = None
        self.on_edit: Optional[Callable] = None
        self.on_delete: Optional[Callable] = None
        self.on_refresh_data: Optional[Callable] = None
        self._child_table_sorted_once = False

    def _wire_ui(self):
        self.ui.add_child.clicked.connect(self._on_add_clicked)
        self.ui.edit_child.clicked.connect(self._on_edit_clicked)
        self.ui.child_table.doubleClicked.connect(self._on_edit_clicked)
        self.ui.delete_child.clicked.connect(self._on_delete_clicked)
        self.ui.reporting_period_filter.currentIndexChanged.connect(self._refresh_data)
        self.ui.filter_a.clicked.connect(self._refresh_data)
        self.ui.filter_all.clicked.connect(self._refresh_data)
        self.ui.filter_ooh.clicked.connect(self._refresh_data)
        self.ui.close_button.clicked.connect(self.close)
        self.ui.child_table.setSortingEnabled(True)

    def _on_add_clicked(self, *args, **kwargs):
        if self.on_add:
            self.on_add(*args, **kwargs)

    def _on_edit_clicked(self, *args, **kwargs):
        if self.on_edit:
            self.on_edit(*args, **kwargs)

    def _on_delete_clicked(self, *args, **kwargs):
        if self.on_delete:
            self.on_delete(*args, **kwargs)

    def _refresh_data(self):
        if self.on_refresh_data:
            self.on_refresh_data()

    @property
    def e1(self) -> str:
        return self._e1

    @e1.setter
    def e1(self, v: str) -> None:
        self._e1 = v
        self._update_window_title()

    @property
    def agency_name(self) -> str:
        return self._agency_name

    @agency_name.setter
    def agency_name(self, v: str) -> None:
        self._agency_name = v
        self._update_window_title()

    @property
    def reporting_period(self) -> str:
        return self._reporting_period

    @reporting_period.setter
    def reporting_period(self, v: str) -> None:
        self._reporting_period = v
        self._update_window_title()

    @property
    def reporting_period_choices(self) -> list[ReportingPeriod]:
        return self._reporting_periods

    @reporting_period_choices.setter
    def reporting_period_choices(self, v: list[ReportingPeriod]):
        self._reporting_periods = v
        self.ui.reporting_period_filter.clear()
        self.ui.reporting_period_filter.addItem("Any")
        self.ui.reporting_period_filter.addItems(v)

    @property
    def reporting_period_filter(self) -> ReportingPeriod:
        return self.ui.reporting_period_filter.currentText()

    @property
    def report_type(self) -> ReportType:
        return self._report_type

    @report_type.setter
    def report_type(self, v: ReportType) -> None:
        self._report_type = v
        self._update_window_title()
        if v == ReportType.OOH:
            self.ui.child_table.horizontalHeaderItem(5).setText("Last Removal")
            self.ui.child_table.horizontalHeaderItem(6).setText("Last Exit")
        if v == ReportType.A:
            self.ui.child_table.horizontalHeaderItem(5).setText("Last Finalization")
            self.ui.child_table.horizontalHeaderItem(6).setText("Last Termination")

    @property
    def report_type_filter(self) -> ReportType | None:
        if self.ui.filter_all.isChecked():
            return None
        if self.ui.filter_a.isChecked():
            return ReportType.A
        if self.ui.filter_ooh.isChecked():
            return ReportType.OOH

    @property
    def file_type(self) -> str:
        return self._file_type

    @file_type.setter
    def file_type(self, v: str) -> None:
        self._file_type = v
        self._update_window_title()

    def _update_window_title(self):
        title = f"{self.agency_name} ({self.e1}) / {self.reporting_period} / {self.report_type.value}"
        self.setWindowTitle(title)

    @property
    def child_data(self) -> list[BaseChild]:
        return self._child_data

    @child_data.setter
    def child_data(self, v: list[BaseChild]) -> None:
        self._child_data = v
        self.refresh_child_data()

    @property
    def current_child(self) -> BaseChild:
        current_row = self.ui.child_table.currentRow()
        item = self.ui.child_table.item(current_row, 0)
        if item is not None:
            return item.data(Qt.UserRole)

    def refresh_child_data(self):
        header = self.ui.child_table.horizontalHeader()
        sort_column = header.sortIndicatorSection()
        sort_order = header.sortIndicatorOrder()
        self.ui.child_table.setSortingEnabled(False)
        self.ui.child_table.clearContents()
        for _ in range(self.ui.child_table.rowCount()):
            self.ui.child_table.removeRow(0)
        row = 0
        for row, data in enumerate(self.child_data):
            self.ui.child_table.insertRow(row)
            item = QTableWidgetItem(str(data.e4 if data.e4 else ""))
            item.setData(Qt.UserRole, data)
            self.ui.child_table.setItem(row, 0, item)
            self.ui.child_table.setItem(row, 1, QTableWidgetItem(str(data.last_name if data.last_name else "")))
            self.ui.child_table.setItem(row, 2, QTableWidgetItem(str(data.first_name if data.first_name else "")))
            self.ui.child_table.setItem(row, 3, QTableWidgetItem(data.e5.strftime("%m/%d/%Y") if data.e5 else ""))
            self.ui.child_table.setItem(row, 4, QTableWidgetItem(
                data.date_created.strftime("%m/%d/%Y") if data.date_created else ""))
            if self.report_type == ReportType.OOH:
                self.ui.child_table.setItem(row, 5, QTableWidgetItem(
                    data.last_removal.strftime("%m/%d/%Y") if data.last_removal else ""))
                self.ui.child_table.setItem(row, 6,
                                            QTableWidgetItem(
                                                data.last_exit.strftime("%m/%d/%Y") if data.last_exit else ""))
            else:
                self.ui.child_table.setItem(row, 5, QTableWidgetItem(
                    data.last_adoption.strftime("%m/%d/%Y") if data.last_adoption else ""))
                self.ui.child_table.setItem(row, 6,
                                            QTableWidgetItem(
                                                data.last_termination.strftime(
                                                    "%m/%d/%Y") if data.last_termination else ""))
            if self.report_type == ReportType.OOH:
                timestamp = data.last_updated_ooh
            else:
                timestamp = data.last_updated_a
            self.ui.child_table.setItem(row, 7, QTableWidgetItem(timestamp.strftime("%m/%d/%Y %H:%M") if timestamp else ""))
        self.ui.child_table.setSortingEnabled(True)
        if not self._child_table_sorted_once:
            header.setSortIndicator(1, Qt.AscendingOrder)
            self.ui.child_table.sortItems(1, Qt.AscendingOrder)
            self._child_table_sorted_once = True
        else:
            header.setSortIndicator(sort_column, sort_order)
        self.ui.child_table.setColumnWidth(0, 120)
        self.ui.child_table.setColumnWidth(2, 105)
        self.ui.child_table.setColumnWidth(3, 80)
        self.ui.child_table.setColumnWidth(4, 80)
        self.ui.child_table.setColumnWidth(5, 120)
        self.ui.child_table.setColumnWidth(6, 120)
        self.ui.child_table.setColumnWidth(7, 120)