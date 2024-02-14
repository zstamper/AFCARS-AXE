from typing import Any, Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.periodic_review_validator import PeriodicReviewValidator
from dialogs.periodic_review_dialog import PeriodicReviewDialog
from model.models import PeriodicReview


class PeriodicReviewController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, child_name: str, data: PeriodicReview):
        self._data = None
        self.dialog = PeriodicReviewDialog(parent)
        self.validator = PeriodicReviewValidator(self.dialog)
        self.on_save: Optional[Callable] = None
        self.dialog.child_name = child_name
        self.dialog.on_validate = self.do_validate
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.data = data

    @property
    def data(self) -> PeriodicReview:
        return self._data

    @data.setter
    def data(self, v: PeriodicReview) -> None:
        self._data = v
        self._data.scatter(self.dialog)

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
        ok = self.validator.validate()
        if not ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)
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

    def is_dirty(self) -> bool:
        for key in vars(self.data).keys():
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
