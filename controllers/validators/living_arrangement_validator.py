import datetime
from datetime import date

from dialogs.living_arrangement_dialog import LivingArrangementDialog


class LivingArrangementValidators:

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

    def __init__(self, dialog: LivingArrangementDialog):
        self.dialog: LivingArrangementDialog = dialog

    def validate_e112(self):
        if not self.is_valid_date(self.dialog.e112):
            raise ValueError("Invalid removal date (E112).")

    def validate_e113(self):
        if self.dialog.e113 not in (0, 1):
            raise ValueError("Foster family home (E113) is required.")

    def validate_e120(self):
        if self.dialog.e113 == 1 and self.dialog.e120 is not None:
            print(f"e120=({type(self.dialog.e120)}) {self.dialog.e120}")
            if self.dialog.e120 not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
                raise ValueError("Invalid selection for Living arrangement type (E120).")

    def validate_e114_e118(self):
        fields = [self.dialog.e114, self.dialog.e115, self.dialog.e116, self.dialog.e117, self.dialog.e118,
                  self.dialog.e119]
        if self.dialog.e113 == 1:
            if not any([x == 1 for x in fields]):
                raise ValueError(
                    "At least one of E114, E115, E116, E118 must be checked, or Relationship must be Relative or Kin when Living Arrangement Type (E120) is Foster Family Home.")

    def validate_e121(self):
        if not self.dialog.e121 in (1, 2, 3, 4):
            raise ValueError("Location (E121) is required.")

    def validate_e122(self):
        if self.dialog.e121 in (2, 3):
            if not self.dialog.e122:
                raise ValueError(
                    "Jurisdiction (E122) is required when Living Arrangement (E121) is 'out of state' or 'out of country'.")

    def validate_e123(self):
        if self.dialog.e113 == 0 and self.dialog.e123 is not None:
            raise ValueError(
                "Marital status of the foster parent (E123) does not apply when child is not placed in foster family home (E113/E120)."
            )
        if self.dialog.e113 == 1 and self.dialog.e123 not in (1,2,3,4):
            raise ValueError(
                "Marital status of the foster parent(E123) is required when child is placed in foster family home (E113/E120)."
            )

    def validate_e124(self):
        if self.dialog.e113 == 0 and self.dialog.e124 is not None:
            raise ValueError(
                "Child's relationship to foster parent (E124) does not apply when childs if not placed in foster family home (E113/E120)."
            )
        if (self.dialog.e117 == 1 or self.dialog.e119 == 1) and self.dialog.e124 != 2:
            raise ValueError(
                "Child's relationship (E124) is required and must be 'non-relative' based on living arrangement type (E113, E120).")
        if self.dialog.e117 == 1 and self.dialog.e124 != 1:
            raise ValueError(
                "Child's relationship (E124) should be 'Relative' based on living arrangement type (E113, E120).")
        if self.dialog.e119 == 1 and self.dialog.e124 != 3:
            raise ValueError(
                "Child's relationship (E124) should be 'Kin' based on living arrangement type (E113, E120).")

    def validate_e125(self):
        if self.dialog.e113 == 1:
            if not self.dialog.e125:
                raise ValueError(
                    "First foster parent's year of birth (E125) is required based on living arrangement type (E113, E120).")
            year = datetime.date.today().year
            if not 10 <= year - self.dialog.e125 < 100:
                raise ValueError(
                    "Foster parent's year of birth (E125) is out of allowed range (age must be greater than 10 and less than 100).")

    def validate_e126(self):
        if self.dialog.e113 == 1:
            if self.dialog.e126 not in (0, 1, 9):
                raise ValueError("First foster parent's tribal membership (E126) is required.")

    def validate_e127_e133(self):
        fields = [self.dialog.e127, self.dialog.e128, self.dialog.e129, self.dialog.e130, self.dialog.e131,
                  self.dialog.e132, self.dialog.e133]
        if self.dialog.e113 == 1:
            if all([x == 0 for x in fields]):
                raise ValueError("First foster parent's race is required (E127 - E133).")

    def validate_e134(self):
        if self.dialog.e113 == 1:
            if self.dialog.e134 not in (0, 1, 8, 9):
                raise ValueError(
                    "First foster parent's hispanic or latino origin (E135) is required based on living arrangements (E113, E120).")

    def validate_e135(self):
        if self.dialog.e113 == 1:
            if self.dialog.e135 not in (1, 2):
                raise ValueError(
                    "First foster parent's sex (E135) is required based on living arrangements (E113, E120).")

    def validate_e136(self):
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if not self.dialog.e136:
                raise ValueError(
                    "Second foster parent's year of birth (E136) is required based on living arrangement type (E113, E120, E123).")
            year = datetime.date.today().year
            if not 10 <= year - self.dialog.e125 < 100:
                raise ValueError(
                    "Foster parent's year of birth (E136) is out of allowed range (age must be greater than 10 and less than 100).")

    def validate_e137(self):
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if self.dialog.e137 not in (0, 1, 9):
                raise ValueError("Second foster parent's tribal membership (E137) is required.")

    def validate_e138_e144(self):
        fields = [self.dialog.e138, self.dialog.e139, self.dialog.e140, self.dialog.e141, self.dialog.e142,
                  self.dialog.e143, self.dialog.e144]
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if all([x == 0 for x in fields]):
                raise ValueError("Second foster parent's race is required (E138 - E144).")

    def validate_e145(self):
        if self.dialog.e113 == 1 and self.dialog.e123 in (1, 2):
            if self.dialog.e145 not in (0, 1, 8, 9):
                raise ValueError(
                    "Second foster parent's hispanic or latino origin (E145) is required based on living arrangements (E113, E120).")

    def validate_e146(self):
        if self.dialog.e113 == 1:
            if self.dialog.e146 not in (1, 2) and self.dialog.e123 in (1, 2):
                raise ValueError(
                    "First foster parent's sex (E146) is required based on living arrangements (E113, E120).")


class LivingArrangementValidator:

    def __init__(self, dialog: LivingArrangementDialog):
        self.dialog = dialog
        self.validator = LivingArrangementValidators(dialog)
        self._messages: list[Exception] = []

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

    def messages(self) -> list[str]:
        return [exc.args[0] for exc in self._messages]