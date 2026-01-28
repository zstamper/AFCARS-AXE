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

from PySide6.QtWidgets import QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.periodic_review_validator import PeriodicReviewValidator
from dialogs.periodic_review_dialog import PeriodicReviewDialog
from model.models import PeriodicReview, Removal2020, FileType, Child, ChildName


class PeriodicReviewController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, child_name: ChildName, data: PeriodicReview, /,
                 file_type: FileType = FileType.PRODUCTION):
        self._data = None
        self.dialog = PeriodicReviewDialog(parent)
        self.file_type = file_type
        self.validator = PeriodicReviewValidator(self.dialog)
        self.parent_data: Optional[Removal2020] = None
        self.on_save: Optional[Callable] = None
        self.dialog.child_name = child_name
        self.dialog.on_validate = self.do_validate
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.data = data

    @property
    def child(self) -> Child:
        return self.dialog.child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v

    @property
    def data(self) -> PeriodicReview:
        return self._data

    @data.setter
    def data(self, v: PeriodicReview) -> None:
        self._data = v
        self._data.scatter(self.dialog)

    @property
    def file_type(self) -> FileType:
        return self.dialog.file_type

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        self.dialog.file_type = v

    def exec(self):
        self.dialog.exec()

    def serialize(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate():
                    return False
            self._data.gather(self.dialog)
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def do_validate(self) -> bool:
        self.validator.parent_data = self.parent_data
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)
        return ok

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

    def is_dirty(self) -> bool:
        for key in vars(self.data).keys():
            if key == "last_updated":
                continue
            if hasattr(self.dialog, key):
                if getattr(self.dialog, key) != getattr(self.data, key):
                    return True
        return False

    @staticmethod
    def confirm_save() -> bool:
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Close)
        msgBox.setDefaultButton(QMessageBox.Save)
        return msgBox.exec() == QMessageBox.Save

    @property
    def data(self) -> PeriodicReview:
        return self._data

    @data.setter
    def data(self, v: PeriodicReview):
        self._data = v
        self._data.scatter(self.dialog)
