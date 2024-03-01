import datetime
from typing import Any, Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.living_arrangement_validator import LivingArrangementValidator
from dialogs.living_arrangement_dialog import LivingArrangementDialog
from model.models import MyBaseModel, LivingArrangement, Removal2020, FileType, Child


class LivingArrangementController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, child_name: str, data: LivingArrangement, /, file_type: FileType = FileType.PRODUCTION):
        self.dialog: LivingArrangementDialog = LivingArrangementDialog(parent)
        self.file_type: FileType = file_type
        self.parent_data: Optional[Removal2020] = None
        self._data = None
        self.data = data
        self.dialog.child_name = child_name
        self.validator = LivingArrangementValidator(self.dialog)
        self.dialog.on_validate = self.do_validate
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.on_save: Optional[Callable] = None

    @property
    def child(self) -> Child:
        return self.dialog.child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v

    @property
    def data(self) -> LivingArrangement:
        return self._data

    @data.setter
    def data(self, v: LivingArrangement) -> None:
        self._data = v
        self._data.scatter(self.dialog)

    @property
    def file_type(self) -> FileType:
        return self.dialog.file_type

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        self.dialog.file_type = v

    @property
    def e56(self)->int:
        return self.dialog.e56

    @e56.setter
    def e56(self, v: int):
        self.dialog.e56 = v

    @property
    def e57(self) -> int:
        return self.dialog.e57

    @e57.setter
    def e57(self, v: int):
        self.dialog.e57 = v

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
