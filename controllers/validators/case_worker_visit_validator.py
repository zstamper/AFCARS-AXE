from datetime import date
from typing import Optional

from controllers.validators.abstract_validator import AbstractValidator
from dialogs.case_worker_visit_dialog import CaseVisitDialog
from model import CaseVisit, Removal2020
from utils.e1 import e2_start_date, e2_end_date, afcars_to_date


class CaseWorkerVisitBaseValidator:

    def __init__(self, dialog: CaseVisitDialog):
        self.parent_data: Optional[Removal2020] = None
        self.dialog: CaseVisitDialog = dialog

    @staticmethod
    def is_valid_date(d: int) -> bool:
        try:
            d = afcars_to_date(d)
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
        d = afcars_to_date(d)
        return d > date.today()

    @staticmethod
    def is_current_period(d: int) -> bool:
        d = afcars_to_date(d)
        return e2_start_date() <= d <= e2_end_date()


class CaseWorkerVisitValidators(CaseWorkerVisitBaseValidator):

    def validate_e151(self):
        if not self.is_valid_date(self.dialog.e151):
            raise ValueError("Date of Visit (E151) is invalid.")
        if self.is_future_date(self.dialog.e151):
            raise ValueError("Date of Visit (E151) may not be in the future.")
        if self.dialog.e151 < self.parent_data.e69:
            raise ValueError("Date of Visit (E151) may not be before the Removal Date (E69).")
        if self.dialog.e151 and not self.is_current_period(self.dialog.e151):
            raise ValueError("Date of Visit (E151) must be from current reporting period (E1).")

    def validate_e152(self):
        if self.dialog.e151 is not None and self.dialog.e152 is None:
            raise ValueError(
                "Caseworker Visit Location (E152) is required when a Caseworker Visit Date (E151) is specified.")
        if self.dialog.e152 not in (1, 2):
            raise ValueError("Invalid Caseworker Visit Location (E152).")


class CaseWorkerVisitValidator(AbstractValidator):
    def __init__(self, dialog):
        self.dialog = dialog
        self.validator = CaseWorkerVisitValidators(self.dialog)
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
