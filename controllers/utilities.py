from PySide6.QtWidgets import QDialog
from pydantic import ValidationError

from dialogs import error_message_dialog


def show_error_dialog(parent: QDialog, ve: ValidationError):
    error_messages = []
    for error in ve.errors():
        if error['type'] == 'missing':
            error_messages.append(f"{error['loc'][0]} is required.")
        else:
            error_messages.append(error['msg'])
    if len(error_messages) > 1:
        error_messages.insert(0, "Validation checks failed:")
    error_message_dialog(parent, error_messages)
