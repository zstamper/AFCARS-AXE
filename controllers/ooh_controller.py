from typing import Optional, Callable

from pydantic import ValidationError

from controllers.removal1993_controller import Removal1993Controller
from controllers.removal_2020_controller import Removal2020Controller
from controllers.second_parent_controller import SecondParentController
from controllers.utilities import show_error_dialog, get_epa_tribes
from controllers.validators.ooh_validator import OOHValidator
from dialogs.ooh_dialog import OOHDialog
from model.models import Removal1993, Removal2020, SecondParent, RecognizedTribe, BaseChild, Child


class OOHController:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, e1: str = ""):
        self.dialog = OOHDialog(parent)
        self.new_data: Child | None = None
        self.validator = OOHValidator(self.dialog)
        self.dialog.current_tab = 0
        self.previous_tab = 0
        self._base_child: BaseChild | None = None
        self._child: Child | None = None
        self.on_accept: Optional[Callable] = None
        self.e1: str = e1

        # Wire up the dialog to our event handlers
        self.dialog.on_accept = self.do_accept
        self.dialog.on_tab_changed = self.do_tab_changed
        self.dialog.on_validate_clicked = self.do_validate_clicked
        self.dialog.on_add_removal1993_clicked = self.do_add_removal1993
        self.dialog.on_edit_removal1993_clicked = self.do_edit_removal1993
        self.dialog.on_delete_removal1993_clicked = self.do_delete_removal1993
        self.dialog.on_add_removal2020_clicked = self.do_add_removal2020
        self.dialog.on_edit_removal2020_clicked = self.do_edit_removal2020
        self.dialog.on_delete_removal2020_clicked = self.do_delete_removal2020
        self.dialog.on_add_second_parent = self.do_add_second_parent
        self.dialog.on_edit_second_parent = self.do_edit_second_parent
        self.dialog.on_delete_second_parent = self.do_delete_second_parent
        self.dialog.on_add_tribe_clicked = self.do_add_tribe
        self.dialog.on_remove_tribe_clicked = self.do_remove_tribe

        self.dialog.epa_tribes = get_epa_tribes()

    @property
    def child_name(self) -> str:
        return self.dialog.child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
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
        self._child = v
        for key in vars(v).keys():
            if hasattr(self.dialog, key):
                setattr(self.dialog, key, getattr(v, key))
        if v.ooh:
            for key in vars(v.ooh).keys():
                if hasattr(self.dialog, key):
                    setattr(self.dialog, key, getattr(v.ooh, key))

    def do_accept(self) -> bool:
        try:
            for key in vars(self.base_child).keys():
                if key != 'id':
                    if hasattr(self.dialog, key):
                        setattr(self.base_child, key, getattr(self.dialog, key))
            for key in vars(self.child).keys():
                if hasattr(self.dialog, key):
                    setattr(self.child, key, getattr(self.dialog, key))
            for key in vars(self.child.ooh).keys():
                if hasattr(self.dialog, key):
                    setattr(self.child.ooh, key, getattr(self.dialog, key))
            if self.on_accept:
                self.on_accept()
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
        return False

    def show(self):
        self.dialog.enable_icwa(not self.is_tribe())
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
        controller: Removal1993Controller = Removal1993Controller(self.dialog, self.dialog.child_name)
        data: Removal1993 = controller.add()
        if data is not None:
            self.dialog.removals1993.append(data)
            self.dialog.refresh_removals1993()

    def do_edit_removal1993(self) -> None:
        current_row = self.dialog.current_removal1993_row()
        if current_row >= 0:
            controller: Removal1993Controller = Removal1993Controller(self.dialog, self.dialog.child_name)
            data: Removal1993 = self.dialog.removals1993[current_row]
            controller.edit(data)
            self.dialog.removals1993[current_row] = data
            self.dialog.refresh_removals1993()

    def do_delete_removal1993(self) -> None:
        current_row = self.dialog.current_removal1993_row()
        if 0 <= current_row < len(self.dialog.removals1993):
            del self.dialog.removals1993[current_row]
            self.dialog.refresh_removals1993()

    def do_add_removal2020(self) -> None:
        controller: Removal2020Controller = Removal2020Controller(self.dialog, self.dialog.child_name)
        data: Removal2020 = controller.add()
        if data is not None:
            self.dialog.removals2020.append(data)
            self.dialog.refresh_removals2020()

    def do_edit_removal2020(self) -> None:
        current_row = self.dialog.current_removal2020_row()
        if current_row >= 0:
            controller: Removal2020Controller = Removal2020Controller(self.dialog, self.dialog.child_name)
            data: Removal2020 = self.dialog.removals2020[current_row]
            controller.edit(data)
            self.dialog.removals2020[current_row] = data
            self.dialog.refresh_removals2020()

    def do_delete_removal2020(self) -> None:
        current_row = self.dialog.current_removal2020_row()
        if 0 <= current_row < len(self.dialog.removals2020):
            del self.dialog.removals2020[current_row]
            self.dialog.refresh_removals2020()

    # ===== SecondParent ======================================================

    def do_add_second_parent(self) -> None:
        controller = SecondParentController(self.dialog, child_name=self.dialog.child_name)
        data: SecondParent = controller.add()
        if data is not None:
            self.dialog.second_parents.append(data)
            self.dialog.refresh_second_parents()

    def do_edit_second_parent(self) -> None:
        current_row = self.dialog.current_second_parents_row()
        if current_row >= 0:
            controller = SecondParentController(self.dialog, child_name=self.dialog.child_name)
            data = self.dialog.second_parents[current_row]
            controller.edit(data)
            self.dialog.second_parents[current_row] = data
            self.dialog.refresh_second_parents()

    def do_delete_second_parent(self) -> None:
        current_row = self.dialog.current_second_parents_row()
        if 0 <= current_row < len(self.dialog.second_parents):
            del self.dialog.second_parents[current_row]
            self.dialog.refresh_second_parents()

    def do_add_tribe(self):
        row: int = self.dialog.current_epa_tribe_row()
        if row >= 0:
            if self.dialog.epa_tribes[row].id not in [tribe.e9 for tribe in self.dialog.tribes]:
                self.dialog.tribes.append(RecognizedTribe(id=None, ooh_id=None, e9=self.dialog.epa_tribes[row].id))
                self.dialog.refresh_tribes()

    def do_remove_tribe(self):
        row: int = self.dialog.current_tribe_row()
        if row >= 0:
            del self.dialog.tribes[row]
            self.dialog.refresh_tribes()

    def is_tribe(self) -> bool:
        return len(self.e1) == 3
