from datetime import date

from dialogs.a_dialog import ADialog
from .abstract_validator import AbstractValidator


class ABaseValidator:
    def __init__(self, dialog: ADialog):
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


class AValidators(ABaseValidator):
    pass


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
