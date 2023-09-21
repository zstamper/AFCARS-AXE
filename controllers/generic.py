from typing import Any

from PySide6.QtWidgets import QDialog
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from model.models import MyBaseModel


class GenericController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.

     :param dialog a QDialog instance of the dialog to operate upon
     :param data_class a class reference used for manipulating model data
     """

    def __init__(self, dialog: QDialog, data_class: Any):
        self.data_class: MyBaseModel = data_class
        self.dialog = dialog
        self.dialog.on_accept = self.do_accept
        self.new_data = None

    def add(self) -> Any:
        """Shows an empty dialog, lets the user do what they will, then returns either a new model instance or None,
        depending on whether the form contents are "valid" or not. The "valid" determination is handled by the model
        as a feature of pydantic."""
        self.dialog.clear()
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            return self.new_data
        return None

    def edit(self, data: MyBaseModel) -> None:
        """Pushes the model data into the form, shows the form, and lets the user do what they will. If the form
        contents are valid, the model instance is modified with the new form contents. Otherwise, the model contents are
        left unchanged. Like the add() method, "valid" is determined by rules in the model using pydantic."""
        self.dialog.clear()
        data.scatter(self.dialog)
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            data.gather(self.dialog)

    def do_accept(self) -> bool:
        try:
            self.new_data = self.data_class.crib(self.dialog)
            return True
        except ValidationError as ve:
            show_error_dialog(ve)
        return False
