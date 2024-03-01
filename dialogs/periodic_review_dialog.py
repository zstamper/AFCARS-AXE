from typing import Optional, Callable

from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model.models import FileType


class PeriodicReviewDialog(BaseDialog):

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
        self.ui: QWidget = self.load_ui('ui_periodic_review.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self) -> None:
        self.setModal(True)
        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)

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
            self.setWindowTitle(f"Periodic Review : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e149(self) -> int | None:
        return self._get_int_field(self.ui.e149)

    @e149.setter
    def e149(self, v: int) -> None:
        self._set_int_field(self.ui.e149, v)
