from typing import Optional, Callable

from PySide6.QtWidgets import QDialog

from dialogs import BaseDialog
from model.models import ReportType, BaseChild, Child, FileType


class ImportDialog(BaseDialog):

    def __init__(self, parent: QDialog = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = self.load_ui('ui_import_dialog.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.on_accept: Optional[Callable] = None
        self.on_reject: Optional[Callable] = None
        self.on_open_file: Optional[Callable] = None

    def _wire_ui(self):
        self.ui.form_action.accepted.connect(self.accept)
        self.ui.form_action.rejected.connect(self.reject)
        self.ui.select_file.clicked.connect(self.do_select_file)

    def do_select_file(self):
        if self.on_open_file:
            self.on_open_file()

    @property
    def file_name(self) -> str:
        return self.ui.file_name.text()

    @file_name.setter
    def file_name(self, v: str) -> None:
        self.ui.file_name.setText(v)


    @property
    def file_type(self) -> FileType | None:
        if self.ui.file_type_production.isChecked():
            return FileType.PRODUCTION
        if self.ui.file_type_testing.isChecked():
            return FileType.TEST
        return None

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        if v == FileType.PRODUCTION:
            self.ui.file_type_production.setChecked(True)
        if v == FileType.TEST:
            self.ui.file_type_testing.setChecked(True)

    @property
    def report_type(self) -> ReportType:
        if self.ui.report_type_a.isChecked():
            return ReportType.A
        if self.ui.report_type_ooh.isChecked():
            return ReportType.OOH

    @report_type.setter
    def report_type(self, v: ReportType) -> None:
        if v == ReportType.A:
            self.ui.report_type_a.setChecked(True)
        if v == ReportType.OOH:
            self.ui.report_type_ooh.setChecked(True)