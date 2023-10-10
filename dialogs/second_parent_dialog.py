from PySide6.QtWidgets import QDialog

from dialogs import BaseDialog
from model import SecondParent


class Parent2Dialog(BaseDialog):
    def __init__(self, *args, relaxed_rules: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.relaxed_rules: bool = relaxed_rules
        self.ui: QDialog
        self.obj = None
        self.ui = self.load_ui('ui_parent2tpr.ui')
        self._wire_ui()
        self.ui.adjustSize()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.id: int | None = None
        self.ooh_id: int | None = None
        self._child_name: str = ""

    def _wire_ui(self):
        self._init_radio(self.ui, 'e64', {'na': 0, 'v': 1, 'i': 2})
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def clear(self):
        super().clear()
        self.child_name = ""

    def populate(self, obj: SecondParent):
        self.obj = obj
        self._from_obj()

    def validate(self) -> bool:
        return True

    def _to_obj(self):
        self.obj.e64 = self._get_radio_button(self.ui.e64)
        self.obj.e66 = self._get_int_field(self.ui.e66)
        self.obj.e68 = self._get_int_field(self.ui.e68)

    def _from_obj(self):
        self._set_radio_button(self.ui.e64, self.obj.e64)
        self._set_int_field(self.ui.e66, self.obj.e66)
        self._set_int_field(self.ui.e68, self.obj.e68)

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self._child_name = v
        if v:
            self.setWindowTitle(f"Putative Parent/Guardian for {self.child_name}")
        else:
            self.setWindowTitle("")