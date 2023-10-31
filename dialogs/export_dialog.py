from pathlib import Path

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QFileDialog

from dialogs import BaseDialog


class ExportDialog(BaseDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = self.load_ui('ui_export_dialog.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    def _wire_ui(self):
        self.setModal(True)
        self.setWindowTitle('NCWDMS XML Export')
        ui = self.ui

        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)
        ui.select_button.clicked.connect(self.select_file)
        ui.e2.setValidator(QRegularExpressionValidator(QRegularExpression(r'20[0-9]{2}(03|09)')))

    def select_file(self):
        home_dir = str(Path.home())
        self.file_name, _ = QFileDialog.getSaveFileName(self, caption="Export to...", dir=home_dir, filter="XML Files (*.xml);;All Files (*.*)")


    @property
    def e2(self) -> int:
        return self._get_int_field(self.ui.e2)

    @e2.setter
    def e2(self, v: int) -> None:
        self._set_int_field(self.ui.e2, v)

    @property
    def file_name(self) -> str:
        return self._get_text_field(self.ui.file_name)

    @file_name.setter
    def file_name(self, v: str) -> None:
        self._set_text_field(self.ui.file_name, v)
