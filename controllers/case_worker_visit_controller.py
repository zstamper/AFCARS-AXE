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

import datetime
from typing import Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.case_worker_visit_validator import CaseWorkerVisitValidator
from dialogs.case_worker_visit_dialog import CaseVisitDialog
from model.models import CaseVisit, Removal2020, FileType, Child, ChildName


class CaseWorkerVisitController:

    def __init__(self, parent, child_name: ChildName, data: CaseVisit, /, file_type: FileType = FileType.PRODUCTION, removal_controller=None):
        self.removal_controller = removal_controller
        self._data = None
        self.on_save: Optional[Callable] = None
        self.dialog = CaseVisitDialog(parent)
        self.file_type = file_type
        self.dialog.child_name = child_name
        self.new_data: CaseVisit | None = None
        self.validator = CaseWorkerVisitValidator(self.dialog)
        self.parent_data: Optional[Removal2020] = None
        self.dialog.on_validate = self.do_validate
        self.dialog.on_save = self.do_save
        self.on_save_and_add: Optional[Callable] = None
        self.dialog.on_close = self.do_close
        self.data = data

    @property
    def child(self) -> Child:
        return self.dialog.child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v

    @property
    def parent_data(self):
        return self.validator.parent_data

    @parent_data.setter
    def parent_data(self, v):
        self.validator.parent_data = v

    @property
    def file_type(self) -> FileType:
        return self.dialog.file_type

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        self.dialog.file_type = v

    @property
    def data(self) -> CaseVisit:
        return self._data

    @data.setter
    def data(self, v: CaseVisit) -> None:
        self._data = v
        self._data.scatter(self.dialog)

    def exec(self):
        self.dialog.exec()

    def do_validate(self) -> bool:
        self.validator.parent_data = self.parent_data
        tab_ok = self.validator.validate()
        if not tab_ok:
            show_error_dialog(self.dialog, messages=self.validator.messages())
        return tab_ok

    def do_save(self) -> None:
        if self.serialize():
            self.data.last_updated = datetime.datetime.now()
            if self.on_save:
                self.on_save()

    def do_close(self) -> bool:
        if self.is_dirty():
            if self.confirm_save():
                self.do_save()
        return True

    @staticmethod
    def confirm_save() -> bool:
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Close)
        msgBox.setDefaultButton(QMessageBox.Save)
        return msgBox.exec() == QMessageBox.Save

    def is_dirty(self) -> bool:
        for key in vars(self.data).keys():
            if key == "last_updated":
                continue
            if hasattr(self.dialog, key):
                if getattr(self.dialog, key) != getattr(self.data, key):
                    return True
        return False

    def serialize(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate():
                    return False
            self.data.gather(self.dialog)
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def clear(self) -> None:
        self.dialog.clear()

    def do_validate_clicked(self) -> bool:
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages())
        return ok
