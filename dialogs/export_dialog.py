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

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QTableWidgetItem

from dialogs import BaseDialog
from model import Child, BaseChild
from model.models import ReportType


class ExportDialog(BaseDialog):
    def __init__(self, parent: QDialog = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = self.load_ui('ui_export_dialog.ui')
        self._wire_ui()
        self._report_type: Optional[ReportType] = None
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self._child_data: list[tuple[BaseChild, Child]] = []

    def _wire_ui(self):
        self.setModal(True)
        self.setWindowTitle('NCWDMS XML Export')
        ui = self.ui

        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)
        ui.select_button.clicked.connect(self.select_button_clicked)
        ui.child_table.itemChanged.connect(self.refresh_select_button_label)

    def select_button_clicked(self) -> None:
        checked = not any(
            [self.ui.child_table.item(row, 0).checkState() == Qt.Checked for row in
             range(self.ui.child_table.rowCount())])
        for row in range(self.ui.child_table.rowCount()):
            self.ui.child_table.item(row, 0).setCheckState(Qt.Checked if checked else Qt.Unchecked)
        self.refresh_select_button_label()

    def refresh_select_button_label(self) -> None:
        if any(
                [self.ui.child_table.item(row, 0).checkState() == Qt.Checked for row in
                 range(self.ui.child_table.rowCount())]):
            self.ui.select_button.setText("Clear Selections")
        else:
            self.ui.select_button.setText("Select All")

    @property
    def report_type(self) -> ReportType:
        return self._report_type

    @report_type.setter
    def report_type(self, v: ReportType) -> None:
        self._report_type = v
        self._set_headers()

    def _set_headers(self):
        if self.report_type == ReportType.OOH:
            self.ui.child_table.horizontalHeaderItem(4).setText("Last Removal")
            self.ui.child_table.horizontalHeaderItem(5).setText("Last Exit")
        elif self.report_type == ReportType.A:
            self.ui.child_table.horizontalHeaderItem(4).setText("Last Adoption")
            self.ui.child_table.horizontalHeaderItem(5).setText("Last Termination")

    @property
    def child_data(self) -> list[tuple[BaseChild, Child]]:
        return self._child_data

    @child_data.setter
    def child_data(self, v: list[tuple[str, Child]]) -> None:
        self._child_data = v
        self.refresh_child_data()

    def refresh_child_data(self):
        self.ui.child_table.clearContents()

        while self.ui.child_table.rowCount() > 0:
            self.ui.child_table.removeRow(0)
        for row, child in enumerate(self.child_data):
            self.ui.child_table.insertRow(row)
            item = QTableWidgetItem(child[0].e4)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.ui.child_table.setItem(row, 0, item)
            self.ui.child_table.setItem(row, 1, QTableWidgetItem(child[0].last_name))
            self.ui.child_table.setItem(row, 2, QTableWidgetItem(child[0].first_name))
            self.ui.child_table.setItem(row, 3, QTableWidgetItem(
                child[0].date_created.strftime("%m/%d/%Y") if child[0].date_created else ""))
            if self.report_type == ReportType.OOH:
                self.ui.child_table.setItem(row, 4, QTableWidgetItem(
                    child[0].last_removal.strftime("%m/%d/%Y") if child[0].last_removal else ""))
                self.ui.child_table.setItem(row, 5, QTableWidgetItem(
                    child[0].last_exit.strftime("%m/%d/%Y") if child[0].last_exit else ""))
            elif self.report_type == ReportType.A:
                self.ui.child_table.setItem(row, 4, QTableWidgetItem(
                    child[0].last_adoption.strftime("%m/%d/%Y") if child[0].last_adoption else ""))
                self.ui.child_table.setItem(row, 5, QTableWidgetItem(
                    child[0].last_termination.strftime("%m/%d/%Y") if child[0].last_termination else ""))
        self.refresh_select_button_label()

    @property
    def selected_children(self) -> list[tuple[BaseChild, Child]]:
        selections: list[(BaseChild, Child)] = []
        for row in range(self.ui.child_table.rowCount()):
            if self.ui.child_table.item(row, 0).checkState() == Qt.Checked:
                selections.append(self._child_data[row])
        return selections
