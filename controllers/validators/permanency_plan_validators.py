from datetime import date

from dialogs.permency_plan_dialog import PermanencyPlanDialog
from utils.e1 import is_future_date, is_valid_date


class PermanencyPlanBaseValidator:

    def __init__(self, dialog: PermanencyPlanDialog):
        self.dialog = dialog
        self.parent_data = None


class PermanencyPlanValidators(PermanencyPlanBaseValidator):

    def validate_e147(self):
        if not is_valid_date(self.dialog.e147):
            raise ValueError(f"Permanency Plan date (E147) is missing or invalid.")
        if is_future_date(self.dialog.e147):
            raise ValueError("Permanency Plan Date (E147) cannot be in the future.")
        if self.dialog.e147 < self.parent_data.e69:
            raise ValueError("Permanency Plan Date (E147) cannot be before Removal Date (E69).")

    def validate_e148(self):
        if self.dialog.e148 not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Invalid selection for Permanency Plan type (E148).")
