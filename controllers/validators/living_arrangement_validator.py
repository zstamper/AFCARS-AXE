import datetime
import re
from datetime import date
from typing import Optional

from dialogs.living_arrangement_dialog import LivingArrangementDialog
from model import Removal2020
from utils.e1 import is_valid_date, is_future_date, e2_end_date, afcars_to_date


class LivingArrangementValidators:

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

    def __init__(self, dialog: LivingArrangementDialog):
        self.parent_data: Optional[Removal2020] = None
        self.dialog: LivingArrangementDialog = dialog

    def validate_e40(self):
        if self.dialog.e40 not in [0, 1, 9]:
            raise ValueError("Child and his/her Child(ren) Placed together (E40) is required.")

    def validate_e58(self):
        if self.dialog.e56 is not None and self.dialog.e56 == 0 and self.dialog.e58 is not None:
            raise ValueError("Number of siblings placed with this child (E58) should be left empty.")
        if self.dialog.e57 is not None and self.dialog.e57 == 0 and self.dialog.e58 is not None:
            raise ValueError("Number of siblings placed with this child (E58) must be left empty.")
        if self.dialog.e57 is not None and self.dialog.e58 is not None and self.dialog.e58 > self.dialog.e57:
            raise ValueError(
                "Number of siblings placed with this child (E58) cannot exceed number of siblings in foster care (E57).")
        if bool(self.dialog.e56) and bool(self.dialog.e57) and not bool(re.match(r"\d+", self.dialog.ui.e58.text())):
            raise ValueError("Number of siblings placed with this child (E58) is invalid.")

    def validate_e112(self):
        if not self.dialog.ui.e112.text():
            raise ValueError("Living Arrangement Start date (E112) is required.")
        if not re.match(r"\d+", self.dialog.ui.e112.text()):
            raise ValueError("Living Arrangement Start Date (E112) is invalid.")
        if not is_valid_date(self.dialog.e112):
            raise ValueError("Living Arrangement Start Date (E112) is invalid.")
        if is_future_date(self.dialog.e112):
            raise ValueError("Living Arrangement Start Date (E112) cannot be in the future.")
        if self.parent_data.e69 and self.dialog.e112 < self.parent_data.e69:
            raise ValueError("Living Arrangement Start Date (E112) may not be earlier than Removal Date (E69)")
        if afcars_to_date(self.dialog.e112) > e2_end_date():
            raise ValueError("Living Arrangement Start Date (E112) must be before end of reporting period (E2).")

    def validate_e113(self):
        if self.dialog.e113 not in (0, 1):
            raise ValueError("Foster family home (E113) is required.")
        if self.dialog.e113 in (None, 0) and self.dialog.e120 in (None, 0):
            raise ValueError("Living Arrangement Type (E113, E120) is required.")

    def validate_e120(self):
        if self.dialog.e113 == 1 and self.dialog.e120 is not None:
            print(f"e120=({type(self.dialog.e120)}) {self.dialog.e120}")
            if self.dialog.e120 not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
                raise ValueError("Living arrangement (E120) is invalid.")

    def validate_e114_e118(self):
        fields = [self.dialog.e114, self.dialog.e115, self.dialog.e116, self.dialog.e117, self.dialog.e118,
                  self.dialog.e119]
        if self.dialog.e113 == 1:
            if not any([x == 1 for x in fields]):
                raise ValueError(
                    "At least one of E114, E115, E116, E118 must be checked, or Relationship must be Relative or Kin when Living Arrangement Type (E120) is Foster Family Home.")

    def validate_e121(self):
        if not self.dialog.e121 in (1, 2, 3, 4):
            raise ValueError("Location (E121) is required.")
        if self.dialog.e120 in (12, 13) and self.dialog.e121 != 4:
            raise ValueError(
                'Location of Living Arrangement (E121) should be Runaway or Whereabouts Unknown when Living Arrangement Type (E113, E120) is Runaway or Whereabouts Unknown.')
        if self.dialog.e121 == 4 and self.dialog.e120 not in (12, 13):
            raise ValueError(
                'Location of Living Arrangement (E121) should be Runaway or Whereabouts Unknown when Living Arrangement Type (E113, E120) is Runaway or Whereabouts Unknown.')

    def validate_e122(self):
        if self.dialog.e121 in (2, 3):
            if not self.dialog.e122:
                raise ValueError(
                    "Jurisdiction (E122) is required when Living Arrangement (E121) is 'out of state' or 'out of country'.")

    def validate_e123(self):
        if self.dialog.e113 == 1 and self.dialog.e123 not in (1, 2, 3, 4):
            raise ValueError(
                "Marital status of the foster parent(E123) is required when child is placed in foster family home (E113/E120)."
            )

    def validate_e124(self):
        if self.dialog.e113 == 1 and self.dialog.e124 not in (1, 2, 3):
            raise ValueError("Foster Parent's Relationship to the Child (E124) is required.")

    def validate_e125(self):
        if self.dialog.e113 == 1:
            if not self.dialog.ui.e125.text():
                raise ValueError(
                    "First foster parent's year of birth (E125) is required.")
            if not re.match(r"\d+", self.dialog.ui.e125.text()):
                raise ValueError("First Foster Parent's Year of Birth (E125) is invalid.")
            year = datetime.date.today().year
            if not 10 <= year - self.dialog.e125 < 100:
                raise ValueError(
                    "Foster parent's year of birth (E125) is outside of allowed range (age must be greater than 10 and less than 100).")

    def validate_e126(self):
        if self.dialog.e113 == 1:
            if self.dialog.e126 not in (0, 1, 9):
                raise ValueError("First foster parent's tribal membership (E126) is required.")

    def validate_e127_e133(self):
        fields = [self.dialog.e127, self.dialog.e128, self.dialog.e129, self.dialog.e130, self.dialog.e131,
                  self.dialog.e132, self.dialog.e133]
        if self.dialog.e113 == 1:
            if all([x == 0 for x in fields]):
                raise ValueError("First foster parent's race is required (E127 - E133).")

    def validate_e134(self):
        if self.dialog.e113 == 1:
            if self.dialog.e134 not in (0, 1, 8, 9):
                raise ValueError(
                    "First foster parent's hispanic or latino origin (E134) is required.")

    def validate_e135(self):
        if self.dialog.e113 == 1:
            if self.dialog.e135 not in (1, 2):
                raise ValueError(
                    "First foster parent's sex (E135) is required.")

    def validate_e136(self):
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if not self.dialog.ui.e136.text():
                raise ValueError(
                    "Second foster parent's year of birth (E136) is required.")
            if not re.match(r"\d+", self.dialog.ui.e136.text()):
                raise ValueError("Second Foster Parent's Year of Birth (E136) is invalid.")
            year = datetime.date.today().year
            if not 10 <= year - self.dialog.e136 < 100:
                raise ValueError(
                    "Second foster parent's year of birth (E136) is outside of allowed range (age must be greater than 10 and less than 100).")

    def validate_e137(self):
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if self.dialog.e137 not in (0, 1, 9):
                raise ValueError("Second foster parent's tribal membership (E137) is required.")

    def validate_e138_e144(self):
        fields = [self.dialog.e138, self.dialog.e139, self.dialog.e140, self.dialog.e141, self.dialog.e142,
                  self.dialog.e143, self.dialog.e144]
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if all([x == 0 for x in fields]):
                raise ValueError("Second foster parent's race is required (E138 - E144).")

    def validate_e145(self):
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if self.dialog.e145 not in (0, 1, 8, 9):
                raise ValueError(
                    "Second foster parent's hispanic or latino origin (E145) is required.")

    def validate_e146(self):
        if self.dialog.e113 == 1:
            if self.dialog.e146 not in (1, 2) and self.dialog.e123 in (1, 2):
                raise ValueError(
                    "Second foster parent's sex (E146) is required.")


class LivingArrangementValidator:

    def __init__(self, dialog: LivingArrangementDialog):
        self.dialog = dialog
        self.validator = LivingArrangementValidators(dialog)
        self._messages: list[Exception] = []

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

    def messages(self) -> list[str]:
        return [exc.args[0] for exc in self._messages]
