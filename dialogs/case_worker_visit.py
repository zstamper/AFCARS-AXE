from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model import CaseVisit


class CaseVisitDialog(BaseDialog):
    obj_to_e152_mapping = {0: 1, 1: 2}
    e152_to_obj_mapping = {1: 0, 2: 1}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_case_visit.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.obj: CaseVisit | None = None

    def populate(self, obj: CaseVisit):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False

    def validate(self):
        self._validate()
        return len(self.errors) == 0

    def _wire_ui(self):
        self.setModal(True)
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    def _validate(self):
        return None

    def _from_obj(self):
        ui = self.ui
        obj = self.obj
        self._set_text_field(ui.e151, obj.e151)
        self._set_combobox_selection(ui.e152, obj.e152, self.obj_to_e152_mapping)

    def _to_obj(self):
        ui = self.ui
        obj = self.obj

        obj.e151 = ui.e151.text()
        obj.e152 = self._get_combobox_selection(ui.e152, self.e152_to_obj_mapping)
