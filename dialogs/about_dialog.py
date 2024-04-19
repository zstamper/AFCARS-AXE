import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import Qt, QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QWidget, QMainWindow


class AboutDialog(QDialog):

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui: QWidget = self.load_ui('ui_about.ui')
        self.wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    @staticmethod
    def load_ui(file_name: str) -> QMainWindow | QDialog | QWidget:
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = Path(__file__).resolve().parent.parent
        ui_file_path = Path(bundle_dir) / 'ui' / file_name
        loader = QUiLoader()
        ui_file = QFile(ui_file_path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file)
        ui_file.close()
        return ui

    def wire_ui(self):
        if getattr(sys, 'frozen', False):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = Path(__file__).resolve().parent.parent
        with open(Path(bundle_dir) / 'assets' / 'about.html') as f:
            html = f.read()
        self.ui.about_text.setHtml(html)
        self.ui.ok_button.clicked.connect(self.close)
