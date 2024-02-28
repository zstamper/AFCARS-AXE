import re
from datetime import datetime, date

from dialogs.ooh_dialog import OOHDialog
from utils.e1 import is_state


class OOHBaseValidator:

    def __init__(self, dialog: OOHDialog):
        self.dialog = dialog

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
            assert d <= date.today()
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


class DemographicsValidator(OOHBaseValidator):

    def validate_e4(self) -> None:
        if self.dialog.e4 is None or len(self.dialog.e4) != 12:
            raise ValueError("Child ID (E4) is required and must be exactly 12 characters long.")

    def validate_e5(self) -> None:
        if not self.dialog.e5 or not self.is_valid_date(self.dialog.e5):
            raise ValueError("Invalid date of birth (E5)")

    def validate_e6(self):
        if self.dialog.e6 not in [1, 2]:
            raise ValueError("Child's gender is required (E6).")

    def validate_e13_e14_e15_e16_e17_e18_e19_e20(self) -> None:
        if all([e != 1 for e in
                [self.dialog.e13, self.dialog.e14, self.dialog.e15, self.dialog.e16, self.dialog.e17, self.dialog.e18,
                 self.dialog.e19, self.dialog.e20]]):
            raise ValueError("At least one race must be selected (E13-E20).")
        if any([e == 1 for e in [self.dialog.e19, self.dialog.e20]]) and any(
                e == 1 for e in
                [self.dialog.e13, self.dialog.e14, self.dialog.e15, self.dialog.e16, self.dialog.e17, self.dialog.e18]):
            raise ValueError(
                "No additional races may be selected (E13-E18) if child is abandoned (E19) or race is declined (E20).")
        if self.dialog.e19 == 1 and self.dialog.e20 == 1:
            raise ValueError("Race may be either Abandoned (E19) or Declined (E20), but not both.")

    def validate_e21(self) -> None:
        if self.dialog.e21 is None:
            raise ValueError("Child's hispanic origin (E21) is required.")

    def validate_e41(self):
        if self.dialog.e41 is None:
            raise ValueError("Prior Adoption (E41) is required.")

    def validate_e42_e43(self) -> None:
        if self.dialog.e42 is not None and self.dialog.e43 not in [0, 1]:
            raise ValueError(
                f"Inter-country prior adoption (E43) is required if prior adoption date is specified (E42).")

    def validate_e56(self) -> None:
        if self.dialog.e56 is None:
            raise ValueError("Total number of siblings (E56) is required.")

    def validate_e57(self) -> None:
        if self.dialog.e57 is None and self.dialog.e56:
            raise ValueError("Total number of siblings in foster care (E57) is required.")
        if self.dialog.e57 and self.dialog.e56 and self.dialog.e57 > self.dialog.e56:
            raise ValueError("Siblings in Foster Care (E57) cannot be larger than Total Number of Siblings (E56).")

    def validate_e56_e57(self) -> None:
        if self.dialog.e56 is not None and self.dialog.e57 is not None:
            if self.dialog.e57 > self.dialog.e56:
                raise ValueError(
                    f"Total number of siblings in foster car (E57) may not be more than total number of siblings (E56).")


