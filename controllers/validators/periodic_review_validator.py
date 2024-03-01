from datetime import date
from typing import Optional

from controllers.validators.abstract_validator import AbstractValidator
from dialogs.periodic_review_dialog import PeriodicReviewDialog
from model import Removal2020
from utils.e1 import is_valid_date, is_future_date


class PeriodicReviewBaseValidator:

    def __init__(self, dialog: PeriodicReviewDialog):
        self.dialog: PeriodicReviewDialog = dialog
        self.parent_data: Optional[Removal2020] = None


class PeriodicReviewValidators(PeriodicReviewBaseValidator):

    def validate_e149(self):
        if not is_valid_date(self.dialog.e149):
            raise ValueError("Invalid date for Periodic Review Date (E149).")
        if is_future_date(self.dialog.e149):
            raise ValueError("Periodic Review Date (E149) cannot be in the future.")
        if self.dialog.e149 < self.parent_data.e69:
            raise ValueError("Periodic Review Data (E149) cannot be before Removal Date (E69).")


class PeriodicReviewValidator(AbstractValidator):
    def __init__(self, dialog):
        self.dialog = dialog
        self.validator = PeriodicReviewValidators(self.dialog)
        self._messages: list[ValueError] = []

    @property
    def parent_data(self):
        return self.validator.parent_data

    @parent_data.setter
    def parent_data(self, v):
        self.validator.parent_data = v

    def validate_tab(self, tab: int) -> bool:
        return False

    def validate(self) -> bool:
        results = []
        self._messages = []
        for func in [func for func in dir(self.validator) if func.startswith('validate_')]:
            try:
                results.append(getattr(self.validator, func)() or True)
            except Exception as e:
                results.append(False)
                self._messages.append(e)
        return all(results)

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
