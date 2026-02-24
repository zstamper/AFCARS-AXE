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

from controllers.case_worker_visit_controller import CaseWorkerVisitController
from controllers.living_arrangement_controller import LivingArrangementController
from controllers.periodic_review_controller import PeriodicReviewController
from controllers.permanency_hearing_controller import PermanencyHearingController
from controllers.permanency_plan_controller import PermanencyPlanController
from controllers.utilities import show_error_dialog
from controllers.validators.removal2020_validator import Removal2020Validator
from dialogs.removal2020_dialog import Removal2020Dialog
from model.models import Removal2020, LivingArrangement, PermanencyPlan, CaseVisit, PermanencyHearing, \
    PeriodicReview, FileType, Child, ChildName


class Removal2020Controller:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, child_name: ChildName, data: Removal2020, /, file_type: FileType = FileType.PRODUCTION):
        self._data = None
        self.dialog: Removal2020Dialog = Removal2020Dialog(parent)
        self.file_type = file_type
        self.validator: Removal2020Validator = Removal2020Validator(self.dialog)
        self.parent_data = None
        self.dialog.child_name = child_name
        self.dialog.on_validate = self.do_validate_clicked
        self.dialog.on_tab_changed = self.do_tab_changed
        self.dialog.on_add_living_arrangement = self.do_add_living_arrangement
        self.dialog.on_edit_living_arrangement = self.do_edit_living_arrangement
        self.dialog.on_delete_living_arrangement = self.do_delete_living_arrangement
        self.dialog.on_add_case_worker_visit = self.do_add_case_worker_visit
        self.dialog.on_edit_case_worker_visit = self.do_edit_case_worker_visit
        self.dialog.on_delete_case_worker_visit = self.do_delete_case_worker_visit
        self.dialog.on_add_permanency_plan = self.do_add_permanency_plan
        self.dialog.on_edit_permanency_plan = self.do_edit_permanency_plan
        self.dialog.on_delete_permanency_plan = self.do_delete_permanency_plan
        self.dialog.on_add_permanency_hearing = self.do_add_permanency_hearing
        self.dialog.on_edit_permanency_hearing = self.do_edit_permanency_hearing
        self.dialog.on_delete_permanency_hearing = self.do_delete_permanency_hearing
        self.dialog.on_add_periodic_review = self.do_add_periodic_review
        self.dialog.on_edit_periodic_review = self.do_edit_periodic_review
        self.dialog.on_delete_periodic_review = self.do_delete_periodic_review
        self.on_save: Optional[Callable] = None
        self.dialog.on_save = self.do_save
        self.dialog.on_close = self.do_close
        self.data = data
        self.previous_tab = 0

    def exec(self):
        self.reset_dialog_state()
        self.dialog.exec()

    @property
    def child(self) -> Child:
        return self.dialog.child

    @child.setter
    def child(self, v: Child) -> None:
        self.dialog.child = v

    @property
    def data(self) -> Removal2020:
        return self._data

    @data.setter
    def data(self, v: Removal2020) -> None:
        self._data = v
        self._data.scatter(self.dialog)
        self.dialog.settle()
        self.dialog.refresh_case_worker_visits()
        self.dialog.refresh_living_arrangements()
        self.dialog.refresh_permanency_plans()
        self.dialog.refresh_periodic_reviews()
        self.dialog.refresh_permanency_hearings()

    @property
    def file_type(self) -> FileType:
        return self.dialog.file_type

    @file_type.setter
    def file_type(self, v: FileType) -> None:
        self.dialog.file_type = v

    def do_save(self) -> None:
        if self.serialize():
            self.data.last_updated = datetime.now()
            self.data.gather(self.dialog, ignore=["last_updated"])
            if self.on_save:
                self.on_save()

    @staticmethod
    def confirm_save() -> bool:
        msgBox = QMessageBox()
        msgBox.setText("The document has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Close)
        msgBox.setDefaultButton(QMessageBox.Save)
        return msgBox.exec() == QMessageBox.Save

    def do_close(self) -> bool:
        if self.is_dirty():
            if self.confirm_save():
                self.do_save()
        return True

    def is_dirty(self) -> bool:
        for key in vars(self.data).keys():
            if key == "last_updated":  # ✅ Ignore timestamp
                continue
            if hasattr(self.dialog, key):
                if getattr(self.dialog, key) != getattr(self.data, key):
                    return True
        return False

    def serialize(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate_clicked():
                    return False
            return True
        except ValidationError as ve:
            show_error_dialog(self.dialog, ve=ve)
            return False

    def _update_tab_labels(self, tab: int, warning: bool):
        if hasattr(self.dialog, 'tab_label') and hasattr(self.dialog, 'set_tab_label'):
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

    def do_validate_clicked(self) -> bool:
        tab_ok = self.validator.validate_tab(self.dialog.current_tab)
        self._update_tab_labels(self.dialog.current_tab, not tab_ok)
        if not tab_ok:
            show_error_dialog(self.dialog, messages=self.validator.messages)
        return tab_ok
    
    def reset_dialog_state(self):
        self.dialog.living_arrangements = list(self.data.living_arrangements)
        self.dialog.permanency_plans = list(self.data.permanency_plans)
        self.dialog.case_worker_visits = list(self.data.case_worker_visits)
        self.dialog.permanency_hearings = list(self.data.permanency_hearings)
        self.dialog.periodic_reviews = list(self.data.periodic_reviews)
        self.dialog.refresh_living_arrangements()
        self.dialog.refresh_permanency_plans()
        self.dialog.refresh_case_worker_visits()
        self.dialog.refresh_permanency_hearings()
        self.dialog.refresh_periodic_reviews()

    def do_add_living_arrangement(self, *args, **kwargs):
        is_new = True
        data = LivingArrangement()

        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.living_arrangements.append(data)
                is_new = False
            self.dialog.refresh_living_arrangements()
            self.do_save()

        controller = LivingArrangementController(self.dialog, self.dialog.child_name, data, file_type=self.file_type)
        controller.child = self.child
        controller.file_type = self.file_type
        controller.parent_data = self.dialog
        controller.e39 = self.parent_data.e39
        controller.e56 = self.parent_data.e56
        controller.e57 = self.parent_data.e57
        controller.on_save = save
        controller.exec()

    def do_edit_living_arrangement(self, *args, **kwargs):
        data: LivingArrangement | None = None

        def save():
            nonlocal data
            self.dialog.refresh_living_arrangements()
            self.do_save()

        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.dialog.living_arrangements_current_row
        if current_row >= 0:
            item = self.dialog.ui.living_arrangements_table.item(current_row, 0)
            data = item.data(Qt.UserRole) if item else None
            controller = LivingArrangementController(self.dialog,
                                                     self.dialog.child_name,
                                                     data,
                                                     file_type=self.file_type)
            controller.on_save = save
            controller.child = self.child
            controller.parent_data = self.dialog
            controller.e39 = self.parent_data.e39
            controller.e56 = self.parent_data.e56
            controller.e57 = self.parent_data.e57
            controller.exec()

    def do_delete_living_arrangement(self, *args, **kwargs):
        current_row = self.dialog.living_arrangements_current_row
        item = self.dialog.ui.living_arrangements_table.item(current_row, 0)
        data = item.data(Qt.UserRole) if item else None
        if data in self.dialog.living_arrangements:
            self.dialog.living_arrangements.remove(data)
            self.dialog.refresh_living_arrangements()

    def do_add_permanency_plan(self, *args, **kwargs):
        is_new = True
        data = PermanencyPlan()

        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.permanency_plans.append(data)
                is_new = False
            self.dialog.refresh_permanency_plans()
            self.do_save()

        controller = PermanencyPlanController(self.dialog, self.dialog.child_name, data, file_type=self.file_type)
        controller.child = self.child
        controller.on_save = save
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_permanency_plan(self, *args, **kwargs):

        def save():
            self.dialog.refresh_permanency_plans()
            self.do_save()

        current_row = self.dialog.permanency_plan_current_row
        item = self.dialog.ui.permanency_plans_table.item(current_row, 0)
        data = item.data(Qt.UserRole) if item else None
        if data:
            controller = PermanencyPlanController(
                self.dialog, self.dialog.child_name, data, file_type=self.file_type)
            controller.on_save = save
            controller.child = self.child
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_permanency_plan(self, *args, **kwargs):
        current_row = self.dialog.permanency_plan_current_row
        if 0 <= current_row <= len(self.dialog.permanency_plans):
            current_row = self.dialog.permanency_plan_current_row
            item = self.dialog.ui.permanency_plans_table.item(current_row, 0)
            data = item.data(Qt.UserRole) if item else None
            if data in self.dialog.permanency_plans:
                self.dialog.permanency_plans.remove(data)
                self.dialog.refresh_permanency_plans()

    def do_add_case_worker_visit(self, *args, **kwargs):
    # Open the Case Worker Visit dialog to add one or more new visits.
    # Uses a loop (no recursion) so 'Save + Add' can open another dialog
    # without calling do_add_case_worker_visit() from inside itself.

        while True:
            # This flag indicates whether the user clicked 'Save + Add'
            # on THIS particular visit dialog.
            add_another = False

            # Create a new CaseVisit for this iteration
            is_new = True
            data = CaseVisit()

            def save():
                """
                Called when the user clicks 'Save' in the CaseVisitDialog.
                Saves this visit and updates the parent Removal2020 record,
                but does NOT automatically open another dialog.
                """
                nonlocal is_new, data

                if is_new:
                    # First save for this new visit: add it to the list
                    self.dialog.case_worker_visits.append(data)
                    is_new = False

                # Refresh the Case Worker Visits table in the Removal2020Dialog
                self.dialog.refresh_case_worker_visits()

                # Save the Removal2020 record itself
                self.do_save()

                # Note: we do NOT close the dialog here.
                # The user can choose to close it, or click 'Save + Add', or keep editing.

            def save_and_add():
                """
                Called when the user clicks 'Save + Add'.

                We reuse the controller's do_save() method, which:
                - Validates and serializes dialog data into `data`
                - Sets data.last_updated
                - Calls our `save()` callback above (append + refresh + parent save).

                Then we mark that the user wants another visit and close this dialog.
                """
                nonlocal add_another

                # Perform the same save logic as the 'Save' button:
                # serialize the dialog into `data`, set last_updated, and invoke `save()`.
                controller.do_save()

                # Indicate that the user requested another visit
                add_another = True

                # Close the CaseVisitDialog, allowing controller.exec() to finish
                controller.dialog.accept()

            # Create a controller for this one CaseVisitDialog
            controller: CaseWorkerVisitController = CaseWorkerVisitController(
                self.dialog,
                self.dialog.child_name,
                data,
                file_type=self.file_type,
                removal_controller=self
            )

            # Wire up callbacks
            controller.on_save = save
            controller.dialog.on_save_and_add = save_and_add

            controller.child = self.child
            controller.parent_data = self.dialog

            # Open the CaseVisitDialog and wait until it is closed
            controller.exec()

            # At this point, the CaseVisitDialog is closed.
            # Decide whether to open another visit dialog.
            if not add_another:
                # User did NOT click 'Save + Add' on this dialog.
                # They either:
                #  - Saved and then closed, or
                #  - Closed without saving, etc.
                # Either way, we stop adding new visits.
                break

            # If add_another is True, the loop continues and we go back
            # to the top, creating a fresh CaseVisit and opening another dialog.

    def do_edit_case_worker_visit(self, *args, **kwargs):
        def save():
            self.dialog.refresh_case_worker_visits()
            self.do_save()

        def save_and_add():
            controller.do_save()
            controller.dialog.accept()
            self.do_add_case_worker_visit()

        current_row = self.dialog.case_worker_visit_current_row
        item = self.dialog.ui.case_visits_table.item(current_row, 0)
        data = item.data(Qt.UserRole) if item else None
        if data:
            controller = CaseWorkerVisitController(
                self.dialog, self.dialog.child_name, data, file_type=self.file_type
            )
            controller.on_save = save
            controller.on_save_and_add = save_and_add
            controller.dialog.on_save_and_add = save_and_add
            controller.child = self.child
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_case_worker_visit(self, *args, **kwargs):
        # if the case_worker_visit_table has a current row, delete it from the obj and refresh the table
        current_row: int = self.dialog.case_worker_visit_current_row
        if 0 <= current_row < len(self.dialog.case_worker_visits):
            current_row = self.dialog.case_worker_visit_current_row
            item = self.dialog.ui.case_visits_table.item(current_row, 0)
            data = item.data(Qt.UserRole) if item else None
            if data in self.dialog.case_worker_visits:
                self.dialog.case_worker_visits.remove(data)
                self.dialog.refresh_case_worker_visits()

    def do_add_permanency_hearing(self) -> None:
        is_new = True
        data = PermanencyHearing()

        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.permanency_hearings.append(data)
                is_new = False
            self.dialog.refresh_permanency_hearings()
            self.do_save()

        controller = PermanencyHearingController(self.dialog, self.dialog.child_name, data, file_type=self.file_type)
        controller.child = self.child
        controller.on_save = save
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_permanency_hearing(self, *args, **kwargs) -> None:

        def save():
            self.dialog.refresh_permanency_hearings()
            self.do_save()

        current_row = self.dialog.permanency_hearings_current_row
        item = self.dialog.ui.permanency_hearings_table.item(current_row, 0)
        data = item.data(Qt.UserRole) if item else None
        if data:
            controller = PermanencyHearingController(
                self.dialog, self.dialog.child_name, data, file_type=self.file_type)
            controller.on_save = save
            controller.child = self.child
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_permanency_hearing(self):
        current_row = self.dialog.permanency_hearings_current_row
        if 0 <= current_row < len(self.dialog.permanency_hearings):
            current_row = self.dialog.permanency_hearings_current_row
            item = self.dialog.ui.permanency_hearings_table.item(current_row, 0)
            data = item.data(Qt.UserRole) if item else None
            if data in self.dialog.permanency_hearings:
                self.dialog.permanency_hearings.remove(data)
                self.dialog.refresh_permanency_hearings()

    def do_add_periodic_review(self):
        is_new = True
        data = PeriodicReview()

        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.periodic_reviews.append(data)
                is_new = False
            self.dialog.refresh_periodic_reviews()
            self.do_save()

        controller: PeriodicReviewController = PeriodicReviewController(self.dialog, self.dialog.child_name, data,
                                                                        file_type=self.file_type)
        controller.on_save = save
        controller.child = self.child
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_periodic_review(self):
        def save():
            self.dialog.refresh_periodic_reviews()
            self.do_save()
        current_row = self.dialog.periodic_reviews_current_row
        item = self.dialog.ui.periodic_reviews_table.item(current_row, 0)
        data = item.data(Qt.UserRole) if item else None
        if data:
            controller = PeriodicReviewController(
                self.dialog, self.dialog.child_name, data, file_type=self.file_type)
            controller.on_save = save
            controller.child = self.child
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_periodic_review(self):
        current_row: int = self.dialog.periodic_reviews_current_row
        if 0 <= current_row < len(self.dialog.periodic_reviews):
            current_row = self.dialog.periodic_reviews_current_row
            item = self.dialog.ui.periodic_reviews_table.item(current_row, 0)
            data = item.data(Qt.UserRole) if item else None
            if data in self.dialog.periodic_reviews:
                self.dialog.periodic_reviews.remove(data)
                self.dialog.refresh_periodic_reviews()
