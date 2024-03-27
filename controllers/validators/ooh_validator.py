from dialogs.ooh_dialog import OOHDialog
from model.models import ReportType
from .abstract_validator import AbstractValidator
from .ooh_validators import DemographicsValidator, ICWAValidator, HealthValidator, EducationValidator, \
    ParentGuardianValidator, FinancialValidator, TraffickingValidator, RemovalValidator


class OOHValidator(AbstractValidator):
    report_type = ReportType.OOH

    def __init__(self, dialog: OOHDialog):
        self.dialog = dialog
        self.validators = {
            0: DemographicsValidator(dialog),
            1: ICWAValidator(dialog),
            2: HealthValidator(dialog),
            3: EducationValidator(dialog),
            4: ParentGuardianValidator(dialog),
            5: FinancialValidator(dialog),
            6: TraffickingValidator(dialog),
            7: RemovalValidator(dialog)
        }
        self._messages: list[ValueError] = []

    def validate(self) -> bool:
        return False

    def validate_tab(self, tab_num: int) -> (bool, list):
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
