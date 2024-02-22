from typing import Any, Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.permanency_hearing_validator import PermanencyHearingValidator
from dialogs.permanency_hearing_dialog import PermanencyHearingDialog
from model.models import MyBaseModel, PermanencyHearing, Removal2020, FileType


class PermanencyHearingController:

    def __init__(self, parent, child_name: str, data: PermanencyHearing,/,file_type:FileType=FileType.PRODUCTION):
        self._data = None
        self.on_save: Optional[Callable] = None
        self.dialog = PermanencyHearingDialog(parent)
        self.file_type = file_type
        self.validator = PermanencyHearingValidator(self.dialog)
        self.parent_data: Optional[Removal2020] = None
        self.dialog.child_name = child_name
        self.dialog.on_validate = self.do_validate
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.data = data

    @property
    def data(self) -> PermanencyHearing:
        return self._data

    @data.setter
    def data(self, v: PermanencyHearing) -> None:
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

    def do_validate(self) -> bool:
        self.validator.parent_data = self.parent_data
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages())
        return ok

    def do_save(self) -> None:
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
            self.data.gather(self.dialog)
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False
