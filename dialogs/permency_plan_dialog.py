from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model import PermanencyPlan


class PermanencyPlanDialog(BaseDialog):
    obj_to_e148_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    e148_to_obj_mapping = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_permanency_plan.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.obj: PermanencyPlan | None = None

    def populate(self, obj: PermanencyPlan):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False

    def validate(self):
        self._validate()
        return len(self.errors) == 0

    def _validate(self):
        return None

    def _wire_ui(self):
        self.setModal(True)

        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    def _from_obj(self):
        self._set_text_field(self.ui.e147, self.obj.e147)
        self._set_combobox_selection(self.ui.e148, self.obj.e148, self.obj_to_e148_mapping)

    def _to_obj(self):
        self.obj.e147 = self.ui.e147.text()
        self.obj.e148 = self._get_combobox_selection(self.ui.e148, self.e148_to_obj_mapping)
