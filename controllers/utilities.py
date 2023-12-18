from typing import Optional

from PySide6.QtWidgets import QDialog
from pydantic import ValidationError

from dialogs import error_message_dialog
from model import TribeTable, TribeStateTable, StateTable
from model.models import Tribe


def get_epa_tribes() -> list[Tribe]:
    results = {}
    query = TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)
    return [Tribe(id=tribe.id, tribe=tribe.tribe, epa_code=tribe.epa_code, states=[tribestate.state.code for tribestate in tribe.states])
            for tribe in TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)]
    # for tribe in query:
    #     states = ", ".join([state.state.code for state in tribe.states])
    #     results[tribe.id] = f"{tribe.tribe} ({states})"
    # return results


def show_error_dialog(parent: QDialog, ve: Optional[ValidationError] = None, messages: Optional[list[str]] = None):
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
    error_message_dialog(parent, error_messages)
