import traceback
from copy import deepcopy
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QDialog, QMainWindow, QFileDialog, QMessageBox

import utils
from dialogs.export_dialog import ExportDialog
from model import BaseChildTable, ContextTable
from model.models import ReportType, ReportingPeriod, FileType, Child
from utils.export import export_xml


class ExportController:

    def __init__(self, parent: QDialog | QMainWindow):
        self.dialog: ExportDialog = ExportDialog(parent)
        self.e1: str = ""
        self.e2: Optional[ReportingPeriod] = None
        self.report_type: Optional[ReportType] = None
        self.file_type: Optional[FileType] = None
        self.dialog.on_accept = self.do_accept

    def show(self):
        self.dialog.report_type = self.report_type
        self.dialog.child_data = self.get_child_data()
        self.dialog.exec_()

    def do_accept(self) -> bool:
        home_dir = str(Path.home())
        file_name, _ = QFileDialog.getSaveFileName(self.dialog, caption="Save to...", dir=home_dir,
                                                   filter="XML Files (*.xml);;All Files (*.*)")
        if file_name:
            export_xml(Path(file_name), self.e1, self.e2, self.report_type, self.dialog.selected_children)
            return True
        return False

    def get_child_data(self) -> list[Child]:
        query = (ContextTable
                 .select()
                 .join(BaseChildTable)
                 .where(ContextTable.e2 == self.e2, BaseChildTable.e1 == self.e1))

        child_data = []
        if self.report_type == ReportType.OOH:
            # Golly, so this was subtle... The filter for the context table records was originally in the query
            # above. But it so happens that with PeeWee, when accessing foreign table, you're given an unfiltered
            # list of child records. Therefore, we have to filter them here.
            child_data = [(row.base_child.to_model(), row.data) for row in query if hasattr(row.data, 'ooh') and row.data.ooh]
        elif self.report_type == ReportType.A:
            child_data = [(row.base_child.to_model(), row.data) for row in query if hasattr(row.data, 'a') and row.data.a]
        return child_data
