from typing import Any, Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.second_parent_validator import SecondParentValidator
from dialogs.second_parent_dialog import Parent2Dialog
from model.models import MyBaseModel, SecondParent


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
        self.dialog.on_validate_clicked = self.do_validate
        self.on_save: Optional[Callable] = None

    def exec(self):
        self.data.scatter(self.dialog)
        self.dialog.exec()

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
