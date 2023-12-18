from datetime import date

from controllers.validators.abstract_validator import AbstractValidator
from dialogs.case_worker_visit_dialog import CaseVisitDialog


class CaseWorkerVisitBaseValidator:

    def __init__(self, dialog: CaseVisitDialog):
        self.dialog: CaseVisitDialog = dialog

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


class CaseWorkerVisitValidators(CaseWorkerVisitBaseValidator):
    pass


class CaseWorkerVisitValidator(AbstractValidator):
    def __init__(self, dialog):
        self.dialog = dialog
        self.validator = CaseWorkerVisitValidators(self.dialog)
        self._messages: list[ValueError] = []

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
        return self._messages
