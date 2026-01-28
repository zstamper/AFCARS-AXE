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

from typing import Optional, Callable
from datetime import datetime

from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from pydantic import ValidationError

from controllers.removal1993_controller import Removal1993Controller
from controllers.removal_2020_controller import Removal2020Controller
from controllers.second_parent_controller import SecondParentController
from controllers.utilities import show_error_dialog, get_epa_tribes
from controllers.validators.ooh_validator import OOHValidator
from dialogs.ooh_dialog import OOHDialog
from model.models import Removal1993, Removal2020, SecondParent, RecognizedTribe, BaseChild, Child, FileType, OOHRecord, \
    ChildName


class OOHController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, e1: str = "", /, file_type: FileType = FileType.PRODUCTION):
        self.dialog = OOHDialog(parent)
        self.file_type = file_type
        # self.new_data: Child | None = None
        self.validator = OOHValidator(self.dialog)
        self.dialog.current_tab = 0
        self.previous_tab = 0
        self._base_child: BaseChild | None = None
        self._child: Child | None = None
        self.on_save: Optional[Callable] = None
        self.e1: str = e1
        self.context_rec_id: int = 0
        self.base_child_rec_id: int = 0

        # Wire up the dialog to our event handlers
        self.dialog.on_accept = self.serialize

        self.dialog.on_close = self.do_close
        self.dialog.on_save = self.do_save
        self.dialog.on_tab_changed = self.do_tab_changed
        self.dialog.on_validate_clicked = self.do_validate_clicked
        self.dialog.on_add_removal1993_clicked = self.do_add_removal1993
        self.dialog.on_edit_removal1993_clicked = self.do_edit_removal1993
        self.dialog.on_delete_removal1993_clicked = self.do_delete_removal1993
        self.dialog.on_add_removal2020_clicked = self.do_add_removal2020
        self.dialog.on_edit_removal2020_clicked = self.do_edit_removal2020
        self.dialog.on_delete_removal2020_clicked = self.do_delete_removal2020
        self.dialog.on_add_putative_parent = self.do_add_putative_parent
        self.dialog.on_edit_putative_parent = self.do_edit_putative_parent
        self.dialog.on_delete_putative_parent = self.do_delete_putative_parent
        self.dialog.on_add_tribe_clicked = self.do_add_tribe
        self.dialog.on_remove_tribe_clicked = self.do_remove_tribe

        self.dialog.epa_tribes = get_epa_tribes()

    @property
    def file_type(self) -> FileType:
        return self.dialog.file_type

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        self.dialog.file_type = v

    @property
    def child_name(self) -> ChildName:
        return self.dialog.child_name

    @child_name.setter
    def child_name(self, v: ChildName) -> None:
        self.dialog.child_name = v

    @property
    def base_child(self) -> BaseChild:
        return self._base_child

    @base_child.setter
    def base_child(self, v: BaseChild) -> None:
        self._base_child = v
        self.dialog.e4 = v.e4
        self.dialog.first_name = v.first_name
        self.dialog.last_name = v.last_name

    @base_child.deleter
    def base_child(self) -> None:
        self._base_child = None
        self.dialog.e4 = ""
        self.dialog.first_name = ""
        self.dialog.last_name = ""

    @property
    def child(self) -> Child:
        return self._child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v
        self._child = v
        for key in vars(v).keys():
            if hasattr(self.dialog, key):
                setattr(self.dialog, key, getattr(v, key))
        if v.ooh:
            for key in vars(v.ooh).keys():
                if hasattr(self.dialog, key):
                    setattr(self.dialog, key, getattr(v.ooh, key))

    @staticmethod
    def confirm_save() -> bool:
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Close)
        msgBox.setDefaultButton(QMessageBox.Save)
        return msgBox.exec() == QMessageBox.Save

    def is_dirty(self) -> bool:
        for key in vars(self.child).keys():
            if hasattr(self.dialog, key):
                if getattr(self.dialog, key) != getattr(self.child, key):
                    return True
        for key in vars(self.child.ooh).keys():
            if hasattr(self.dialog, key):
                if getattr(self.dialog, key) != getattr(self.child.ooh, key):
                    return True
        if len(self.dialog.removals1993) < self._initial_removals1993_count:
            return True
        if len(self.dialog.removals2020) < self._initial_removals2020_count:
            return True
        if len(self.dialog.second_parents) < self._initial_second_parents_count:
            return True
        current_tribe_ids = {tribe.e9 for tribe in self.dialog.tribes}
        if current_tribe_ids != self._initial_tribe_ids:
            return True

    def serialize(self) -> bool:
        try:
            for key in vars(self.base_child).keys():
                if key != 'id':
                    if hasattr(self.dialog, key):
                        setattr(self.base_child, key, getattr(self.dialog, key))
            for key in vars(self.child).keys():
                if hasattr(self.dialog, key):
                    setattr(self.child, key, getattr(self.dialog, key))
            if not self.child.ooh:
                self.child.ooh = OOHRecord()
            for key in vars(self.child.ooh).keys():
                if hasattr(self.dialog, key):
                    setattr(self.child.ooh, key, getattr(self.dialog, key))
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def do_save(self) -> None:
        # gather model fields from the view
        # bubble the save operation up the call stack until the record is saved in the database
        if self.serialize():
            self.base_child.last_updated_ooh = datetime.now()
            if self.on_save:
                self.on_save()

    def do_close(self) -> bool:
        if self.is_dirty():
            if self.confirm_save():
                self.do_save()
        return True

    def exec(self):
        self.dialog.settle()
        self.dialog.enable_icwa(not self.is_tribe())
        self._initial_removals1993_count = len(self.dialog.removals1993)
        self._initial_removals2020_count = len(self.dialog.removals2020)
        self._initial_second_parents_count = len(self.dialog.second_parents)
        self._initial_tribe_ids = {tribe.e9 for tribe in self.dialog.tribes}
        self.dialog.exec()

    def clear(self):
        self.dialog.clear()

    def _update_tab_labels(self, tab: int, warning: bool):
        if not warning:
            if self.dialog.tab_label(tab).startswith('⚠️'):
                self.dialog.set_tab_label(tab, self.dialog.tab_label(tab)[2:])
        else:
            if not self.dialog.tab_label(tab).startswith('⚠️'):
                self.dialog.set_tab_label(tab, f"⚠️{self.dialog.tab_label(tab)}")

    def do_tab_changed(self, new_tab: int):
        tab_ok = self.validator.validate_tab(self.previous_tab)
        self._update_tab_labels(self.previous_tab, not tab_ok)
        self.previous_tab = new_tab

    def do_validate_clicked(self):
        tab_ok = self.validator.validate_tab(self.dialog.current_tab)
        self._update_tab_labels(self.dialog.current_tab, not tab_ok)
        if not tab_ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)

    def do_add_removal1993(self) -> None:
        is_new = True
        data = Removal1993()

        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.removals1993.append(data)
                is_new = False
            self.dialog.refresh_removals1993()
            self.do_save()

        controller: Removal1993Controller = Removal1993Controller(self.dialog,
                                                                  self.dialog.child_name,
                                                                  data,
                                                                  file_type=self.file_type)
        controller.on_save = save
        controller.child = self.child
        controller.exec()

    def do_edit_removal1993(self) -> None:
        def save():
            self.dialog.refresh_removals1993()
            self.do_save()
        current_row = self.dialog.current_removal1993_row()
        item = self.dialog.ui.removal_1993_table.item(current_row, 0)
        selected_removal = item.data(Qt.UserRole) if item is not None else None
        if selected_removal:
            controller = Removal1993Controller(self.dialog, self.dialog.child_name,
                selected_removal, file_type=self.file_type)
            controller.on_save = save
            controller.child = self.child
            controller.exec()

    def do_delete_removal1993(self) -> None:
        current_row = self.dialog.current_removal1993_row()
        item = self.dialog.ui.removal_1993_table.item(current_row, 0)
        selected_removal = item.data(Qt.UserRole) if item is not None else None
        if selected_removal in self.dialog.removals1993:
            self.dialog.removals1993.remove(selected_removal)
            self.dialog.refresh_removals1993()

    def do_add_removal2020(self) -> None:
        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.removals2020.append(data)
                is_new = False
            self.dialog.refresh_removals2020()
            self.do_save()

        is_new = True

        data = Removal2020()
        # element 104 should be preset to checked if the funding element is checked.
        # funding element may be checked if E1 is a state agency.
        data.e104 = self.dialog.funding

        controller: Removal2020Controller = Removal2020Controller(self.dialog, self.dialog.child_name,
                                                                  data, file_type=self.file_type)
        controller.on_save = save
        controller.child = self.child
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_removal2020(self) -> None:
        def save():
            self.dialog.refresh_removals2020()
            self.do_save()
        current_row = self.dialog.current_removal2020_row()
        item = self.dialog.ui.removal_2020_table.item(current_row, 0)
        selected_removal = item.data(Qt.UserRole) if item is not None else None
        if selected_removal:
            controller = Removal2020Controller(
                self.dialog,
                self.dialog.child_name,
                selected_removal,
                file_type=self.file_type
            )
            controller.on_save = save
            controller.child = self.child
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_removal2020(self) -> None:
        current_row = self.dialog.current_removal2020_row()
        item = self.dialog.ui.removal_2020_table.item(current_row, 0)
        selected_removal = item.data(Qt.UserRole) if item is not None else None
        if selected_removal in self.dialog.removals2020:
            self.dialog.removals2020.remove(selected_removal)
            self.dialog.refresh_removals2020()

    # ===== SecondParent ======================================================

    # When a parent is added, it should be assigned the first available parent number >= 2.

    def _next_parent_number(self) -> int:
        # second_parents[0] is the 2nd parent. second_parents[1:] are the putative parents.
        return self.dialog.second_parents[-1].number + 1

    def do_add_putative_parent(self) -> None:
        is_new = True

        def save():
            nonlocal is_new
            if is_new:
                self.dialog.second_parents.append(controller.data)
                is_new = False

            self.dialog.refresh_second_parents()
            self.do_save()

        controller = SecondParentController(self.dialog, child_name=self.dialog.child_name,
                                            data=SecondParent(number=self._next_parent_number()))
        controller.on_save = save
        controller.child = self.child
        controller.e60 = self.dialog.e60
        controller.file_type = self.file_type
        controller.exec()

    def do_edit_putative_parent(self) -> None:
        def save():
            self.dialog.refresh_second_parents()
            self.do_save()
        current_row = self.dialog.current_second_parents_row()
        if current_row >= 0:
            item = self.dialog.ui.parent2tpr.item(current_row, 0)
            selected_parent = item.data(Qt.UserRole) if item is not None else None
            if selected_parent:
                controller = SecondParentController(self.dialog, child_name=self.dialog.child_name,
                    data=selected_parent)
            controller.on_save = save
            controller.child = self.child
            controller.e60 = self.dialog.e60
            controller.file_type = self.file_type
            controller.exec()

    def do_delete_putative_parent(self) -> None:
        current_row = self.dialog.current_second_parents_row()
        item = self.dialog.ui.parent2tpr.item(current_row, 0)
        selected_parent = item.data(Qt.UserRole) if item is not None else None
        if selected_parent in self.dialog.second_parents:
            self.dialog.second_parents.remove(selected_parent)
            skip = True
            number = 3
            for parent in self.dialog.second_parents:
                if skip:
                    skip = False
                    continue
                parent.number = number
                number += 1
            self.dialog.refresh_second_parents()

    def do_add_tribe(self):
        row: int = self.dialog.current_epa_tribe_row()
        if row >= 0:
            if self.dialog.epa_tribes[row].id not in [tribe.e9 for tribe in self.dialog.tribes]:
                self.dialog.tribes.append(RecognizedTribe(id=None, ooh_id=None, e9=int(self.dialog.epa_tribes[row].epa_code)
))
                self.dialog.refresh_tribes()

    def do_remove_tribe(self):
        row: int = self.dialog.current_tribe_row()
        if row >= 0:
            del self.dialog.tribes[row]
            self.dialog.refresh_tribes()

    def is_tribe(self) -> bool:
        return len(self.e1) == 3
