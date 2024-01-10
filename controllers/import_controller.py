from pathlib import Path
from xml.etree.ElementTree import ParseError

from PySide6.QtWidgets import QFileDialog, QDialog, QMainWindow

import utils.xml_parser
from dialogs.import_dialog import ImportDialog
from model.models import FileType, ReportType


class ImportController:

    def __init__(self, parent: QDialog | QMainWindow):
        self.dialog = ImportDialog(parent)
        self.file_type: FileType = FileType.PRODUCTION
        self.file_name: str = ""
        self.dialog.on_accept = self.do_accept
        self.dialog.on_open_file = self.do_open_file

    def show(self):
        self.dialog.file_type = FileType.PRODUCTION
        self.dialog.report_type = ReportType.OOH
        self.dialog.file_name = ""
        self.dialog.exec()

    def do_accept(self):
        if not self.dialog.file_name:
            return False
        try:
            tree = utils.xml_parser.parse_file(self.dialog.file_name)
            if self.dialog.report_type == ReportType.A:
                utils.xml_parser.import_a_tree(tree, self.dialog.file_type)
            if self.dialog.report_type == ReportType.OOH:
                utils.xml_parser.import_ooh_tree(tree, self.dialog.file_type)
            return True
        except ParseError:
            return False

    def do_open_file(self):
        home_dir = str(Path.home())
        file_name, _ = QFileDialog.getOpenFileName(self.dialog, caption="Save to...", dir=home_dir,
                                                   filter="XML Files (*.xml);;All Files (*.*)")
        if file_name:
            self.dialog.file_name = file_name
        else:
            self.dialog.file_name = ""
