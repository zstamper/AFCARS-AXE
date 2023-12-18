from datetime import date

from dialogs.removal1993_dialog import Removal1993Dialog
from .abstract_validator import AbstractValidator


class Removal1993BaseValidator:

    def __init__(self, dialog: Removal1993Dialog):
        self.dialog = dialog

    @staticmethod
    def is_valid_date(d: int) -> bool:
        try:
            s = str(d)
            year = int(s[0:4])
            month = int(s[4:6])
            day = int(s[6:8])
            date(year=year, month=month, day=day)
            return True
        except ValueError:
            return False


class Removal1993Validators(Removal1993BaseValidator):

    def validate_e69(self):
        if not self.is_valid_date(self.dialog.e69):
            raise ValueError("Invalid date provided for Removal Date (E69).")

    def validate_e153(self):
        if self.dialog.e153 and not self.is_valid_date(self.dialog.e153):
            raise ValueError("Invalid date provided for Exit Date (E153).")

    def validate_e69_e153(self):
        if self.is_valid_date(self.dialog.e69) and self.is_valid_date(self.dialog.e153):
            if self.dialog.e69 >= self.dialog.e153:
                raise ValueError("Removal Date (E69) must be prior to Exit Date (E153).")

    def validate_e155(self):
        if self.dialog.e155 not in (1, 2, 3, 4, 5, 6, 8):
            raise ValueError("Invalid selection for Exit Reason (E155).")


class Removal1993Validator(AbstractValidator):
    def __init__(self, dialog: Removal1993Dialog):
        self.dialog = dialog
        self.validator = Removal1993Validators(self.dialog)
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

    def validate_tab(self, tab_num: int) -> bool:
        return False

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
