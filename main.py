# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the widgets/gallery example from Qt v5.15"""
import traceback

import peewee

from dialogs.database_setup_dialog import DatabaseSetupDialog
from model.models import Agency

try:
    import os
    import sys
    from pathlib import Path

    from PySide6.QtCore import QFile, QCoreApplication
    from PySide6.QtGui import QAction, QPixmap, QColor
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton, QTableWidgetItem, \
        QTableWidget, QSplashScreen

    import model
    from controllers import GenericController, OOHController, AController
    from dialogs import MainWindow
    from dialogs.a_dialog import ADialog

    from dialogs.ooh_dialog import OOHDialog
    from model import TribeTable, OOHRecord, Child, Context, StateTable, TribeStateTable, ChildTable, ARecordTable, \
        OOHRecordTable, ContextTable


    def initialize_database() -> None:
        dialog = DatabaseSetupDialog()
        controller = GenericController(dialog, Agency)
        data = controller.add()
        if data:
            model.create_tables()
            ContextTable.get_or_create(e1=data.e1)
        else:
            sys.exit(1)


    def epa_tribes() -> dict:
        results = {}
        query = TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)
        for tribe in query:
            states = ", ".join([state.state.code for state in tribe.states])
            results[tribe.id] = f"{tribe.tribe} ({states})"
        return results

    def main():
        """
        @startuml
        start
        :show splash page;
        :open the database;
        :populate the child list
        in the main form;
        :show the form;
        :execute event loop;
        end
        @enduml
        """
        try:
            app = QApplication()
            app.setApplicationName('ADT')
            app.setApplicationDisplayName('ADT')
            app.setDesktopFileName('ADT')

            if getattr(sys, 'frozen', False):
                bundle_dir = sys._MEIPASS
            else:
                bundle_dir = os.path.dirname(os.path.abspath(__file__))

            pixmap = QPixmap(Path(bundle_dir) / "assets" / "pexels-negative-space-97077.jpg")
            splash = QSplashScreen(pixmap)
            splash.show()
            splash.showMessage("Opening database...", color=QColor.fromRgb(255, 255, 255, 255))
            QCoreApplication.processEvents()

            with open(Path(bundle_dir) / 'ui' / 'style.qss', 'r') as f:
                style_sheet = f.read()
            app.setStyleSheet(style_sheet)

            if getattr(sys, 'frozen', False):
                database_path = Path.home() / 'default.db'
            else:
                database_path = 'default.db'
            model.open_database(str(database_path))

            try:
                if ContextTable.select().count() == 0:
                    initialize_database()
            except (peewee.OperationalError, peewee.DoesNotExist) as e:
                initialize_database()

            main_window = MainWindow()
            main_window.context_id = ContextTable.select().first().id
            main_window.epa_tribes = epa_tribes()
            query = ChildTable.select()
            main_window.refresh_children(query)
            main_window.show()
            splash.finish(main_window)
            sys.exit(app.exec())

        except Exception as e:
            traceback.print_exc()


    if __name__ == '__main__':
        main()

except Exception as e:
    with open('./stderr.txt', 'w') as stderr:
        traceback.print_exc(file=stderr)
