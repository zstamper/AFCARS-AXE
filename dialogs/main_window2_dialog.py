from typing import Optional, Literal, Callable

from PySide6.QtWidgets import QMainWindow

from dialogs import BaseMixin
from model.models import ReportType, FileType


class MainWindow2Dialog(QMainWindow, BaseMixin):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui: QMainWindow = self.load_ui("ui_main_window2.ui")
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.setCentralWidget(self.ui)
        self._wire_ui()
        self._fips_codes: list = []
        self._epa_codes: list = []
        self._reporting_periods: list = []
        self._report_types: list = []
        self._file_types: Optional[Literal["production", "test"]] = None
        self.on_go: Optional[Callable] = None
        self.on_export: Optional[Callable] = None
        self.on_import: Optional[Callable] = None
        self.on_close: Optional[Callable] = None
        self.report_types = [e.value for e in ReportType]

    def _wire_ui(self):
        # go button
        # close button
        # main menu options
        self.ui.go_button.clicked.connect(self._on_go_button_clicked)
        self.ui.close_button.clicked.connect(self._on_close_button_clicked)
        self.ui.actionQuit.triggered.connect(self._on_close_button_clicked)
        self.ui.actionExport.triggered.connect(self._on_export_button_clicked)
        self.ui.actionImport.triggered.connect(self._on_import_button_clicked)

    def close(self):
        if self.on_close:
            self.on_close()
        super().close()

    def _on_close_button_clicked(self):
        self.close()

    def _on_go_button_clicked(self, *args, **kwargs):
        if self.on_go:
            self.on_go(*args, **kwargs)

    def _on_export_button_clicked(self):
        if self.on_export:
            self.on_export()

    def _on_import_button_clicked(self):
        if self.on_import:
            self.on_import()

    @property
    def fips_codes(self) -> list:
        return self._fips_codes

    @fips_codes.setter
    def fips_codes(self, v: list) -> None:
        self._fips_codes = v
        self.ui.fips_code.clear()
        self.ui.fips_code.addItems(v)

    @property
    def fips_code(self) -> str | None:
        current_index = self.ui.fips_code.currentIndex()
        if 0 <= current_index < len(self._fips_codes):
            return self._fips_codes[current_index]
        return None

    @fips_code.setter
    def fips_code(self, v: str) -> None:
        try:
            current_index = self._fips_codes.index(v)
            if current_index >= 0:
                self.ui.fips_code.setCurrentIndex(current_index)
        except ValueError:
            pass

    @property
    def epa_codes(self) -> list:
        return self._epa_codes

    @epa_codes.setter
    def epa_codes(self, v: list) -> None:
        self._epa_codes = v
        self.ui.epa_code.clear()
        self.ui.epa_code.addItems(v)

    @property
    def epa_code(self) -> str | None:
        current_index = self.ui.epa_code.currentIndex()
        if 0 <= current_index < len(self._epa_codes):
            return self._epa_codes[current_index]
        return None

    @epa_code.setter
    def epa_code(self, v: str) -> None:
        try:
            current_index = self._epa_codes.index(v)
            if current_index >= 0:
                self.ui.epa_code.setCurrentIndex(current_index)
        except ValueError:
            pass

    @property
    def reporting_periods(self) -> list:
        return self._reporting_periods

    @reporting_periods.setter
    def reporting_periods(self, v: list) -> None:
        self._reporting_periods = v
        self.ui.reporting_period.clear()
        self.ui.reporting_period.addItems(v)

    @property
    def reporting_period(self) -> str | None:
        current_index = self.ui.reporting_period.currentIndex()
        if 0 <= current_index < len(self._reporting_periods):
            period = self._reporting_periods[current_index]
            return f"{period[:4]}03" if period.endswith('A') else f"{period[:4]}09"
        return None

    @reporting_period.setter
    def reporting_period(self, v: str):
        period = f"{v[:4]}A" if v.endswith('03') else f"{v[:4]}B"
        current_index = self._reporting_periods.index(period)
        if current_index >= 0:
            self.ui.reporting_period.setCurrentIndex(current_index)

    @property
    def report_types(self) -> list:
        return self._report_types

    @report_types.setter
    def report_types(self, v: list) -> None:
        self._report_types = v
        self.ui.report_type.clear()
        self.ui.report_type.addItems(v)

    @property
    def report_type(self) -> ReportType | None:
        current_index = self.ui.report_type.currentIndex()
        if 0 <= current_index <= len(self._report_types):
            value = self._report_types[current_index]
            for e in ReportType:
                if e.value == value:
                    return e
        return None

    @report_type.setter
    def report_type(self, v: ReportType) -> None:
        current_index = self._report_types.index(v.value)
        if current_index >= 0:
            self.ui.report_type.setCurrentIndex(current_index)

    @property
    def file_type(self) -> FileType | None:
        if self.ui.file_type_production.isChecked():
            return FileType.PRODUCTION
        if self.ui.file_type_test.isChecked():
            return FileType.TEST
        return None

    @file_type.setter
    def file_type(self, v: FileType | None):
        self.ui.file_type_production.setChecked(v == FileType.PRODUCTION)
        self.ui.file_type_test.setChecked(v == FileType.TEST)
