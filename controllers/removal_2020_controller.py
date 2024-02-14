from typing import Any, Optional, Callable

from PySide6.QtWidgets import QDialog, QMessageBox
from pydantic import ValidationError

from controllers.case_worker_visit_controller import CaseWorkerVisitController
from controllers.living_arrangement_controller import LivingArrangementController
from controllers.periodic_review_controller import PeriodicReviewController
from controllers.permanency_hearing_controller import PermanencyHearingController
from controllers.permanency_plan_controller import PermanencyPlanController
from controllers.utilities import show_error_dialog
from controllers.validators.removal2020_validator import Removal2020Validator
from dialogs.removal2020_dialog import Removal2020Dialog
from model.models import MyBaseModel, Removal2020, LivingArrangement, PermanencyPlan, CaseVisit, PermanencyHearing, \
    PeriodicReview


class Removal2020Controller:
    """Provides a basic controller for the dialogs. The basic controller serves as the interface point between the model
     and the view. The GenericController provides to main entry points: add() and edit(). These methods handle adding
     and editing model data using the view provided at time of controller instantiation.
     """

    def __init__(self, parent, child_name: str, data: Removal2020):
        self._data = None
        self.dialog: Removal2020Dialog = Removal2020Dialog(parent)
        self.validator: Removal2020Validator = Removal2020Validator(self.dialog)
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
        self.dialog.exec()

    @property
    def data(self) -> Removal2020:
        return self._data

    @data.setter
    def data(self, v: Removal2020) -> None:
        self._data = v
        self._data.scatter(self.dialog)
        self.dialog.refresh_case_worker_visits()
        self.dialog.refresh_living_arrangements()
        self.dialog.refresh_permanency_plans()
        self.dialog.refresh_periodic_reviews()
        self.dialog.refresh_permanency_hearings()

    def do_save(self) -> None:
        # gather model fields from the view
        # bubble the save operation up the call stack until the record is saved in the database
        if self.serialize():
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
            if hasattr(self.dialog, key):
                if getattr(self.dialog, key) != getattr(self.data, key):
                    return True
        return False

    def serialize(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate_clicked():
                    return False
            self.data.gather(self.dialog)
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

        controller = LivingArrangementController(self.dialog, self.dialog.child_name, data)
        controller.parent_data = self.dialog
        controller.on_save = save
        controller.exec()

    def do_edit_living_arrangement(self, *args, **kwargs):

        def save():
            self.dialog.refresh_living_arrangements()
            self.do_save()

        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.dialog.living_arrangements_current_row
        if current_row >= 0:
            controller = LivingArrangementController(self.dialog, self.dialog.child_name,
                                                     data=self.dialog.living_arrangements[current_row])
            controller.on_save = save
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_living_arrangement(self, *args, **kwargs):
        current_row = self.dialog.living_arrangements_current_row
        if 0 <= current_row < len(self.dialog.living_arrangements):
            del self.dialog.living_arrangements[current_row]
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

        controller = PermanencyPlanController(self.dialog, self.dialog.child_name, data)
        controller.on_save = save
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_permanency_plan(self, *args, **kwargs):

        def save():
            self.dialog.refresh_permanency_plans()
            self.do_save()

        current_row = self.dialog.permanency_plan_current_row
        if current_row >= 0:
            controller = PermanencyPlanController(self.dialog, self.dialog.child_name,
                                                  self.dialog.permanency_plans[current_row])
            controller.on_save = save
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_permanency_plan(self, *args, **kwargs):
        current_row = self.dialog.permanency_plan_current_row
        if 0 <= current_row <= len(self.dialog.permanency_plans):
            del self.dialog.permanency_plans[current_row]
            self.dialog.refresh_permanency_plans()

    def do_add_case_worker_visit(self, *args, **kwargs):
        is_new = True
        data = CaseVisit()

        def save():
            nonlocal is_new, data
            if is_new:
                self.dialog.case_worker_visits.append(data)
                is_new = False
            self.dialog.refresh_case_worker_visits()
            self.do_save()

        controller: CaseWorkerVisitController = CaseWorkerVisitController(self.dialog, self.dialog.child_name, data)
        controller.on_save = save
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_case_worker_visit(self, *args, **kwargs):
        def save():
            self.dialog.refresh_case_worker_visits()
            self.do_save()

        # if the case_worker_visit_table has a current row, pass the corresponding obj item to the dialog
        current_row: int = self.dialog.case_worker_visit_current_row
        if current_row >= 0:
            controller: CaseWorkerVisitController = CaseWorkerVisitController(self.dialog, self.dialog.child_name,
                                                                              self.dialog.case_worker_visits[
                                                                                  current_row])
            controller.on_save = save
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_case_worker_visit(self, *args, **kwargs):
        # if the case_worker_visit_table has a current row, delete it from the obj and refresh the table
        current_row: int = self.dialog.case_worker_visit_current_row
        if 0 <= current_row < len(self.dialog.case_worker_visits):
            del self.dialog.case_worker_visits[current_row]
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

        controller = PermanencyHearingController(self.dialog, self.dialog.child_name, data)
        controller.on_save = save
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_permanency_hearing(self, *args, **kwargs) -> None:

        def save():
            self.dialog.refresh_permanency_hearings()
            self.do_save()

        # if the permanency_hearing_table has a current row, pass the corresponding obj item to the dialog
        current_row: int = self.dialog.permanency_hearings_current_row
        if current_row >= 0:
            controller = PermanencyHearingController(self.dialog, self.dialog.child_name,
                                                     self.dialog.permanency_hearings[current_row])
            controller.on_save = save
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_permanency_hearing(self):
        current_row = self.dialog.permanency_hearings_current_row
        if 0 <= current_row < len(self.dialog.permanency_hearings):
            del self.dialog.permanency_hearings[current_row]
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

        controller: PeriodicReviewController = PeriodicReviewController(self.dialog, self.dialog.child_name, data=data)
        controller.on_save = save
        controller.parent_data = self.dialog
        controller.exec()

    def do_edit_periodic_review(self):
        def save():
            self.dialog.refresh_periodic_reviews()
            self.do_save()

        current_row: int = self.dialog.periodic_reviews_current_row
        if current_row >= 0:
            controller: PeriodicReviewController = PeriodicReviewController(self.dialog, self.dialog.child_name,
                                                                            data=self.dialog.periodic_reviews[
                                                                                current_row])
            controller.on_save = save
            controller.parent_data = self.dialog
            controller.exec()

    def do_delete_periodic_review(self):
        current_row: int = self.dialog.periodic_reviews_current_row
        if 0 <= current_row < len(self.dialog.periodic_reviews):
            del self.dialog.periodic_reviews[current_row]
            self.dialog.refresh_periodic_reviews()
