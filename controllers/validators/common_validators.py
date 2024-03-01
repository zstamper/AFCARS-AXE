from utils.e1 import is_valid_date, is_future_date, is_way_past_date


class CommonValidators:

    def validate_e4(self) -> None:
        if self.dialog.e4 is None or len(self.dialog.e4) != 12:
            raise ValueError("Child ID (E4) is required and must be exactly 12 characters long.")

    def validate_e5(self) -> None:
        if not is_valid_date(self.dialog.e5):
            raise ValueError("Invalid date of birth (E5)")
        if is_future_date(self.dialog.e5):
            raise ValueError("Date of Birth (E5) may not be in the future.")
        if is_way_past_date(self.dialog.e5):
            raise ValueError("Date of Birth (E5) is too far in the past.")

    def validate_e6(self):
        if self.dialog.e6 not in [1, 2]:
            raise ValueError("Child's gender is required (E6).")

    def validate_e13_e14_e15_e16_e17_e18_e19_e20(self) -> None:
        if all([e != 1 for e in
                [self.dialog.e13, self.dialog.e14, self.dialog.e15, self.dialog.e16, self.dialog.e17, self.dialog.e18,
                 self.dialog.e19, self.dialog.e20]]):
            raise ValueError("At least one race must be selected (E13-E20).")
        if any([e == 1 for e in [self.dialog.e19, self.dialog.e20]]) and any(
                e == 1 for e in
                [self.dialog.e13, self.dialog.e14, self.dialog.e15, self.dialog.e16, self.dialog.e17, self.dialog.e18]):
            raise ValueError(
                "No additional races may be selected (E13-E18) if child is abandoned (E19) or race is declined (E20).")
        if self.dialog.e19 == 1 and self.dialog.e20 == 1:
            raise ValueError("Race may be either Abandoned (E19) or Declined (E20), but not both.")

    def validate_e21(self) -> None:
        if self.dialog.e21 is None:
            raise ValueError("Child's hispanic origin (E21) is required.")
