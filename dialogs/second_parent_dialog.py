from typing import Optional, Callable

from dialogs import BaseDialog


class Parent2Dialog(BaseDialog):
    def __init__(self, *args, relaxed_rules: bool = False, **kwargs):
        super().__init__(*args, **kwargs)

        self._number: int | None = None
        self.child = None
        self._child_name: str = ""
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
    def number(self) -> int:
        return self._number

    @number.setter
    def number(self, v: int) -> None:
        self._number = v
        self.ui.parent2_tpr_group_box.setTitle(
            f"{'Second' if v == 2 else 'Putative'} Parent/Guardian Modified or Terminated Parental Rights")

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
