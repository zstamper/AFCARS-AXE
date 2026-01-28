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

from typing import Optional, Callable
from datetime import datetime

from PySide6.QtWidgets import QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.second_parent_validator import SecondParentValidator
from dialogs.second_parent_dialog import Parent2Dialog
from model.models import SecondParent, Child


class SecondParentController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.

     The data instance variable holds a reference to the original data element. We must be careful to not reassign it
     to a new instance of the data class, else people will be scratching their heads wondering why their edits aren't
     being saved.
     """

    def __init__(self, parent, child_name: str, data: SecondParent):
        self._data = None
        self._child_name = None
        self.dialog = Parent2Dialog(parent)
        self.child_name = child_name
        self.data = data
        self.validator = SecondParentValidator(self.dialog)
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.dialog.on_validate = self.do_validate
        self.on_save: Optional[Callable] = None

    def exec(self):
        self.data.scatter(self.dialog)
        self.dialog.exec()

    @property
    def child(self) -> Child:
        return self.dialog.child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self._child_name = v
        self.dialog.child_name = v

    @property
    def data(self) -> SecondParent:
        return self._data

    @data.setter
    def data(self, v: SecondParent) -> None:
        self._data = v
        v.scatter(self.dialog)

    @property
    def e60(self) -> int:
        return self.dialog.e60

    @e60.setter
    def e60(self, v: int) -> None:
        self.dialog.e60 = v

    def do_save(self) -> None:
        # gather model fields from the view
        # bubble the save operation up the call stack until the record is saved in the database
        if self.serialize():
            self.data.last_updated = datetime.now()
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
            if key == "last_updated":  # ✅ Ignore timestamp
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

    def do_validate(self) -> bool:
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)
        return ok
