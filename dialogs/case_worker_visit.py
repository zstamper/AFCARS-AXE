from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class CaseVisitDialog(BaseDialog):
    obj_to_e152_mapping = {0: 1, 1: 2}
    e152_to_obj_mapping = {1: 0, 2: 1}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_case_visit.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self):
        self.setModal(True)
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    @property
    def e151(self) -> int:
        return self._get_int_field(self.ui.e151)

    @e151.setter
    def e151(self, v: int) -> None:
        self._set_int_field(self.ui.e151, v)

    @property
    def e152(self) -> int:
        return self._get_combobox_selection(self.ui.e152, self.e152_to_obj_mapping)

    @e152.setter
    def e152(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e152, v, self.obj_to_e152_mapping)
