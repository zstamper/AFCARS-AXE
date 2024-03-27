import re
from datetime import date

from dialogs.a_dialog import ADialog
from model.models import ReportType
from utils.e1 import is_valid_date, e2_end_date, afcars_to_date, is_future_date, is_way_past_date
from .abstract_validator import AbstractValidator
from .common_validators import CommonValidators


class ABaseValidator:
    def __init__(self, dialog: ADialog):
        self.dialog = dialog


class AValidators(ABaseValidator, CommonValidators):
    report_type = ReportType.A

    def validate_a15(self):
        if self.dialog.a15 not in [1, 2]:
            raise ValueError("Assistance Agreement Type (A15) is required.")

    def validate_a16(self):
        if self.dialog.a16 is None or self.dialog.a16 < 0 or self.dialog.a16 > 999999:
            raise ValueError("Adoption or Guardianship Subsidy Amount (A16) is out of range (0-999,999).")

    def validate_a17(self):
        if not self.dialog.ui.a17.text():
            raise ValueError("Adoption Finalization or Guardianship Legalization Date (A17) is missing.")
        if not re.match(r"\d+", self.dialog.ui.a17.text()):
            raise ValueError("Adoption Finalization or Guardianship Legalization Date (A17) is invalid.")
        if not is_valid_date(self.dialog.a17):
            raise ValueError("Adoption Finalization or Guardianship Legalization Date (A17) is invalid.")
        if is_future_date(self.dialog.a17):
            raise ValueError("Adoption Finalization or Guardianship Legalization Date (A17) can't be in the future.")
        if afcars_to_date(self.dialog.a17) > e2_end_date():
            raise ValueError(
                "Adoption Finalization or Guardianship Legalization Date (A17) can't be after reporting period end.")
        if is_way_past_date(self.dialog.a17):
            raise ValueError("Adoption Finalization or Guardianship Legalization Date (A17) is too far in the past.")

    def validate_a18(self):
        if not bool(self.dialog.ui.a18.text()):
            return
        if not re.match(r"\d+", self.dialog.ui.a18.text()):
            raise ValueError("Agreement Termination Date (A18) is not valid.")
        if not is_valid_date(self.dialog.a18):
            raise ValueError("Agreement Termination Date (A18) is not valid.")
        if self.dialog.a18 < self.dialog.a17:
            raise ValueError(
                "Agreement Termination Date (A18) can't be before Adoption Finalization or Guardianship Legalization Date (A17).")

    def validate_a19(self):
        if self.dialog.a19 not in [1, 2, 3]:
            raise ValueError("Adoption or Guardianship Placing Agency is required.")


class AValidator(AbstractValidator):

    def __init__(self, dialog: ADialog):
        self.dialog = dialog
        self.validator = AValidators(self.dialog)
        self._messages: list[ValueError] = []

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

    def validate_tab(self, tab_num: int) -> (bool, list):
        return False

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
