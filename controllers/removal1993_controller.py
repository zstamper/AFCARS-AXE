from typing import Any

from PySide6.QtWidgets import QDialog
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.removal1993_validator import Removal1993Validator
from dialogs.removal1993_dialog import Removal1993Dialog
from model import Removal1993


class Removal1993Controller:

    def __init__(self, parent, child_name: str):
        self.dialog = Removal1993Dialog(parent)
        self.child_name = child_name
        self.dialog.on_accept = self.do_accept
        self.new_data = None
        self.validator = Removal1993Validator(self.dialog)
        self.dialog.on_validate_clicked = self.do_validate_clicked

    def add(self) -> Any:
        """Shows an empty dialog, lets the user do what they will, then returns either a new model instance or None,
        depending on whether the form contents are "valid" or not. The "valid" determination is handled by the model
        as a feature of pydantic."""
        self.dialog.clear()
        self.dialog.child_name = self.child_name

        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            return self.new_data
        return None

    def edit(self, data: Removal1993) -> None:
        """Pushes the model data into the form, shows the form, and lets the user do what they will. If the form
        contents are valid, the model instance is modified with the new form contents. Otherwise, the model contents are
        left unchanged. Like the add() method, "valid" is determined by rules in the model using pydantic."""
        data.scatter(self.dialog)
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            data.gather(self.dialog)
        else:
            # put the data back in to the dialog so that further queries of the form don't get confused by the form
            # state not matching the data state
            data.scatter(self.dialog)

    def do_accept(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate_clicked():
                    return False
            self.new_data = Removal1993.crib(self.dialog)
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def do_validate_clicked(self) -> bool:
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)
        return ok
