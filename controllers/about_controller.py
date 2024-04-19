from typing import Optional

from PySide6.QtWidgets import QWidget

from dialogs.about_dialog import AboutDialog


class AboutController:

    def __init__(self, parent: Optional[QWidget] = None):
        self.dialog = AboutDialog(parent)

    def exec(self):
        self.dialog.exec()
