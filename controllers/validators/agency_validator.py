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

from datetime import date

from controllers.validators.abstract_validator import AbstractValidator
from dialogs.database_setup_dialog import DatabaseSetupDialog


class AgencyBaseValidator:

    def __init__(self, dialog: DatabaseSetupDialog):
        self.dialog: DatabaseSetupDialog = dialog

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


class AgencyValidators(AgencyBaseValidator):

    def validate_fips_code_epa_code(self):
        if self.dialog.fips_code is None and self.dialog.epa_code is None:
            raise ValueError("Select either a FIPS code or an EPA Tribal code.")
        if self.dialog.fips_code and self.dialog.epa_code:
            raise ValueError("Select either a FIPS code or an EPA Tribal code, but not both.")


class AgencyValidator(AbstractValidator):

    def __init__(self, dialog: DatabaseSetupDialog):
        self.dialog = dialog
        self.validator = AgencyValidators(dialog)
        self._messages: list[ValueError] = []

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

    def validate_tab(self, tab: int) -> bool:
        return True

    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
