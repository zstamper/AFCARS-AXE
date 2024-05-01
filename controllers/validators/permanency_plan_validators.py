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

from dialogs.permency_plan_dialog import PermanencyPlanDialog
from utils.e1 import is_future_date, is_valid_date


class PermanencyPlanBaseValidator:

    def __init__(self, dialog: PermanencyPlanDialog):
        self.dialog = dialog
        self.parent_data = None


class PermanencyPlanValidators(PermanencyPlanBaseValidator):

    def validate_e147(self):
        if not self.dialog.ui.e147.text():
            raise ValueError("Permanency Plan Date (E147) is required.")
        if not re.match(r"\d+", self.dialog.ui.e147.text()):
            raise ValueError("Permanency Plan Date (E147) is invalid.")
        if not is_valid_date(self.dialog.e147):
            raise ValueError(f"Permanency Plan date (E147) is invalid.")
        if is_future_date(self.dialog.e147):
            raise ValueError("Permanency Plan Date (E147) cannot be in the future.")
        if self.dialog.e147 < self.parent_data.e69:
            raise ValueError("Permanency Plan Date (E147) cannot be before Removal Date (E69).")

    def validate_e148(self):
        if self.dialog.e148 not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Permanency Plan type (E148) is invalid.")
