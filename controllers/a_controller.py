from typing import Optional, Callable

from PySide6.QtWidgets import QMessageBox
from pydantic import ValidationError

from dialogs import BaseDialog
from dialogs.a_dialog import ADialog
from model.models import Child, BaseChild
from .utilities import show_error_dialog
from .validators.a_validator import AValidator


class AController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, e1: str = ""):
        self.dialog = ADialog(parent=parent)
        self.validator = AValidator(self.dialog)
        self._base_child: BaseChild | None = None
        self._child: Child | None = None
        self.on_save: Optional[Callable] = None
        self.dialog.on_validate = self.do_validate
        self.dialog.on_close = self.do_close
        self.dialog.child_name = self.child_name
        self.dialog.on_save = self.do_save
        self.e1 = e1

        # Wire our callbacks into the dialog
        # self.dialog.on_save = self.do_save

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

    def do_save(self) -> bool:
        try:
            for key in vars(self.base_child).keys():
                if key != 'id':
                    if hasattr(self.dialog, key):
                        setattr(self.base_child, key, getattr(self.dialog, key))
            for key in vars(self.child).keys():
                if hasattr(self.dialog, key):
                    setattr(self.child, key, getattr(self.dialog, key))
            for key in vars(self.child.a).keys():
                if hasattr(self.dialog, key):
                    setattr(self.child.a, key, getattr(self.dialog, key))
            if self.on_save:
                self.on_save()
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def do_validate(self):
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)

    def exec(self):
        self.dialog.exec()

    def clear(self):
        self.dialog.clear()

    @property
    def child_name(self) -> str:
        return self.dialog.child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self.dialog.child_name = v

    @property
    def base_child(self) -> BaseChild:
        return self._base_child

    @base_child.setter
    def base_child(self, v: BaseChild) -> None:
        self._base_child = v
        self.dialog.e4 = v.e4
        self.dialog.first_name = v.first_name
        self.dialog.last_name = v.last_name

    @property
    def child(self) -> Child:
        return self._child

    @child.setter
    def child(self, v: Child) -> None:
        self._child = v
        for key in vars(v).keys():
            if hasattr(self.dialog, key):
                setattr(self.dialog, key, getattr(v, key))
        if v.a:
            for key in vars(v.a).keys():
                if hasattr(self.dialog, key):
                    setattr(self.dialog, key, getattr(v.a, key))
