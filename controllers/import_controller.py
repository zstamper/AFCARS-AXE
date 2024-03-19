from pathlib import Path
from xml.etree.ElementTree import ParseError

from PySide6.QtWidgets import QFileDialog, QDialog, QMainWindow

import utils.xml_parser
from dialogs import ok_dialog, error_dialog
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
            imported = skipped = []
            tree = utils.xml_parser.parse_file(self.dialog.file_name)
            if self.dialog.report_type == ReportType.A:
                imported, skipped = utils.xml_parser.import_a_tree(tree, self.dialog.file_type)
            if self.dialog.report_type == ReportType.OOH:
                imported, skipped = utils.xml_parser.import_ooh_tree(tree, self.dialog.file_type)
            message = f"**Import Complete**\n\n{len(imported)} rows inserted, {len(skipped)} rows skipped."
            if len(skipped) > 0:
                message += f"\n\nThe following child IDs were skipped due to pre-existing data:\n"
                message += "".join(f"* {id}\n" for id in skipped[:5])
                if len(skipped) > 5:
                    message += "\nPlus {len(skipped)-5} additional IDs"
            title = "Import Finished"
            ok_dialog(self.dialog, title, message)
            return True
        except ParseError:
            error_dialog(self.dialog, "Import Error", "There was an error importing the data. Please check\n"
                                                      "that the import file is of the correct format for the selected report type.")
            return False

    def do_open_file(self):
        home_dir = str(Path.home())
        file_name, _ = QFileDialog.getOpenFileName(self.dialog, caption="Import from...", dir=home_dir,
                                                   filter="XML Files (*.xml);;All Files (*.*)")
        if file_name:
            self.dialog.file_name = file_name
        else:
            self.dialog.file_name = ""
