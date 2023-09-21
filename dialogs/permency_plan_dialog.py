from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class PermanencyPlanDialog(BaseDialog):
    obj_to_e148_mapping = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    e148_to_obj_mapping = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_permanency_plan.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self):
        self.setModal(True)

        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    @property
    def e147(self) -> int:
        return self._get_int_field(self.ui.e147)

    @e147.setter
    def e147(self, v: int) -> None:
        self._set_int_field(self.ui.e147)

    @property
    def e148(self) -> int:
        return self._get_combobox_selection(self.ui.e148, self.e148_to_obj_mapping)

    @e148.setter
    def e148(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e148, v, self.obj_to_e148_mapping)
