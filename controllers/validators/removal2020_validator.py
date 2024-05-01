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

from dialogs.removal2020_dialog import Removal2020Dialog
from .abstract_validator import AbstractValidator
from .removal2020_validators import RemovalValidator, ExitValidator, PermanencyPlanValidator, Removal2020BaseValidator


class Removal2020Validator(AbstractValidator):
    def __init__(self, dialog: Removal2020Dialog):
        self.dialog = dialog
        self.validators = {
            0: RemovalValidator(dialog),
            1: Removal2020BaseValidator(dialog),
            2: PermanencyPlanValidator(dialog),
            3: Removal2020BaseValidator(dialog),
            4: Removal2020BaseValidator(dialog),
            5: Removal2020BaseValidator(dialog),
            6: ExitValidator(dialog)
        }
        self._messages: list[ValueError] = []

    def validate(self) -> bool:
        return True

    def validate_tab(self, tab_num: int) -> bool:
        if tab_num not in self.validators:
            return True
        results = []
        self._messages = []
        validator = self.validators[tab_num]
        for func in [func for func in dir(validator) if func.startswith('validate_')]:
            try:
                results.append(getattr(validator, func)() or True)
            except Exception as e:
                results.append(False)
                self._messages.append(e)
        return all(results)

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
