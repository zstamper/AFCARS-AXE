from datetime import date

from dialogs.removal1993_dialog import Removal1993Dialog
from .abstract_validator import AbstractValidator


class Removal1993BaseValidator:

    def __init__(self, dialog: Removal1993Dialog):
        self.dialog = dialog
        self.parent_data = None

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

    @staticmethod
    def is_future_date(d: int) -> bool:
        if d is None:
            return False
        year = d // 10000
        month = (d - (d // 10000) * 10000) // 100
        day = d - (d // 100) * 100
        d = date(year=year, month=month, day=day)
        return d > date.today()

    @staticmethod
    def is_after_1993_date(d: int) -> bool:
        year = d // 10000
        month = (d - (d // 10000) * 10000) // 100
        day = d - (d // 100) * 100
        d = date(year=year, month=month, day=day)
        return d >= date(year=2022, month=10, day=1)


class Removal1993Validators(Removal1993BaseValidator):

    def validate_e69(self):
        try:
            e69 = self.dialog.e69
        except ValueError:
            raise ValueError("Removal Date (E69) is invalid format.")
        if self.dialog.e69 is None:
            raise ValueError("Removal Date (E69) is required.")
        if not self.is_valid_date(self.dialog.e69):
            raise ValueError("Invalid date provided for Removal Date (E69).")
        if self.is_future_date(self.dialog.e69):
            raise ValueError("Removal Date (E69) cannot be in the future.")
        if self.is_after_1993_date(self.dialog.e69):
            raise ValueError("Removal Date (E69) must be on or before 10/1/2022.")

    def validate_e153(self):
        try:
            e153 = self.dialog.e153
        except ValueError:
            raise ValueError("Exit Date (E153) is invalid format.")
        if self.dialog.e153 is None:
            raise ValueError("Exit Date (E153) is required.")
        if self.dialog.e153 and not self.is_valid_date(self.dialog.e153):
            raise ValueError("Invalid date provided for Exit Date (E153).")
        if self.is_future_date(self.dialog.e153):
            raise ValueError("Exit Date (E153) cannot be in the future.")
        if self.is_after_1993_date(self.dialog.e153):
            raise ValueError("Exit Date (E153) must be before 10/1/2022.")

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

    @property
    def parent_data(self):
        return self.validator.parent_data

    @parent_data.setter
    def parent_data(self, v):
        self.validator.parent_data = v

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
