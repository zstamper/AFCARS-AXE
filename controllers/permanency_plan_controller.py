from typing import Any

from PySide6.QtWidgets import QDialog
from pydantic import ValidationError

from controllers.utilities import show_error_dialog
from controllers.validators.permanency_plan_validator import PermanencyPlanValidator
from dialogs.permency_plan_dialog import PermanencyPlanDialog
from model.models import PermanencyPlan


class PermanencyPlanController:

    def __init__(self, parent, child_name: str):
        self.dialog = PermanencyPlanDialog(parent)
        self.dialog.child_name = child_name
        self.dialog.on_accept = self.do_accept
        self.new_data = None
        self.validator = PermanencyPlanValidator(self.dialog)
        self.dialog.on_validate_clicked = self.do_validate_clicked

    def add(self) -> Any:
        self.dialog.clear()
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            return self.new_data
        return None

    def edit(self, data: PermanencyPlan) -> None:
        self.dialog.clear()
        data.scatter(self.dialog)
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            data.gather(self.dialog)
        else:
            # put the data back in to the dialog so that further queries of the form don't get confused by the form
            # state not matching the data state
            data.scatter(self.dialog)

    def do_accept(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate_clicked():
                    return False
            self.new_data = PermanencyPlan.crib(self.dialog)
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def do_validate_clicked(self) -> bool:
        tab_ok = self.validator.validate()
        if not tab_ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)
        return tab_ok
