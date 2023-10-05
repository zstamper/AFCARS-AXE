# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the widgets/gallery example from Qt v5.15"""
try:
    import os
    import sys
    from pathlib import Path

    from PySide6.QtCore import QFile
    from PySide6.QtGui import QAction
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton, QTableWidgetItem, \
        QTableWidget

    import model
    from controllers import GenericController, OOHController
    from controllers.a_controller import AController
    from dialogs import BasePath
    from dialogs.a_dialog import ADialog

    from dialogs.ooh_dialog import OOHDialog
    from model import TribeTable, OOHRecord, Child, Context, StateTable, TribeStateTable


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = None
            self.setup_ui()
            self._children = []
            self.setWindowTitle('AFCARS Database Tool')
            self.context_id = 1  # FIXME: need to fetch context ID from the Context table

        def setup_ui(self):
            loader = QUiLoader()
            main_window_file = QFile(Path(__file__).resolve().parent / 'ui' / 'mainwindow.ui')
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

        def add_a(self):
            a_dialog = ADialog(self)
            controller = AController(a_dialog, self.context_id)
            data: Child = controller.add()
            if data is not None:
                self._children.append(data)
                self.__add_child_row(data)

        def edit_a(self):
            current_row = self.ui.child_table.currentRow()
            if current_row >= 0:
                data = self._children[current_row]
                dialog = ADialog(self)
                controller = AController(dialog, self.context_id)
                controller.edit(data)
                self.__update_child_row(current_row, data)

        def edit_a_button_clicked(self):
            row = self.sender().property('row')
            self.ui.child_table.setCurrentCell(row, 6)
            self.edit_a()

        def delete_a(self):
            current_row = self.ui.child_table.currentRow()
            if 0 <= current_row < len(self._children):
                del self._children[current_row]
                self.ui.child_table.removeRow(current_row)

        def add_ooh(self):
            ooh_dialog = OOHDialog(self)
            controller = OOHController(ooh_dialog, self.context_id)
            data: Child = controller.add()
            if data is not None:
                self._children.append(data)
                self.__add_child_row(data)

        def edit_ooh(self):
            current_row = self.ui.child_table.currentRow()
            if current_row >= 0:
                data = self._children[current_row]
                dialog = OOHDialog(self)
                dialog.setWindowTitle(f"{data.last_name}, {data.first_name}")
                controller = OOHController(dialog, self.context_id)
                controller.edit(data)
                self.__update_child_row(current_row, data)

        def edit_ooh_button_clicked(self):
            row = self.sender().property('row')
            self.ui.child_table.setCurrentCell(row, 5)
            self.edit_ooh()

        def delete_ooh(self):
            current_row = self.ui.child_table.currentRow()
            if 0 <= current_row < len(self._children):
                del self._children[current_row]
                self.ui.child_table.removeRow(current_row)

        def __add_child_row(self, data: Child):
            row: int = self.ui.child_table.rowCount()
            self.ui.child_table.insertRow(row)
            self.__update_child_row(row, data)

        def __update_child_row(self, row: int, data: Child):
            self.ui.child_table.setItem(row, 0, QTableWidgetItem(data.e4))
            self.ui.child_table.setItem(row, 1, QTableWidgetItem(data.last_name))
            self.ui.child_table.setItem(row, 2, QTableWidgetItem(data.first_name))
            self.ui.child_table.setItem(row, 3, QTableWidgetItem('M' if data.e6 == 1 else 'F' if data.e6 == 2 else ''))
            self.ui.child_table.setItem(row, 4, QTableWidgetItem(str(data.e5)))
            button = QPushButton('Add' if data.ooh is None else 'Edit')
            button.clicked.connect(self.edit_ooh_button_clicked)
            button.setProperty('row', row)
            self.ui.child_table.setCellWidget(row, 5, button)
            button = QPushButton('Add' if data.a is None else 'Edit')
            button.clicked.connect(self.edit_a_button_clicked)
            self.ui.child_table.setCellWidget(row, 6, button)
            button.setProperty('row', row)

        def refresh_children(self):
            for child in self._children:
                self.__add_child_row(child)

        def open_dialog(self):
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setWindowTitle('Open Database')
            file_dialog.setDefaultSuffix('.db')
            file_dialog.setNameFilter('AFCARS Databases (*.db)')
            if file_dialog.exec():
                selected_files = file_dialog.selectedFiles()
                print(f"Selected files: {selected_files}")


    def inject_demo_data(dialog):
        dialog._children.append(
            Child(id=None, context_id=1, last_name="Rubble", first_name="Barney", e4="000000000000", e5=1, e6=20050606,
                  e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None, e20=None,
                  e21=None, ooh=None, a=None))


    def main():
        try:
            if getattr(sys, 'frozen', False):
                database_path = Path.home() / 'default.db'
            else:
                database_path = 'default.db'
            print(f"opening database {database_path}...")
            model.open_database(str(database_path))
            print("database open, creating tables...")
            model.create_tables()
            print("tables created, instantiating application...")
            app = QApplication()
            print("application instantiated, setting application name...")
            app.setApplicationName('ADT')
            print("application name set, setting application display name...")
            app.setApplicationDisplayName('ADT')
            print("application display name set, setting desktop file name...")
            app.setDesktopFileName('ADT')
            print("desktop file name set, getting bundle_dir...")
            if getattr(sys, 'frozen', False):
                # we are running in a bundle
                bundle_dir = sys._MEIPASS
            else:
                # we are running in a normal Python environment
                bundle_dir = os.path.dirname(os.path.abspath(__file__))
            print(f"{bundle_dir=}, opening style sheet...")
            with open(Path(bundle_dir) / 'ui' / 'style.qss', 'r') as f:
                style_sheet = f.read()
            app.setStyleSheet(style_sheet)
            print("style sheet set, instantiating main_window...")
            main_window = MainWindow()
            print("main_window instantiated, injecting demo data...")
            inject_demo_data(main_window)
            print("demo data injected, refreshing the form contents...")
            main_window.refresh_children()
            print("form contents refreshed, showing main window...")
            main_window.show()
            print("main_window shown, entering event loop...")
            sys.exit(app.exec())
        except Exception as e:
            print(e)


    if __name__ == '__main__':
        main()

except Exception as e:
    with open('./stderr.txt', 'w') as stderr:
        print(f"{e.__class__.__name__}({e.args})", file=stderr)