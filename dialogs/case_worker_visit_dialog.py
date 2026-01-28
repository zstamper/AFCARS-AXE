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

import datetime
from typing import Optional, Callable

from PySide6.QtWidgets import QWidget

from dialogs import BaseDialog
from model.models import FileType, ChildName


class CaseVisitDialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_case_visit.ui')
        self.child = None
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.file_type: FileType = FileType.PRODUCTION
        self.last_updated: Optional[datetime.datetime] = None
        self.id: int | None = None
        self.removal_id: int | None = None
        self._child_name: ChildName = ChildName()
        self.on_validate: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_save_and_add: Optional[Callable] = None
        self.on_close: Optional[Callable] = None

    def clear(self, exclude: list[str] = None) -> None:
        super().clear()
        self.child_name = ""

    def _wire_ui(self) -> None:
        self.setModal(True)
        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.save_and_add_button.clicked.connect(self.save_and_add_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)

    def validate_button_clicked(self):
        self.on_validate() if self.on_validate else None

    def save_button_clicked(self):
        self.on_save() if self.on_save else None

    def save_and_add_button_clicked(self):
        if self.on_save_and_add:
            self.on_save_and_add()

    def close_button_clicked(self):
        if self.on_close and not self.on_close():
            return
        self.close()

    @property
    def child_name(self) -> ChildName:
        return self._child_name

    @child_name.setter
    def child_name(self, v: ChildName) -> None:
        self._child_name = v
        self.setWindowTitle(f"Caseworker Visit: {str(self._child_name)}")

    @property
    def e151(self) -> int | None:
        return self._get_int_field(self.ui.e151)

    @e151.setter
    def e151(self, v: int) -> None:
        self._set_int_field(self.ui.e151, v)

    @property
    def e152(self) -> int | None:
        return self._get_combobox_selection(self.ui.e152, 1)

    @e152.setter
    def e152(self, v: int) -> None:
        self._set_combobox_selection(self.ui.e152, v, -1)
