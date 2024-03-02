from datetime import date
from typing import Optional

from controllers.validators.abstract_validator import AbstractValidator
from dialogs.permanency_hearing_dialog import PermanencyHearingDialog
from model import Removal2020
from utils.e1 import e2_end_date, afcars_to_date, is_valid_date, is_future_date


class PermanencyHearingBaseValidator:

    def __init__(self, dialog: PermanencyHearingDialog):
        self.dialog: PermanencyHearingDialog = dialog
        self.parent_data: Optional[Removal2020] = None


class PermanencyHearingValidators(PermanencyHearingBaseValidator):

    def validate_e150(self):
        if not is_valid_date(self.dialog.e150):
            raise ValueError("Permanency Hearing Date (E150) is invalid.")
        if is_future_date(self.dialog.e150):
            raise ValueError("Permanency Hearing Date (E150) may not be in the future.")
        if self.dialog.e150 < self.parent_data.e69:
            raise ValueError("Permanency Hearing Date (E150) may not be before Removal Date (E69).")
        if afcars_to_date(self.dialog.e150) > e2_end_date():
            raise ValueError("Permanency Hearing Date (E150) must be before end of current reporting period (E2).")


class PermanencyHearingValidator(AbstractValidator):
    def __init__(self, dialog):
        self.dialog = dialog
        self.validator = PermanencyHearingValidators(self.dialog)
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

    def messages(self) -> list:
        return [exc.args[0] for exc in self._messages]
