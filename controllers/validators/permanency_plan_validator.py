from controllers.validators.abstract_validator import AbstractValidator
from controllers.validators.permanency_plan_validators import PermanencyPlanValidators
from dialogs.permency_plan_dialog import PermanencyPlanDialog


class PermanencyPlanValidator(AbstractValidator):
    def __init__(self, dialog: PermanencyPlanDialog):
        self.dialog = dialog
        self.validator = PermanencyPlanValidators(self.dialog)
        self._messages: list[ValueError] = []

    @property
    def parent_data(self):
        return self.validator.parent_data

    @parent_data.setter
    def parent_data(self, v):
        self.validator.parent_data = v

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

    def validate_tab(self, tab_num: int) -> (bool, list):
        return False

    @property
    def messages(self) -> list:
        return [ve.args[0] for ve in self._messages]
