from typing import Optional, Callable

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

    def __init__(self, parent: BaseDialog):
        self.dialog = ADialog(parent=parent)
        self.validator = AValidator(self.dialog)
        self.new_data: Child | None = None
        self._base_child: BaseChild | None = None
        self._child: Child | None = None
        self.on_accept: Optional[Callable] = None

        # Wire our callbacks into the dialog
        self.dialog.on_accept = self.do_accept
        self.dialog.on_validate_clicked = self.do_validate_clicked

    def do_accept(self) -> bool:
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
            if self.on_accept:
                self.on_accept()
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def do_validate_clicked(self):
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)

    def show(self):
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
