from typing import Any, Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.removal1993_validator import Removal1993Validator
from dialogs.removal1993_dialog import Removal1993Dialog
from model import Removal1993
from model.models import FileType, Child, ChildName


class Removal1993Controller:

    def __init__(self, parent, child_name: ChildName, data: Removal1993, /, file_type: FileType = FileType.PRODUCTION):
        self.dialog = Removal1993Dialog(parent)
        self.file_type = file_type
        self.child_name = child_name
        self._data = None
        self.data = data
        self.validator = Removal1993Validator(self.dialog)
        self.on_save: Optional[Callable] = None
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.dialog.on_validate = self.do_validate

    @property
    def child(self) -> Child:
        return self.dialog.child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v

    @property
    def data(self) -> Removal1993:
        return self._data

    @data.setter
    def data(self, v: Removal1993):
        self._data = v
        self._data.scatter(self.dialog)

    @property
    def file_type(self) -> FileType:
        return self.dialog.file_type

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        self.dialog.file_type = v

    def exec(self):
        self.dialog.child_name = self.child_name
        self.dialog.exec()

    def do_save(self) -> None:
        # gather model fields from the view
        # bubble the save operation up the call stack until the record is saved in the database
        if self.serialize():
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
