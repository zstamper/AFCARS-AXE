import datetime
import traceback
from threading import Event, Timer

import peewee

import utils
from controllers.main_window2_controller import MainWindow2Controller
from model.models import Tribe

SPLASH_DELAY = 5.0

try:
    import os
    import sys
    from pathlib import Path

    from PySide6.QtCore import QFile, QCoreApplication
    from PySide6.QtGui import QAction, QPixmap, QColor, QIcon
    from PySide6.QtUiTools import QUiLoader
    from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolButton, QPushButton, QTableWidgetItem, \
        QTableWidget, QSplashScreen

    import model
    from model import TribeTable, OOHRecord, Child, Context, ContextTable, StateTable, TribeStateTable, BaseChildTable, \
        ConfigTable


    def initialize_database() -> None:
        model.create_tables()


    def epa_tribes() -> list[Tribe]:
        results = {}
        query = TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)
        return [Tribe(id=tribe.id, tribe=tribe.tribe, epa_code=tribe.epa_code,
                      states=[tribestate.state.code for tribestate in tribe.states])
                for tribe in TribeTable.select().order_by(TribeTable.tribe).prefetch(TribeStateTable, StateTable)]
        # for tribe in query:
        #     states = ", ".join([state.state.code for state in tribe.states])
        #     results[tribe.id] = f"{tribe.tribe} ({states})"
        # return results


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
        app_dir = None
        bundle_dir = None
        e = Event()
        t = Timer(SPLASH_DELAY, e.set)
        app_dir, bundle_dir = utils.file_system_directories()
        try:
            app = QApplication()
            app.setApplicationName('AXE')
            app.setApplicationDisplayName('AXE')
            app.setDesktopFileName('AXE')
            if sys.platform.startswith('win32'):
                app.setWindowIcon(QPixmap(str(bundle_dir / "assets" / "favocon.ico")))
            else:
                app.setWindowIcon(QPixmap(str(bundle_dir / "assets" / "app_icon.icns")))

            pixmap = QPixmap(bundle_dir / "assets" / "pexels-negative-space-97077.jpg")
            splash = QSplashScreen(pixmap)
            splash.show()
            t.start()
            splash.showMessage(f"Opening database: {app_dir / 'axe.db'}", color=QColor.fromRgb(255, 255, 255, 255))
            QCoreApplication.processEvents()

            with open(bundle_dir / 'ui' / 'style.qss', 'r') as f:
                style_sheet = f.read()
            app.setStyleSheet(style_sheet)

            database_path = app_dir / 'axe.db'
            init_needed = not Path(database_path).exists()
            if init_needed:
                splash.showMessage(f"Initializing new database: {app_dir / 'axe.db'}",
                                   color=QColor.fromRgb(255, 255, 255, 255))
                QCoreApplication.processEvents()
            model.open_database(str(database_path))

            e.wait(timeout=SPLASH_DELAY)

            main_window = MainWindow2Controller()
            main_window.show()
            splash.finish(main_window.window)
            sys.exit(app.exec())

        except Exception as e:
            traceback.print_exc()
            with open(Path.home() / 'stderr.txt', 'w+') as stderr:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file=stderr)
                traceback.print_exc(file=stderr)
                print(f"app_dir={app_dir}", file=stderr)
                print(f"bundle_dir={bundle_dir}", file=stderr)
                print('-' * 80, file=stderr)


    if __name__ == '__main__':
        main()

except Exception as e:
    traceback.print_exc()
    with open(Path.home() / 'stderr.txt', 'w+') as stderr:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file=stderr)
        traceback.print_exc(file=stderr)
        print('-' * 80, file=stderr)
