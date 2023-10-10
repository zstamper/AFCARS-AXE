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
        self.id: int | None = None
        self.removal_id: int | None = None
        self._child_name: str = ""

    def clear(self):
        super().clear()
        self.child_name = ""

    def _wire_ui(self):
        self.setModal(True)
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str):
        self._child_name = v
        if v:
            self.setWindowTitle(f"Case Worker Visit : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e151(self) -> int:
        return self._get_int_field(self.ui.e151)

    @e151.setter
    def e151(self, v: int) -> None:
        self._set_int_field(self.ui.e151, v)

    @property
    def e152(self) -> int:
        return self._get_combobox_selection(self.ui.e152, 1)

    @e152.setter
    def e152(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e152, v, -1)
