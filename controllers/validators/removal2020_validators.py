from datetime import date

from dialogs.removal2020_dialog import Removal2020Dialog


class Removal2020BaseValidator:

    def __init__(self, dialog: Removal2020Dialog):
        self.dialog = dialog

    @staticmethod
    def is_valid_date(d: int) -> bool:
        try:
            s = str(d)
            year = int(s[0:4])
            month = int(s[4:6])
            day = int(s[6:8])
            d = date(year=year, month=month, day=day)
            if date(year=date.today().year-100, month=month, day=day) <= d <= date.today():
                return True
        except ValueError:
            pass
        return False


class RemovalValidator(Removal2020BaseValidator):

    def validate_e3(self):
        if self.dialog.e3 is None or len(self.dialog.e3) != 5:
            raise ValueError("Agency FIPS code (E3) is required and must be 5 digits.")

    def validate_e69(self) -> None:
        if not self.is_valid_date(self.dialog.e69):
            raise ValueError(f"Invalid date specified for Date of Removal (E69).")

    def validate_e71(self) -> None:
        if self.dialog.e71 not in (1, 2, 3, 4, 5, 6, 7):
            raise ValueError(f"Invalid selection for Environment at Removal (E71).")

    def validate_e72_e105(self):
        field_names = [f'e{i}' for i in range(72, 106)]
        for field in field_names:
            if getattr(self.dialog, field) not in (0, 1):
                raise ValueError(f"Invalid selection for {field.upper()}.")
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
        if self.dialog.e69 is not None and self.dialog.e153 is not None:
            if self.dialog.e69 >= self.dialog.e153:
                raise ValueError(f"Date of Removal (e69) must be prior to the Date of Exit (e153) for the same removal")

    def validate_e153(self):
        if self.dialog.e153 is not None:
            if not self.is_valid_date(self.dialog.e153):
                raise ValueError(f"Invalid date specified for Date of Exit (E153).")
            if self.dialog.e153 <= 20220930:
                raise ValueError("Date of exit (E153) must be on or after October 1, 2022.")
            if self.dialog.e69 is None or self.dialog.e153 <= self.dialog.e69:
                raise ValueError("Date of exit (E153) must be after date of removal (E69).")
            today = int(date.today().strftime('%Y%m%d'))
            if self.dialog.e153 > today:
                raise ValueError("Date of exit (E153) may not be a future date.")

    def validate_e155(self):
        if self.dialog.e155 not in (1, 2, 3, 4, 5, 6, 7, 8, 9):
            raise ValueError(f"Invalid selection for Exit Reason (E155).")
        if self.dialog.e153 is None and self.dialog.e155 != 9:
            raise ValueError("Exit reason (E155) must be 'Not Applicable' when no exit date (E153) is provided.")

    def validate_e156(self):
        if self.dialog.e155 != 8 and self.dialog.e156 is not None:
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
        if self.dialog.e155 in (3, 5) and self.dialog.e162 is None:
            raise ValueError(
                "Date of Birth for first adoptive parent or guardian (E162) is required when Exit Reason (E155) is Adoption or Guadianship.")

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
                'Sex of first adoptive parent or guardian (E172) is required when Exit Reason (E155) is Adoption or Guardianship.')

    def validate_e173(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1,2) and self.dialog.e173 is None:
            raise ValueError(
                "Date of Birth for second adoptive parent or guardian (E173) is required when Exit Reason (E155) is Adoption or Guadianship.")
        return self

    def validate_e174(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1,2) and self.dialog.e174 not in (0, 1, 9):
            raise ValueError(
                "Tribal membership of second adoptive parent or guardian (E174) is required when Exit Reason (E155) is Adoption or Guardianship.")

    def validate_e175_e176_e177_e178_e179_e180_e181(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1,2) and not any(
                [self.dialog.e175, self.dialog.e176, self.dialog.e177, self.dialog.e178, self.dialog.e179,
                 self.dialog.e180, self.dialog.e181]):
            raise ValueError(
                "Adoptive parent race (E175, E176, E177, E178, E179, E180, E181) is required when Exit Reason (E155) is Adoption or Guardianship.")
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1,2) and self.dialog.e181 and any(
                [self.dialog.e175, self.dialog.e176, self.dialog.e177, self.dialog.e178, self.dialog.e179,
                 self.dialog.e180]):
            raise ValueError("When race is declined (E181), no other racial indicators may be selected (E175-E180).")

    def validate_e182(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1,2) and self.dialog.e182 not in (0, 1, 8, 9):
            raise ValueError(
                'Hispanic/Latino ethnicity of first adoptive parent or guardian (E182) is required when Exit Reason (E155) is Adoption or Guardianship.')

    def validate_e183(self):
        if self.dialog.e155 in (3, 5) and self.dialog.e157 in (1,2) and self.dialog.e183 not in (1, 2):
            raise ValueError(
                'Sex of first adoptive parent or guardian (E183) is required when Exit Reason (E155) is Adoption or Guardianship.')


class PermanencyPlanValidator(Removal2020BaseValidator):

    def validate_e69_e147(self):
        for plan in self.dialog.permanency_plans:
            if plan.e147 < self.dialog.e69:
                raise ValueError(f"Permanency plan dates (E147) must be on or after date of removal (E69).")
