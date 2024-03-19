import re
from datetime import date, datetime

from dialogs.removal2020_dialog import Removal2020Dialog
from utils import afcars_to_date
from utils.e1 import is_valid_date, is_way_past_date, is_valid_adult_birth_date, e2_end_date


class Removal2020BaseValidator:

    def __init__(self, dialog: Removal2020Dialog):
        self.dialog = dialog

    @staticmethod
    def is_valid_date(d: int) -> bool:
        try:
            d = afcars_to_date(d)
            if d:
                if date(year=date.today().year - 100, month=d.month, day=d.day) <= d <= date.today():
                    return True
        except ValueError:
            pass
        return False


class RemovalValidator(Removal2020BaseValidator):

    def validate_e3(self):
        if bool(self.dialog.ui.e3.text()) and not re.match(r"\d{5}", self.dialog.ui.e3.text()):
            raise ValueError("Agency FIPS code(E3) is invalid.")
        if self.dialog.e3 is None or len(self.dialog.e3) != 5:
            raise ValueError("Agency FIPS code (E3) is required and must be 5 digits.")

    def validate_e69(self) -> None:
        if not self.dialog.ui.e69.text():
            raise ValueError(f"Date of Removal (E69) is required.")
        if not re.match(r"\d+", self.dialog.ui.e69.text()):
            raise ValueError(f"Date of Removal (E69) is invalid.")
        if not is_valid_date(self.dialog.e69):
            raise ValueError(f"Date of Removal (E69) is invalid.")
        if self.dialog.e153 and is_valid_date(self.dialog.e153) and self.dialog.e153 < self.dialog.e69:
            raise ValueError(f"Date of Removal (E69) must be prior to the date of exit (E153).")
        if is_valid_date(self.dialog.child.e5) and self.dialog.e69 < self.dialog.child.e5:
            raise ValueError("Date of Removal (E69) must be on or after the child's data of birth (E5).")
        if afcars_to_date(self.dialog.e69) > e2_end_date():
            raise ValueError("Date of Removal (E69) must be on or before the reporting period end (E2).")

    def validate_e70(self) -> None:
        if not self.dialog.ui.e70.text():
            raise ValueError(f"Removal Transaction Date (E70) is required.")
        if not re.match(r"\d+", self.dialog.ui.e70.text()):
            raise ValueError(f"Removal Transaction Date (E70) is invalid.")
        if not is_valid_date(self.dialog.e70):
            raise ValueError(f"Removal Transaction Date (E70) is invalid.")
        if self.dialog.e69 and is_valid_date(self.dialog.e69):
            removal_date = afcars_to_date(self.dialog.e69)
            tx_date = afcars_to_date(self.dialog.e70)
            delta = tx_date - removal_date
            if delta.days > 30:
                raise ValueError("Removal Transaction Date (E70) must be within 30 days of removal date (E69).")
        if self.dialog.e69 and is_valid_date(self.dialog.e69):
            if self.dialog.e69 > self.dialog.e70:
                raise ValueError("Removal Transaction Date (E70) must be on or after removal date (E69).")
        if is_valid_date(self.dialog.child.e5) and self.dialog.e70 < self.dialog.child.e5:
            raise ValueError("Removal Transaction Date (E70) must be on or after the child's data of birth (E5).")

    def validate_e71(self) -> None:
        if self.dialog.e71 not in (1, 2, 3, 4, 5, 6, 7):
            raise ValueError(f"Environment at Removal (E71) is invalid.")

    def validate_e72_e105(self):
        field_names = [f'e{i}' for i in range(72, 106)]
        for field in field_names:
            if getattr(self.dialog, field) not in (0, 1):
                raise ValueError(f"{field.upper()} is invalid.")
        if not any([getattr(self.dialog, field) == 1 for field in field_names]):
            raise ValueError(f"At least one Family and Child Circumstance must be selected (E72-E105).")

    def validate_e72_e73(self):
        if self.dialog.e72 == 1 and self.dialog.e73 == 1:
            raise ValueError(f"Only one of Runaway (E72) and Whereabouts Unknown (E73) may be selected.")

    def validate_e80_e81_e97(self):
        if self.dialog.e80 and self.dialog.e81 or self.dialog.e80 and self.dialog.e97 or self.dialog.e81 and self.dialog.e97:
            raise ValueError(
                "Only one of Abandonment (E80), Failure to Return (E81), or Voluntary Relinquishment for Adoption (E97) may be selected.")


