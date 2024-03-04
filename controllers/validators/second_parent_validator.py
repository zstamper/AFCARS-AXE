from datetime import date

from dialogs.second_parent_dialog import Parent2Dialog
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
        if self.dialog.e64 == 0 and self.dialog.e66 is not None:
            raise ValueError("Petition Date (E66) should be empty when Termination/Modification (E64) does not apply.")
        if self.dialog.e64 > 0 and self.dialog.e66 is None:
            raise ValueError("Petition Date (E66) is required when Termination/Modification (E64) applies.")
        if not self.is_valid_date(self.dialog.e66):
            raise ValueError("Petition Date (E66) is invalid.")

    def validate_e68(self):
        if self.dialog.e68 is not None and not self.is_valid_date(self.dialog.e68):
            raise ValueError("Termination date (E68) is not a valid date.")


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
