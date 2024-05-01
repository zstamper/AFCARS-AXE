# Copyright 2024 by ICF International, Inc.
#
# This file is part of AXE, the AFCARS XML Editor.
#
# AXE is free software: you can redistribute it and/or modify it under the terms
# of the GNU Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# AXE is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# AXE. If not, see <https://www.gnu.org/licenses/>.

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QFile
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
