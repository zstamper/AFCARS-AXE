from typing import Optional, Callable

from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog


class CaseVisitDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_case_visit.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.id: int | None = None
        self.removal_id: int | None = None
        self._child_name: str = ""
        self.on_validate: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_close: Optional[Callable] = None

    def clear(self, exclude: list[str] = None) -> None:
        super().clear()
        self.child_name = ""

    def _wire_ui(self) -> None:
        self.setModal(True)
        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)

    def validate_button_clicked(self):
        self.on_validate() if self.on_validate else None

    def save_button_clicked(self):
        self.on_save() if self.on_save else None

    def close_button_clicked(self):
        if self.on_close and not self.on_close():
            return
        self.close()

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
    def e151(self) -> int | None:
        return self._get_int_field(self.ui.e151)

    @e151.setter
    def e151(self, v: int) -> None:
        self._set_int_field(self.ui.e151, v)

    @property
    def e152(self) -> int | None:
        return self._get_combobox_selection(self.ui.e152, 1)

    @e152.setter
    def e152(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e152, v, -1)
