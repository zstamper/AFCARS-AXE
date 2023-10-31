from pathlib import Path
from typing import Any, Optional

from PySide6.QtCore import QFile, QAbstractTableModel, Qt, QModelIndex
from PySide6.QtGui import QAction
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMainWindow, QToolButton, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog

from model import Child, ChildTable, Export
from utils import XMLExporter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = None
        self.setup_ui()
        self._children = []
        self.tribes: list[int] = []
        self.epa_tribes: dict = {}
        self.setWindowTitle('AFCARS Database Tool')
        self.context_id = None

    def setup_ui(self) -> None:
        loader = QUiLoader()
        main_window_file = QFile(Path(__file__).resolve().parent.parent / 'ui' / 'mainwindow.ui')
        main_window_file.open(QFile.ReadOnly)
        self.ui = loader.load(main_window_file)
        main_window_file.close()

        self.setCentralWidget(self.ui)
        self.resize(self.ui.baseSize())

        self.ui.findChild(QAction, 'actionOpen').triggered.connect(self.open_dialog)
        self.ui.findChild(QAction, 'actionQuit').triggered.connect(self.close)
        self.ui.findChild(QToolButton, 'importButton').clicked.connect(self.open_dialog)
        self.ui.findChild(QPushButton, 'add_child').clicked.connect(self.add_ooh)
        self.ui.findChild(QTableWidget, 'child_table').doubleClicked.connect(self.edit_ooh)

        self.ui.findChild(QToolButton, 'export_button').clicked.connect(self.do_export)

    def add_a(self, child: Optional[Child] = None) -> None:
        from controllers import AController
        from .a_dialog import ADialog
        a_dialog = ADialog(self)
        a_dialog.child_name = ""
        controller = AController(a_dialog, self.context_id)
        data: Child | None = controller.add(child)
        if data is not None:
            self._children.append(data)
            self.__update_child_row(data)
            ChildTable.persist_model(data)

    def edit_a(self) -> None:
        from controllers import AController
        from .a_dialog import ADialog
        current_row = self.ui.child_table.currentRow()
        if current_row >= 0:
            data = self._children[current_row]
            dialog = ADialog(self)
            dialog.child_name = f"{data.last_name}, {data.first_name}"
            controller = AController(dialog, self.context_id)
            controller.edit(data)
            self.__update_child_row(current_row, data)
            ChildTable.persist_model(data)

    # def add_a_button_clicked(self) -> None:
    #     row = self.sender().property('row')
    #     self.ui.child_table.setCurrentCell(row, 6)
    #     self.add_a(self._children[row])

    def edit_a_button_clicked(self) -> None:
        row = self.sender().property('row')
        self.ui.child_table.setCurrentCell(row, 6)
        self.edit_a()

    def delete_a(self) -> None:
        current_row = self.ui.child_table.currentRow()
        if 0 <= current_row < len(self._children):
            del self._children[current_row]
            self.ui.child_table.removeRow(current_row)

    def add_ooh(self, child: Optional[Child] = None) -> None:
        from controllers import OOHController
        from .ooh_dialog import OOHDialog
        ooh_dialog = OOHDialog(self)
        ooh_dialog.child_name = ""
        controller = OOHController(ooh_dialog, self.context_id, self.epa_tribes)
        data: Child | None = controller.add(child)
        if data is not None:
            self._children.append(data)
            self.__add_child_row(data)
            ChildTable.persist_model(data)

    def edit_ooh(self) -> None:
        from controllers import OOHController
        from .ooh_dialog import OOHDialog
        current_row = self.ui.child_table.currentRow()
        if current_row >= 0:
            data = self._children[current_row]
            dialog = OOHDialog(self)
            dialog.child_name = f"{data.last_name}, {data.first_name}"
            controller = OOHController(dialog, self.context_id, self.epa_tribes)
            controller.edit(data)
            self.__update_child_row(current_row, data)
            ChildTable.persist_model(data)

    def add_ooh_button_clicked(self) -> None:
        row = self.sender().property('row')
        self.ui.child_table.setCurrentCell(row, 5)
        self.add_ooh(self._children[row])

    def edit_ooh_button_clicked(self) -> None:
        row = self.sender().property('row')
        self.ui.child_table.setCurrentCell(row, 5)
        self.edit_ooh()

    def delete_ooh(self) -> None:
        current_row = self.ui.child_table.currentRow()
        if 0 <= current_row < len(self._children):
            del self._children[current_row]
            self.ui.child_table.removeRow(current_row)

    def __add_child_row(self, data: Child) -> None:
        row: int = self.ui.child_table.rowCount()
        self.ui.child_table.insertRow(row)
        self.__update_child_row(row, data)

    def __update_child_row(self, row: int, data: Child) -> None:
        self.ui.child_table.setItem(row, 0, QTableWidgetItem(data.e4))
        self.ui.child_table.setItem(row, 1, QTableWidgetItem(data.last_name))
        self.ui.child_table.setItem(row, 2, QTableWidgetItem(data.first_name))
        self.ui.child_table.setItem(row, 3, QTableWidgetItem('M' if data.e6 == 1 else 'F' if data.e6 == 2 else ''))
        self.ui.child_table.setItem(row, 4, QTableWidgetItem(str(data.e5)))
        button = QPushButton('Add' if data.ooh is None else 'Edit')
        button.setProperty('row', row)
        button.clicked.connect(self.edit_ooh_button_clicked if data.ooh is None else self.edit_ooh_button_clicked)
        self.ui.child_table.setCellWidget(row, 5, button)
        button = QPushButton('Add' if data.a is None else 'Edit')
        button.setProperty('row', row)
        button.clicked.connect(self.edit_a_button_clicked)
        self.ui.child_table.setCellWidget(row, 6, button)

    def refresh_children(self, query) -> None:
        for row in query:
            child: Child = row.to_model()
            self._children.append(child)
            self.__add_child_row(child)
            # print(f"{child.child_id}: {child.last_name} {child.first_name}")

    def open_dialog(self) -> None:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setWindowTitle('Open Database')
        file_dialog.setDefaultSuffix('.db')
        file_dialog.setNameFilter('AFCARS Databases (*.db)')
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            # print(f"Selected files: {selected_files}")

    def do_export(self):
        from controllers import GenericController
        from .export_dialog import ExportDialog
        export_dialog = ExportDialog(self)
        controller = GenericController(export_dialog, Export)
        export = controller.add()
        if export:
            exporter = XMLExporter(export.file_name)
            exporter.export(export.e2)
