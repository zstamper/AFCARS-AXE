from typing import Optional, Callable

from dialogs import BaseDialog
from model.models import ChildName


class Parent2Dialog(BaseDialog):
    def __init__(self, *args, relaxed_rules: bool = False, **kwargs):
        super().__init__(*args, **kwargs)

        self._number: int | None = None
        self.child = None
        self.e60 = None
        self._child_name: ChildName = ChildName()
        self.on_validate: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_close: Optional[Callable] = None

        self.id: int | None = None
        self.ooh_id: int | None = None
        self.relaxed_rules: bool = relaxed_rules
        self.ui = self.load_ui('ui_parent2tpr.ui')

        self._wire_ui()
        self.ui.adjustSize()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self):
        self._init_radio(self.ui, 'e64', {'na': 0, 'v': 1, 'i': 2})
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)
        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.e64.buttonClicked.connect(self._e64_button_clicked)

    def clear(self, exclude: list[str] = None):
        super().clear()
        self.child_name = ""

    def validate_button_clicked(self):
        if self.on_validate:
            self.on_validate()

    def save_button_clicked(self):
        if self.on_save:
            self.on_save()

    def close_button_clicked(self):
        if not self.on_close or self.on_close():
            self.close()

    def _e64_button_clicked(self):
        enabled = self.e64 in [1,2]
        self.ui.e66.setEnabled(enabled)
        self.ui.e66_label.setEnabled(enabled)
        self.ui.e68.setEnabled(enabled)
        self.ui.e68_label.setEnabled(enabled)
        if not enabled:
            self.e66 = None
            self.e68 = None

    @property
    def child_name(self) -> ChildName:
        return self._child_name

    @child_name.setter
    def child_name(self, v: ChildName) -> None:
        self._child_name = v
        self.setWindowTitle(f"Putative Parent: {str(self._child_name)}")

    @property
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, v: int) -> None:
        self._number = v

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
