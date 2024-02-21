from copy import deepcopy
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QDialog, QMainWindow, QFileDialog

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
        query = (BaseChildTable
                 .select()
                 .join(ContextTable)
                 .where(BaseChildTable.e1 == self.e1))
        child_data = []
        if self.report_type == ReportType.OOH:
            # Golly, so this was subtle... The filter for the context table records was originally in the query
            # above. But it so happens that with PeeWee, when accessing foreign table, you're given an unfiltered
            # list of records. Therefore, we have to filter them here.
            child_data = [(row.to_model(), deepcopy(context.data)) for row in query for context in row.contexts if
                          context.file_type == self.file_type and context.data.ooh]
        elif self.report_type == ReportType.A:
            child_data = [(row.to_model(), deepcopy(context.data)) for row in query for context in row.contexts if
                          context.file_type == self.file_type and context.data.a]
        return child_data
