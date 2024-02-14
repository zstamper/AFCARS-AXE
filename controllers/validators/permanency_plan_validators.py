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
            d = date(year=year, month=month, day=day)
            today = date.today()
            min_d = date(year=today.year - 100, month=today.month, day=today.day)
            assert d >= min_d
            return True
        except ValueError:
            return False
        except AssertionError:
            return False

    @staticmethod
    def is_future_date(d: int) -> bool:
        year = d // 10000
        month = (d - (d // 10000) * 10000) // 100
        day = d - (d//100)*100
        d = date(year=year, month=month, day=day)
        return d > date.today()


class PermanencyPlanValidators(PermanencyPlanBaseValidator):

    def validate_e147(self):
        if not self.is_valid_date(self.dialog.e147):
            raise ValueError(f"Permanency Plan date (E147) is missing or invalid.")
        if self.is_future_date(self.dialog.e147):
            raise ValueError("Permanency Plan Date (E147) cannot be in the future.")

    def validate_e148(self):
        if self.dialog.e148 not in [1, 2, 3, 4, 5]:
            raise ValueError(f"Invalid selection for Permanency Plan type (E148).")
