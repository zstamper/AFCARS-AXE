from datetime import date

from controllers.validators.abstract_validator import AbstractValidator
from dialogs.periodic_review_dialog import PeriodicReviewDialog


class PeriodicReviewBaseValidator:

    def __init__(self, dialog: PeriodicReviewDialog):
        self.dialog: PeriodicReviewDialog = dialog

    @staticmethod
    def is_valid_date(d: int) -> bool:
        try:
            s = str(d)
            year = int(s[0:4])
            month = int(s[4:6])
            day = int(s[6:8])
            d = date(year=year, month=month, day=day)
            today = date.today()
            min_d = date(year=today.year - 100, month=today.month, day=today.day)
            assert d >= min_d
            return True
        except ValueError:
            return False
        except AssertionError:
            return False

    @staticmethod
    def is_future_date(d: int) -> bool:
        year = d // 10000
        month = (d - (d // 10000) * 10000) // 100
        day = d - (d // 100) * 100
        d = date(year=year, month=month, day=day)
        return d > date.today()


class PeriodicReviewValidators(PeriodicReviewBaseValidator):

    def validate_e149(self):
        if not self.is_valid_date(self.dialog.e149):
            raise ValueError("Invalid date for Periodic Review Date (E149).")
        if self.is_future_date(self.dialog.e149):
            raise ValueError("Periodic Review Date (E149) cannot be in the future.")


class PeriodicReviewValidator(AbstractValidator):
    def __init__(self, dialog):
        self.dialog = dialog
        self.validator = PeriodicReviewValidators(self.dialog)
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

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]