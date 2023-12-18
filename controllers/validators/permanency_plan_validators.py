from datetime import date

from dialogs.permency_plan_dialog import PermanencyPlanDialog


class PermanencyPlanBaseValidator:

    def __init__(self, dialog: PermanencyPlanDialog):
        self.dialog = dialog

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


class PermanencyPlanValidators(PermanencyPlanBaseValidator):

    def validate_e147(self):
        if not self.is_valid_date(self.dialog.e147):
            raise ValueError(f"Permanency Plan date (E147) is missing or invalid.")

    def validate_e148(self):
        if self.dialog.e148 not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Invalid selection for Permanency Plan type (E148).")
