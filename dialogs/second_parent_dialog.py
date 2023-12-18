from typing import Optional, Callable

from PySide6.QtWidgets import QDialog

from dialogs import BaseDialog


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
        self.on_validate_clicked: Optional[Callable] = None

    def _wire_ui(self):
        self._init_radio(self.ui, 'e64', {'na': 0, 'v': 1, 'i': 2})
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.validate_button.clicked.connect(self.do_validate_clicked)

    def clear(self):
        super().clear()
        self.child_name = ""

    def do_validate_clicked(self):
        if self.on_validate_clicked:
            self.on_validate_clicked()

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

    @property
    def e64(self) -> int:
        return self._get_radio_button(self.ui.e64)

    @e64.setter
    def e64(self, v: int) -> None:
        self._set_radio_button(self.ui.e64, v)

    @property
    def e64_text(self) -> str:
        if self.e64 is not None:
            return self.ui.e64.checkedButton().text()
        return ""

    @property
    def e66(self) -> int:
        return self._get_int_field(self.ui.e66)

    @e66.setter
    def e66(self, v: int) -> None:
        self._set_int_field(self.ui.e66, v)

    @property
    def e68(self) -> int:
        return self._get_int_field(self.ui.e68)

    @e68.setter
    def e68(self, v: int) -> None:
        self._set_int_field(self.ui.e68, v)
