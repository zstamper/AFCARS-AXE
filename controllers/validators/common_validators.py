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

from model.models import ReportType
from utils.e1 import is_valid_date, is_future_date, is_way_past_date, afcars_to_date, e2_end_date


class CommonValidators:

    def f(self, field: str) -> str:
        map = {
            'E4': 'A3', 'E5': 'A4', 'E6': 'A5', 'E13': 'A6', 'E14': 'A7', 'E15': 'A8', 'E16': 'A9', 'E17': 'A10',
            'E18': 'A11', 'E19': 'A12', 'E20': 'A13', 'E21': 'A14'
        }
        if self.report_type == ReportType.OOH:
            return field
        return map[field]

    def validate_e4(self) -> None:
        if self.dialog.e4 is None or len(self.dialog.e4) != 12:
            raise ValueError(f"Child ID ({self.f('E4')}) is required and must be exactly 12 characters long.")

    def validate_e5(self) -> None:
        if not re.match(r"\d+", self.dialog.ui.e5.text()):
            raise ValueError(f"Date of Birth ({self.f('E5')}) is invalid.")
        if not is_valid_date(self.dialog.e5):
            raise ValueError(f"Date of Birth ({self.f('E5')}) is invalid.")
        if is_future_date(self.dialog.e5):
            raise ValueError(f"Date of Birth ({self.f('E5')}) may not be in the future.")
        if is_way_past_date(self.dialog.e5):
            raise ValueError(f"Date of Birth ({self.f('E5')}) is too far in the past.")
        if afcars_to_date(self.dialog.e5) > e2_end_date():
            raise ValueError(
                f"Date of Birth ({self.f('E5')}) must be on or before end of reporting period ({self.f('E2')}).")

    def validate_e6(self):
        if self.dialog.e6 not in [1, 2]:
            raise ValueError(f"Child's gender is required ({self.f('E6')}).")

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
