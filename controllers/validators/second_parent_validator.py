import re
from datetime import date

from dialogs.second_parent_dialog import Parent2Dialog
from utils.e1 import is_valid_date, is_future_date, is_way_past_date, afcars_to_date, e2_end_date
from .abstract_validator import AbstractValidator


class SecondParentBaseValidator:

    def __init__(self, dialog: Parent2Dialog):
        self.dialog: Parent2Dialog = dialog

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


class SecondParentValidators(SecondParentBaseValidator):

    def validate_e64(self):
        if self.dialog.e64 not in [0, 1, 2]:
            raise ValueError("Termination/Modification of parental rights (E64) is required.")

    def validate_e66(self):
        if self.dialog.e64 in [1,2] and not bool(self.dialog.ui.e66.text()):
            raise ValueError("Date of Petition for Termination (E66) is required.")
        if bool(self.dialog.ui.e66.text()) and self.dialog.e66 != 66666666:
            if not re.match(r"\d+", self.dialog.ui.e66.text()):
                raise ValueError("Date of Petition for Termination (E66) is invalid.")
            if not is_valid_date(self.dialog.e66):
                raise ValueError("Date of Petition for Termination (E66) is invalid.")
            if is_future_date(self.dialog.e66):
                raise ValueError("Date of Petition for Termination (E66) may not be in the future.")
            if is_way_past_date(self.dialog.e66):
                raise ValueError("Date of Petition for Termination (E66) is too far in the past.")
            # if self.dialog.e64 == 0:
            #     raise ValueError("Date of Petition for Termination (E66) should be blank when E64 is not applicable.")
            if afcars_to_date(self.dialog.e66) > e2_end_date():
                raise ValueError("Date of Petition for Termination (E66) can't be after current period.")

    def validate_e68(self):
        if self.dialog.ui.e68.text():
            if not re.match(r"\d+", self.dialog.ui.e68.text()):
                raise ValueError("Date of Termination (E68) is invalid.")
            if not is_valid_date(self.dialog.e68):
                raise ValueError("Date of Termination (E68) is invalid.")
            if is_future_date(self.dialog.e68):
                raise ValueError("Date of Termination (E68) may not be in the future.")
            if is_way_past_date(self.dialog.e68):
                raise ValueError("Date of Termination (E68) is too far in the past.")
            # if self.dialog.e64 == 0:
            #     raise ValueError("Date of Termination (E68) should be blank when E64 is not applicable.")
            if afcars_to_date(self.dialog.e68) > e2_end_date():
                raise ValueError("Date of Termination (E68) can't be after current period.")


class SecondParentValidator(AbstractValidator):
    def __init__(self, dialog: Parent2Dialog):
        self.dialog = dialog
        self.validator = SecondParentValidators(self.dialog)
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
