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
from typing import Callable, Optional, Any

from PySide6.QtWidgets import QWidget

from model.models import FileType, Child, ChildName
from . import BaseDialog


class Removal1993Dialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__ooh = None
        self._child = None
        self._child_name: ChildName = ChildName()
        self.id: int | None = None
        self.ooh_id: int | None = None
        self.ui: QWidget = self.load_ui('ui_removal1993.ui')
        self.file_type: FileType = FileType.PRODUCTION
        self.last_updated: Optional[datetime.datetime] = None
        self.on_validate: Optional[Callable] = None
        self.on_save: Optional[Callable] = None
        self.on_close: Optional[Callable] = None

        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())

    # ------------------------------------------------------------------------

    def clear(self, exclude: list[str] = None) -> None:
        super().clear()
        self.child_name = ""
        self.id = None
        self.ooh = None

    @property
    def child(self) -> Child:
        return self._child

    @child.setter
    def child(self, v: Child) -> None:
        self._child = v

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, id: int | None) -> None:
        self.__id = id

    @property
    def ooh(self) -> Any:
        return self.__ooh

    @ooh.setter
    def ooh(self, ooh: Any) -> None:
        self.__ooh = ooh

    @property
    def child_name(self) -> ChildName:
        return self._child_name

    @child_name.setter
    def child_name(self, v: ChildName) -> None:
        self._child_name = v
        self.setWindowTitle(f"1993 Removal: {str(self._child_name)}")

    @property
    def e69(self) -> int | None:
        return self._get_int_field(self.ui.e69)

    @e69.setter
    def e69(self, v: int) -> None:
        self._set_int_field(self.ui.e69, v)

    @property
    def e153(self) -> int | None:
        return self._get_int_field(self.ui.e153)

    @e153.setter
    def e153(self, v: int):
        self._set_int_field(self.ui.e153, v)

    @property
    def e155(self) -> int | None:
        return self._get_combobox_selection(self.ui.e155, mapping={0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8})

    @e155.setter
    def e155(self, v: int):
        self._set_combobox_selection(self.ui.e155, v, mapping={1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 6})

    # ------------------------------------------------------------------------

    def _wire_ui(self):
        self.setModal(True)

        ui = self.ui
        """add event handlers to the form"""
        self.ui.save_button.clicked.connect(self.save_button_clicked)
        self.ui.close_button.clicked.connect(self.close_button_clicked)
        self.ui.validate_button.clicked.connect(self.validate_button_clicked)

    def validate_button_clicked(self):
        if self.on_validate:
            self.on_validate()

    def save_button_clicked(self):
        if self.on_save:
            self.on_save()

    def close_button_clicked(self):
        if not self.on_close or self.on_close():
            self.close()