class ICWAValidator(OOHBaseValidator):

    def validate_funding_e7(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e7 not in [0, 1]:
                raise ValueError(
                    f"'Agency made inquries' (E7) is required."
                )

    def validate_e8(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e8 not in [0, 1, 9]:
                raise ValueError(
                    f"Child's Tribal membership (E8) is required."
                )

    def validate_e10(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e10 not in [0, 1, 9]:
                raise ValueError(
                    "ICWA applicability (E10) is required."
                )

    def validate_e8_e9(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e8 == 1 and (self.dialog.tribes is None or len(self.dialog.tribes) == 0):
                raise ValueError("One or more Tribes should be selected (E9) if the child is a Tribe member (E8).")

    def validate_e10_e11(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e10 == 1:
                if self.dialog.e11 is None:
                    raise ValueError("Date of determination (E11) is required if ICWA applies (E10).")
                if not self.is_valid_date(self.dialog.e11) or self.is_future_date(self.dialog.e11):
                    raise ValueError("Invalid date provided for Date of Determination (E11).")

    def validate_e10_e12(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e10 == 1 and self.dialog.e12 not in [0, 1]:
                raise ValueError("Tribal ICWA notification indication (E12) is required if ICWA applies (E10).")


class HealthValidator(OOHBaseValidator):
    def validate_e22(self):
        if self.dialog.e22 not in [0, 1]:
            raise ValueError("Health Assessment (E22) must be Yes or No.")

    def validate_e23(self):
        if self.dialog.e23 not in [0, 1, 2, 3]:
            raise ValueError("Health conditions (E23) is required.")

    def validate_e24_e34(self):
        if self.dialog.e23 == 1:
            if any([e not in [0, 1, 2] for e in
                    [self.dialog.e24, self.dialog.e25, self.dialog.e26, self.dialog.e27, self.dialog.e28,
                     self.dialog.e29, self.dialog.e30, self.dialog.e31, self.dialog.e32, self.dialog.e33,
                     self.dialog.e34]]):
                raise ValueError(
                    "Responses are required for all health conditions (E24-E34) when the child has a diagnosed condition (E23).")
            if all([e == 0 for e in
                    [self.dialog.e24, self.dialog.e25, self.dialog.e26, self.dialog.e27, self.dialog.e28,
                     self.dialog.e29, self.dialog.e30, self.dialog.e31, self.dialog.e32, self.dialog.e33,
                     self.dialog.e34]]):
                raise ValueError(
                    "Responses are required for all health conditions (E24-E34) when the child has a diagnosed condition (E23).")

    def validate_e6_e38(self):
        if self.dialog.e6 == 2 and self.dialog.e38 not in [0, 1]:
            raise ValueError("Pregnancy indication (E38) is required when child is female (E6).")

    def validate_e39(self):
        if self.dialog.e39 not in [0, 1]:
            raise ValueError("Element E39 is required.")


class ParentGuardianValidator(OOHBaseValidator):
    E59 = re.compile(r'7777|(19|20)[0-9]{2}')
    E60 = re.compile(r'7777|9999|(19|20)[0-9]{2}')
    E66 = re.compile(
        r'66666666|(19|20)[0-9]{2}(((01|03|05|07|08|10|12])(0[1-9]|[12][0-9]|30|31))|(02(0[1-9]|[12][0-9]))|((04|06|09|11)(0[1-9]|[12][0-9]|30)))')

    def validate_e59(self):
        if self.dialog.e59 is None or not self.E59.match(str(self.dialog.e59)):
            raise ValueError("Invalid birth year for first parent or guardian (E59).")
        return self

    def validate_e60(self):
        if self.dialog.e60 is None or not self.E60.match(str(self.dialog.e60)):
            raise ValueError("Invalid birth year for second parent or guardian (E60).")
        elif self.dialog.e60 not in [7777, 9999]:
            current_year: int = datetime.today().year
            if self.dialog.e60 > current_year - 10 or self.dialog.e60 < current_year - 100:
                raise ValueError(
                    f"Second parent birth year (E60) must be in range {current_year - 100}-{current_year - 10}.")
        return self

    def validate_e61(self):
        from utils.e1 import is_tribe
        # Rules:
        #   - Data Format: Numeric – Required unless a tribe or 7777 is entered for E59
        #   - Null should be used if there is no parent
        #   - Null should be used by tribal agencies
        #   - Null should be used if Element 104 is selected
        #   - Disable or do not display for tribes
        #
        # The rules here are plain stupid. It may be null only if there's no mother, E1 is a tribe, or E104 is checked.
        # So If there's a mother or if E1 is a state or E104 is not checked, this field is required.

        def e104() -> int:
            if len(self.dialog.removals2020):
                removals = sorted(self.dialog.removals2020, key=lambda x: x.e69, reverse=True)
                return removals[0].e104
            return 0

        if is_tribe():
            return self
        if self.dialog.e59 == 7777:
            return self
        if e104():
            return self
        if self.dialog.e61 in [0, 1, 9]:
            return self
        raise ValueError("Mother's Tribal membership (E61) must be specified.")

    def validate_e62(self):
        from utils.e1 import is_tribe
        # Rules:
        #   - Data Format: Numeric – Required unless a tribe or 7777 is entered for E59
        #   - Null should be used if there is no parent
        #   - Null should be used by tribal agencies
        #   - Null should be used if Element 104 is selected
        #   - Disable or do not display for tribes
        #
        # The rules here are plain stupid. It may be null only if there's no mother, E1 is a tribe, or E104 is checked.
        # So If there's a mother or if E1 is a state or E104 is not checked, this field is required.

        def e104() -> int:
            if len(self.dialog.removals2020):
                removals = sorted(self.dialog.removals2020, key=lambda x: x.e69, reverse=True)
                return removals[0].e104
            return 0

        if is_tribe():
            return self
        if self.dialog.e60 in [7777, 9999]:
            return self
        if e104():
            return self
        if self.dialog.e62 in [0, 1, 9]:
            return self
        raise ValueError("Father's Tribal membership (E62) must be specified.")

    def validate_e63(self):
        if self.dialog.e63 not in [0, 1, 2]:
            raise ValueError("Mother's TPR (E63) is required.")
        return self

    def validate_e64(self) -> None:
        if self.dialog.e64 not in [0, 1, 2]:
            raise ValueError(f"Second parent's TPR (E64) is required.")


class EducationValidator(OOHBaseValidator):
    def validate_e35(self):
        if self.dialog.e35 not in [0, 1, 2, 3, 4, 5]:
            raise ValueError('School enrollment (E35) is required.')
        return self

    def validate_e36(self):
        if self.dialog.e35 != 0 and self.dialog.e36 not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
            raise ValueError(
                'Highest level of education (E36) is required if the child has ever attended or completed a grade in school not due to age (E35).')
        return self

    def validate_e37(self):
        if self.dialog.e37 not in [0, 1]:
            raise ValueError('A selection for Special Education (E37) is required.')
        return self


class TraffickingValidator(OOHBaseValidator):
    def validate_e106(self):
        if self.dialog.e106 not in [0, 1]:
            raise ValueError("Prior victim of sex trafficking before foster care (E106) is required.")
        return self

    def validate_e107(self):
        if self.dialog.e106 == 1 and self.dialog.e107 not in [0, 1]:
            raise ValueError(
                "Reported to law enforcement (E107) is required if child is victim of sex trafficking (E106).")
        return self

    def validate_e108(self):
        if self.dialog.e107 == 1 and (self.dialog.e108 is None or not self.is_valid_date(self.dialog.e108)):
            raise ValueError("Date reported (E108) is required.")
        return self

    def validate_e109(self):
        if self.dialog.e109 not in [0, 1]:
            raise ValueError("Victim of sex trafficking in foster care (E109) is required.")
        return self

    def validate_e110(self):
        if self.dialog.e109 == 1 and self.dialog.e110 not in [0, 1]:
            raise ValueError(
                "Reported to law enforcement (E110) is required with child is victime of sex trafficking (E109).")
        return self

    def validate_e111(self):
        def e69() -> int | None:
            removals = [removal.e69 for removal in (self.dialog.removals2020 if self.dialog.removals2020 else []) + (
                self.dialog.removals1993 if self.dialog.removals1993 else [])]
            if removals:
                return max(removals)
            return None

        if self.dialog.e110 == 1 and (self.dialog.e111 is None or not self.is_valid_date(self.dialog.e111)):
            raise ValueError("Date report to law enforcement (E111) is required.")
        e = e69()
        if self.dialog.e111 is not None and e and self.dialog.e111 < e:
            raise ValueError(
                "Date law enforcement was contacted (E111) must be after date of most recent removal (E69).")
        return self


class FinancialValidator(OOHBaseValidator):

    def validate_e55(self):
        if self.dialog.e55 not in [0, 1]:
            raise ValueError("Foster Care Maintenance Payment (E55) is required.")


class RemovalValidator(OOHBaseValidator):
    pass
