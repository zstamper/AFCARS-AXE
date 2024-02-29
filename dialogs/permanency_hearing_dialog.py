from typing import Optional, Callable

from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model.models import FileType


class PermanencyHearingDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._child_name: str = ""
        self.child = None
        self.file_type: FileType = FileType.PRODUCTION
        self.on_validate: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_close: Optional[Callable] = None
        self.id: int | None = None
        self.removal_id: int | None = None
        self.ui: QWidget = self.load_ui('ui_permanency_hearing.ui')

        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self):
        self.setModal(True)
        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)

    def clear(self, exclude: list[str] = None):
        super().clear()
        self.child_name = ""

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str):
        self._child_name = v
        if v:
            self.setWindowTitle(f"Permanency Hearing : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e150(self) -> int | None:
        return self._get_int_field(self.ui.e150)

    @e150.setter
    def e150(self, v: int) -> None:
        self._set_int_field(self.ui.e150, v)

    def validate_button_clicked(self):
        if self.on_validate:
            self.on_validate()

    def save_button_clicked(self):
        if self.on_save:
            self.on_save()

    def close_button_clicked(self):
        if not self.on_close or self.on_close():
            self.close()
