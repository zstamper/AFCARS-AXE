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

from controllers.validators.abstract_validator import AbstractValidator
from controllers.validators.permanency_plan_validators import PermanencyPlanValidators
from dialogs.permency_plan_dialog import PermanencyPlanDialog


class PermanencyPlanValidator(AbstractValidator):
    def __init__(self, dialog: PermanencyPlanDialog):
        self.dialog = dialog
        self.validator = PermanencyPlanValidators(self.dialog)
        self._messages: list[ValueError] = []

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

    def validate_tab(self, tab_num: int) -> (bool, list):
        return False

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
