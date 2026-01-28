# Copyright 2024 by ICF International, Inc.
#
# This file is part of AXE, the AFCARS XML Editor.
#
# AXE is free software: you can redistribute it and/or modify it under the terms
# of the GNU Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# AXE is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# AXE. If not, see <https://www.gnu.org/licenses/>.

import re
from datetime import date

from controllers.validators.common_validators import CommonValidators
from dialogs.ooh_dialog import OOHDialog
from model.models import ReportType
from utils.e1 import is_state, is_future_date, is_way_past_date, afcars_to_date, is_valid_date, is_valid_year_month, \
    is_future_year_month, is_way_past_year_month, e2_end_date


class OOHBaseValidator:

    def __init__(self, dialog: OOHDialog):
        self.dialog = dialog

    @staticmethod
    def is_valid_date(d: int) -> bool:
        try:
            d = afcars_to_date(d)
            today = date.today()
            min_d = date(year=today.year - 100, month=today.month, day=today.day)
            assert min_d <= d <= date.today()
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


class DemographicsValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH

    def validate_e13_e14_e15_e16_e17_e18_e19_e20(self) -> None:
        if all([e != 1 for e in
                [self.dialog.e13, self.dialog.e14, self.dialog.e15, self.dialog.e16, self.dialog.e17, self.dialog.e18,
                 self.dialog.e19, self.dialog.e20]]):
            raise ValueError(f"At least one race must be selected ({self.f('E13')}-{self.f('E20')}).")
        if any([e == 1 for e in [self.dialog.e19, self.dialog.e20]]) and any(
                e == 1 for e in
                [self.dialog.e13, self.dialog.e14, self.dialog.e15, self.dialog.e16, self.dialog.e17, self.dialog.e18]):
            raise ValueError(
                f"No additional races may be selected ({self.f('E13')}-{self.f('E18')}) if child is abandoned ({self.f('E19')}) or race is declined ({self.f('E20')}).")
        if self.dialog.e19 == 1 and self.dialog.e20 == 1:
            raise ValueError(
                f"Race may be either Abandoned ({self.f('E19')}) or Declined ({self.f('E20')}), but not both.")

    def validate_e21(self) -> None:
        if self.dialog.e21 is None:
            raise ValueError(f"Child's hispanic origin ({self.f('E21')}) is required.")

    def validate_e41(self):
        if self.dialog.e41 is None:
            raise ValueError("Prior Adoption (E41) is required.")

    def validate_e42(self):
        if bool(self.dialog.ui.e42.text()) and not re.match(r'\d+', self.dialog.ui.e42.text()):
            raise ValueError("Prior Adoption Date (E42) is invalid.")
        if self.dialog.e41 == 1:
            if not is_valid_year_month(self.dialog.e42):
                raise ValueError("Prior Adoption Date (E42) is invalid.")
            if is_future_year_month(self.dialog.e42):
                raise ValueError("Prior Adoption Date (E42) may not be in the future.")
            if is_way_past_year_month(self.dialog.e42):
                raise ValueError("Prior Adoption Date (E42) is too far in the past.")
            if self.dialog.e42 and self.dialog.e5:
                dob_year_month = self.dialog.e5 // 100
                if self.dialog.e42 < dob_year_month:
                    raise ValueError("Prior Adoption Date (E42) cannot be before Child's Date of Birth (E5).")
            for removal in (self.dialog.removals1993 + self.dialog.removals2020):
                        if removal.e69:
                            removal_year_month = removal.e69 // 100
                            if self.dialog.e42 > removal_year_month:
                                raise ValueError("Prior Adoption Date (E42) cannot be after the most recent removal date (E69).")


    def validate_e42_e43(self) -> None:
        if self.dialog.e42 is not None and self.dialog.e43 not in [0, 1]:
            raise ValueError(
                f"Inter-country prior adoption (E43) is required if prior adoption date is specified (E42).")

    def validate_e45(self):
        if bool(self.dialog.ui.e45.text()) and not re.match(r'\d+', self.dialog.ui.e45.text()):
            raise ValueError("Prior Guardianship Date (E45) is invalid.")
        if self.dialog.e44 == 1:
            if not is_valid_year_month(self.dialog.e45):
                raise ValueError("Prior Guardianship Date (E45) is invalid.")
            if is_future_year_month(self.dialog.e45):
                raise ValueError("Prior Guardianship Date (E45) may not be in the future.")
            if is_way_past_year_month(self.dialog.e45):
                raise ValueError("Prior Guardianship Date (E45) is too far in the past.")
            if self.dialog.e45 and self.dialog.e5:
                dob_year_month = self.dialog.e5 // 100
                if self.dialog.e45 < dob_year_month:
                    raise ValueError("Prior Guardianship Date (E45) cannot be before Child's Date of Birth (E5).")
            for removal in (self.dialog.removals1993 + self.dialog.removals2020):
                        if removal.e69:
                            removal_year_month = removal.e69 // 100
                            if self.dialog.e45 > removal_year_month:
                                raise ValueError("Prior Guardianship Date (E45) cannot be after the most recent removal date (E69).")


    def validate_e56(self) -> None:
        if not self.dialog.ui.e56.text():
            raise ValueError("Total number of siblings (E56) is required.")
        if not re.match(r'\d+', self.dialog.ui.e56.text()):
            raise ValueError("Total Number of Siblings (E56) is invalid.")

    def validate_e57(self) -> None:
        if self.dialog.e57 is None and self.dialog.e56 is not None and self.dialog.e56 > 0:
            raise ValueError("Total number of siblings in foster care (E57) is required.")
        if bool(self.dialog.e56) and not bool(re.match(r'\d+', self.dialog.ui.e57.text())):
            raise ValueError("Siblings in Foster Care (E57) is invalid.")

    def validate_e56_e57(self) -> None:
        if self.dialog.e57 is not None and self.dialog.e56 is not None and self.dialog.e57 > self.dialog.e56:
            raise ValueError("Siblings in Foster Care (E57) cannot be larger than Total Number of Siblings (E56).")


class ICWAValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH

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
                if not re.match(r"\d+", self.dialog.ui.e11.text()):
                    raise ValueError("Date of Determination (E11) is invalid.")
                if self.dialog.e11 is None:
                    raise ValueError("Date of determination (E11) is required if ICWA applies (E10).")
                if not is_valid_date(self.dialog.e11):
                    raise ValueError("Date of Determination (E11) is invalid.")
                if is_future_date(self.dialog.e11):
                    raise ValueError("Date of Determination (E11) may not be a future date.")
                if is_way_past_date(self.dialog.e11):
                    raise ValueError("Date of Determination (E11) is too far in the past.")

    def validate_e10_e12(self):
        if is_state() and self.dialog.funding == 0:
            if self.dialog.e10 == 1 and self.dialog.e12 not in [0, 1]:
                raise ValueError("Tribal ICWA notification indication (E12) is required.")


class HealthValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH

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
                    "At least one health condition/diagnosis (E24-E34) must be selected.")

    def validate_e6_e38(self):
        if self.dialog.e6 == 2 and self.dialog.e38 not in [0, 1]:
            raise ValueError("Pregnancy indication (E38) is required when child is female (E6).")

    def validate_e39(self):
        if self.dialog.e39 not in [0, 1]:
            raise ValueError("Element E39 is required.")


class ParentGuardianValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH
    E59 = re.compile(r'7777|(19|20)[0-9]{2}')
    E60 = re.compile(r'7777|9999|(19|20)[0-9]{2}')
    E66 = re.compile(
        r'66666666|(19|20)[0-9]{2}(((01|03|05|07|08|10|12])(0[1-9]|[12][0-9]|30|31))|(02(0[1-9]|[12][0-9]))|((04|06|09|11)(0[1-9]|[12][0-9]|30)))')

    def validate_e59(self):
        if not re.match(r"\d+", self.dialog.ui.e59.text()):
            raise ValueError("First Parent or Guardian Birth Year (E59) is invalid.")
        if self.dialog.e59 is None or not self.E59.match(str(self.dialog.e59)):
            raise ValueError("First Parent or Guardian Birth Year (E59) is invalid.")
        if self.dialog.e59 != 7777:
            if not (date.today().year - 100 < self.dialog.e59 < date.today().year - 10):
                raise ValueError("First parent or Guardian must be between 10 and 100 years old (E59).")

    def validate_e60(self):
        if not re.match(r"\d+", self.dialog.ui.e60.text()):
            raise ValueError("Second Parent or Guardian (E60) is invalid.")
        if self.dialog.e60 is None or not self.E60.match(str(self.dialog.e60)):
            raise ValueError("Second Parent or Guardian (E60) is invalid.")
        elif self.dialog.e60 not in [7777, 9999]:
            if not (date.today().year - 100 < self.dialog.e60 < date.today().year - 10):
                raise ValueError("Age of second parent or guardian must be between 10 and 100 years old (E60).")

    def validate_e61(self) -> None:
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
            valid_removals = [r for r in self.dialog.removals2020 if r.e69 is not None]
            if valid_removals:
                removals = sorted(valid_removals, key=lambda x: x.e69, reverse=True)
                return removals[0].e104
            return 0

        if is_tribe():
            return
        if self.dialog.e59 == 7777:
            return
        if e104():
            return
        if self.dialog.e61 in [0, 1, 9]:
            return
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
            valid_removals = [r for r in self.dialog.removals2020 if r.e69 is not None]
            if valid_removals:
                removals = sorted(valid_removals, key=lambda x: x.e69, reverse=True)
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
        if self.dialog.e60 not in [None, 7777, 9999] and self.dialog.e64 not in [0, 1, 2]:
            raise ValueError(f"Second parent's TPR (E64) is required.")

    def validate_e65(self) -> None:
        if bool(self.dialog.ui.e65.text()) and self.dialog.e65 != 66666666:
            if not re.match(r"\d+", self.dialog.ui.e65.text()):
                raise ValueError("Date of Petition for Termination (E65) is invalid.")
            if not is_valid_date(self.dialog.e65):
                raise ValueError("Date of Petition for Termination (E65) is invalid.")
            if is_future_date(self.dialog.e65):
                raise ValueError("Date of Petition for Termination (E65) may not be in the future.")
            if is_way_past_date(self.dialog.e65):
                raise ValueError("Date of Petition for Termination (E65) is too far in the past.")
            if self.dialog.e63 == 0:
                raise ValueError("Date of Petition for Termination (E65) should be blank when E63 is not applicable.")

    def validate_e66(self) -> None:
        if self.dialog.e60 in [7777, 9999] and self.dialog.e66:
            raise ValueError("Date of Petition for Termination (E66) should be left blank.")
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
                raise ValueError("Date of Petition for Termination (E66) cannot be after current period.")

    def validate_e67(self) -> None:
        if self.dialog.ui.e67.text():
            if not re.match(r"\d+", self.dialog.ui.e67.text()):
                raise ValueError("Date of Termination (E67) is invalid.")
            if not is_valid_date(self.dialog.e67):
                raise ValueError("Date of Termination (E67) is invalid.")
            if is_future_date(self.dialog.e67):
                raise ValueError("Date of Termination (E67) may not be in the future.")
            if is_way_past_date(self.dialog.e67):
                raise ValueError("Date of Termination (E67) is too far in the past.")
            if self.dialog.e63 == 0:
                raise ValueError("Date of Termination (E67) should be blank when E63 is not applicable.")

    def validate_e68(self) -> None:
        if self.dialog.e60 in [7777, 9999] and self.dialog.e66:
            raise ValueError("Date of Termination (E68) should be left blank.")
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
                raise ValueError("Date of Termination (E68) cannot be after current period.")


class EducationValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH

    def validate_e35(self):
        if self.dialog.e35 not in [0, 1, 2, 3, 4, 5]:
            raise ValueError('School enrollment (E35) is required.')
        return self

    def validate_e36(self):
        if self.dialog.e36 not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
            raise ValueError('Highest level of education (E36) is required.')
        return self

    def validate_e37(self):
        if self.dialog.e37 not in [0, 1]:
            raise ValueError('A selection for Special Education (E37) is required.')
        return self


class TraffickingValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH

    def validate_e106(self):
        if self.dialog.e106 not in [0, 1]:
            raise ValueError("Prior victim of sex trafficking before foster care (E106) is required.")
        return self

    def validate_e107(self):
        if self.dialog.e106 == 1 and self.dialog.e107 not in [0, 1]:
            raise ValueError(
                "Reported to law enforcement (E107) is required if child is victim of sex trafficking (E106).")
        return self

    def validate_e108(self) -> None:
        if self.dialog.ui.e108.text():
            if not re.match(r"\d+", self.dialog.ui.e108.text()):
                raise ValueError("Date Reported (E108) is invalid.")
            if not is_valid_date(self.dialog.e108):
                raise ValueError("Date Reported (E108) is invalid.")
            if is_way_past_date(self.dialog.e108):
                raise ValueError("Date Reported (E108) is too far in the past.")
            if is_future_date(self.dialog.e108):
                raise ValueError("Date Reported (E108) cannot be in the future.")

    def validate_e109(self):
        if self.dialog.e109 not in [0, 1]:
            raise ValueError("Victim of sex trafficking in foster care (E109) is required.")
        return self

    def validate_e110(self):
        if self.dialog.e109 == 1 and self.dialog.e110 not in [0, 1]:
            raise ValueError(
                "Reported to law enforcement (E110) is required when child is victim of sex trafficking (E109).")
        return self

    def validate_e111(self) -> None:
        def e69() -> int | None:
            # Filter out None values before sorting
            valid_removals_2020 = [r for r in self.dialog.removals2020 if r.e69 is not None]
            if valid_removals_2020:
                removals = sorted(valid_removals_2020, key=lambda x: x.e69, reverse=True)
                return removals[0].e69
            valid_removals_1993 = [r for r in self.dialog.removals1993 if r.e69 is not None]
            if valid_removals_1993:
                removals = sorted(valid_removals_1993, key=lambda x: x.e69, reverse=True)
                return removals[0].e69
            return None
        if self.dialog.e110 == 1:
            if not self.dialog.ui.e111.text():
                raise ValueError("Date Reported to Law Enforcement (E111) is required.")
            if not re.match(r"\d+", self.dialog.ui.e111.text()):
                raise ValueError("Date Reported to Law Enforcement (E111) is invalid.")
            if not is_valid_date(self.dialog.e111):
                raise ValueError("Date Reported to Law Enforcement (E111) is invalid.")
            if is_way_past_date(self.dialog.e111):
                raise ValueError("Date Reported to Law Enforcement (E111) is too far in the past.")
            if is_future_date(self.dialog.e111):
                raise ValueError("Date Reported to Law Enforcement (E111) cannot be in the future.")
            _e69 = e69()
            if _e69 is not None and self.dialog.e111 < _e69:
                raise ValueError("Date law enforcement was contacted (E111) must be after date of most recent removal (E69).")


class FinancialValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH

    def validate_e55(self):
        if self.dialog.e55 not in [0, 1]:
            raise ValueError("Foster Care Maintenance Payment (E55) is required.")


class RemovalValidator(OOHBaseValidator, CommonValidators):
    report_type = ReportType.OOH