class ExitValidator(Removal2020BaseValidator):

    def validate_e69_e153(self) -> None:
        if is_valid_date(self.dialog.e69) and is_valid_date(self.dialog.e153):
            if self.dialog.e69 >= self.dialog.e153:
                raise ValueError(f"Date of Removal (e69) must be prior to the Date of Exit (e153) for the same removal")

    def validate_e153(self):
        if self.dialog.ui.e153.text():
            if not re.match(r"\d+", self.dialog.ui.e153.text()):
                raise ValueError(f"Date of Exit (E153) is invalid.")
            if not is_valid_date(self.dialog.e153):
                raise ValueError(f"Date of Exit (E153) is invalid.")
            if self.dialog.e153 <= 20220930:
                raise ValueError("Date of exit (E153) must be on or after October 1, 2022.")
            if self.dialog.e69 is None or self.dialog.e153 <= self.dialog.e69:
                raise ValueError("Date of exit (E153) must be after date of removal (E69).")
            today = int(date.today().strftime('%Y%m%d'))
            if self.dialog.e153 > today:
                raise ValueError("Date of exit (E153) may not be a future date.")

    def validate_e154(self):
        if not re.match(r"\d+", self.dialog.ui.e154.text()):
            raise ValueError(f"Exit Transaction Date (E154) is invalid.")
        if not is_valid_date(self.dialog.e154):
            raise ValueError(f"Exit Transaction Date (E154) is invalid.")
        if self.dialog.e154 <= 20220930:
            raise ValueError("Exit Transaction Date (E154) must be on or after October 1, 2022.")
        today = date.today()
        if afcars_to_date(self.dialog.e154) > today:
            raise ValueError("Exit Transaction Date (E154) may not be a future date.")
        if is_valid_date(self.dialog.e69) and self.dialog.e69 >= self.dialog.e154:
            raise ValueError("Exit Transaction Date (E154) must be after date of removal (E69).")
        if is_valid_date(self.dialog.e153) and self.dialog.e153 > self.dialog.e154:
            raise ValueError("Exit Transaction Date (E154) must be after date of exit (E153).")
        if is_valid_date(self.dialog.e153):
            exit_date = afcars_to_date(self.dialog.e153)
            tx_date = afcars_to_date(self.dialog.e154)
            delta = tx_date - exit_date
            if delta.days > 30:
                raise ValueError("Exit Transaction Date (E154) must be within 30 days of exit date (E153).")


    def validate_e155(self):
        if self.dialog.e155 not in (1, 2, 3, 4, 5, 6, 7, 8, 9):
            raise ValueError(f"Exit Reason (E155) is invalid.")
        if self.dialog.e153 is None and self.dialog.e155 != 9:
            raise ValueError("Exit reason (E155) must be 'Not Applicable' when no exit date (E153) is provided.")

    def validate_e156(self):
        if self.dialog.e155 == 8 and self.dialog.e156 is None:
            raise ValueError(
                "Agency indicator (E156) is required when exit reason (E155) indicates 'Transfer to another Agency'.")

    def validate_e157(self):
        if self.dialog.e155 in [3, 5] and self.dialog.e157 is None:
            raise ValueError(
                "Marital status of adoptive parent (E157) is required when exit reason (E155) is Adoption or Guardianship.")

    def validate_e158_e159_e160_e161(self):
        if self.dialog.e155 in (
                3,
                5) and self.dialog.e158 == 0 and self.dialog.e159 == 0 and self.dialog.e160 == 0 and self.dialog.e161 == 0:
            raise ValueError(
                "At least one Relationship (E158, E159, E160, E161) must be checked when Exit Reason (E155) is Adoption or Guardianship.")

    def validate_e162(self):
        if self.dialog.e155 in (3, 5):
            if not self.dialog.ui.e162.text():
                raise ValueError(
                    "Date of Birth for first adoptive parent or guardian (E162) is required.")
            if not re.match(r"\d+", self.dialog.ui.e162.text()):
                raise ValueError("Date of Birth for first adoptive parent or guardian (E162) is invalid.")
            if not is_valid_date(self.dialog.e162):
                raise ValueError("Date of Birth for first adoptive parent or guardian (E162) is invalid.")

    def validate_e163(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e163 not in (0, 1, 9):
            raise ValueError(
                "Tribal membership of first adoptive parent or guardian (E163) is required when Exit Reason (E155) is Adoption or Guardianship.")

    def validate_e164_e165_e166_e167_e168_e169_e170(self):
        if self.dialog.e155 in (3, 5) and not any(
                [self.dialog.e164, self.dialog.e165, self.dialog.e166, self.dialog.e167, self.dialog.e168,
                 self.dialog.e169, self.dialog.e170]):
            raise ValueError(
                "Adoptive parent race (E164, E165, E166, E167, E168, E169, E170) is required when Exit Reason (E155) is Adoption or Guardianship.")
        if self.dialog.e155 in (3, 5) and self.dialog.e170 and any(
                [self.dialog.e164, self.dialog.e165, self.dialog.e166, self.dialog.e167, self.dialog.e168,
                 self.dialog.e169]):
            raise ValueError("When race is declined (E170), no other racial indicators may be selected (E164-E169).")

    def validate_e171(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e171 not in (0, 1, 8, 9):
            raise ValueError(
                'Hispanic/Latino ethnicity of first adoptive parent or guardian (E171) is required when Exit Reason (E155) is Adoption or Guardianship.')

    def validate_e172(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e172 not in (1, 2):
            raise ValueError(
                'Sex of first adoptive parent or guardian (E172) is required when Exit Reason (E155) is Adoption or Guardianship by a couple.')

    def validate_e173(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1, 2):
            if not self.dialog.ui.e173.text():
                raise ValueError("Date of Birth for second adoptive parent or guardian (E173) is required.")
            if not re.match(r"\d+", self.dialog.ui.e173.text()):
                raise ValueError("Date of Birth for second adoptive parent or guardian (E173) is invalid.")
            if self.dialog.e173 and not is_valid_date(self.dialog.e173):
                raise ValueError("Date of Birth for second adoptive parent or guardian (E173) is invalid.")
            if self.dialog.e173 and not is_valid_adult_birth_date(self.dialog.e173):
                raise ValueError(
                    "Age of second adoptive parent or guardian (E173) must be between 10 and 100 years old.")

    def validate_e174(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1, 2) and self.dialog.e174 not in (0, 1, 9):
            raise ValueError(
                "Tribal membership of second adoptive parent or guardian (E174) is required.")

    def validate_e175_e176_e177_e178_e179_e180_e181(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1, 2) and not any(
                [self.dialog.e175, self.dialog.e176, self.dialog.e177, self.dialog.e178, self.dialog.e179,
                 self.dialog.e180, self.dialog.e181]):
            raise ValueError(
                "Adoptive parent race (E175, E176, E177, E178, E179, E180, E181) is required.")
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1, 2) and self.dialog.e181 and any(
                [self.dialog.e175, self.dialog.e176, self.dialog.e177, self.dialog.e178, self.dialog.e179,
                 self.dialog.e180]):
            raise ValueError("When race is declined (E181), no other racial indicators may be selected (E175-E180).")

    def validate_e182(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1, 2) and self.dialog.e182 not in (0, 1, 8, 9):
            raise ValueError(
                'Hispanic/Latino ethnicity of first adoptive parent or guardian (E182) is required.')

    def validate_e183(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1, 2) and self.dialog.e183 not in (1, 2):
            raise ValueError(
                'Sex of first adoptive parent or guardian (E183) is required.')

    def validate_e185(self):
        if self.dialog.e155 in [3, 5] and self.dialog.e185 is None:
            raise ValueError("Adoption or Guardianship Type (E185) is required.")

    def validate_e186(self):
        if self.dialog.e155 in [3,5]:
            if not re.match(r"\d+", self.dialog.ui.e186.text()):
                raise ValueError("Number of Siblings in the Guardian or Adoption Home (E186) is missing or invalid.")


class PermanencyPlanValidator(Removal2020BaseValidator):

    def validate_e69_e147(self):
        for plan in self.dialog.permanency_plans:
            if plan.e147 < self.dialog.e69:
                raise ValueError(f"Permanency plan dates (E147) must be on or after date of removal (E69).")
