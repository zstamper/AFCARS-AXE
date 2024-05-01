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

from typing import Optional

from PySide6.QtWidgets import QDialog
from pydantic import ValidationError

from dialogs import error_message_dialog
from model import TribeTable, TribeStateTable, StateTable
from model.models import Tribe


def get_epa_tribes() -> list[Tribe]:
    # results = {}
    # query = TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)
    return [Tribe(id=tribe.id, tribe=tribe.tribe, epa_code=tribe.epa_code,
                  states=[tribestate.state.code for tribestate in tribe.states])
            for tribe in TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)]
    # for tribe in query:
    #     states = ", ".join([state.state.code for state in tribe.states])
    #     results[tribe.id] = f"{tribe.tribe} ({states})"
    # return results


def show_error_dialog(parent: QDialog, ve: Optional[ValidationError] = None, messages: Optional[list[str]] = None,
                      limit: int = 5):
    error_messages = []
    if ve:
        for error in ve.errors():
            if error['type'] == 'missing':
                error_messages.append(f"{error['loc'][0]} is required.")
            else:
                error_messages.append(error['msg'])
    elif messages:
        error_messages = messages
    if len(error_messages) > 1:
        error_messages.insert(0, "Validation checks failed:")
    error_message_dialog(parent, error_messages, limit)
