from typing import Any

from PySide6.QtWidgets import QDialog
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

    def __init__(self, parent, child_name: str):
        self.dialog: Removal2020Dialog = Removal2020Dialog(parent)
        self.dialog.child_name = child_name
        self.validator: Removal2020Validator = Removal2020Validator(self.dialog)
        self.dialog.on_accept = self.do_accept
        self.dialog.on_tab_changed = self.do_tab_changed
        self.new_data = None
        self.previous_tab = 0
        self.dialog.on_add_living_arrangement = self.do_add_living_arrangement
        self.dialog.on_edit_living_arrangement = self.do_edit_living_arrangement
        self.dialog.on_delete_living_arrangement = self.do_delete_living_arrangement
        self.dialog.on_add_case_worker_visit = self.do_add_case_worker_visit
        self.dialog.on_edit_case_worker_visit = self.do_edit_case_worker_visit
        self.dialog.on_delete_case_worker_visit = self.do_edit_case_worker_visit
        self.dialog.on_add_permanency_plan = self.do_add_permanency_plan
        self.dialog.on_edit_permanency_plan = self.do_edit_permanency_plan
        self.dialog.on_delete_permanency_plan = self.do_delete_permanency_plan
        self.dialog.on_add_permanency_hearing = self.do_add_permanency_hearing
        self.dialog.on_edit_permanency_hearing = self.do_edit_permanency_hearing
        self.dialog.on_delete_permanency_hearing = self.do_delete_permanency_hearing
        self.dialog.on_add_periodic_review = self.do_add_periodic_review
        self.dialog.on_edit_periodic_review = self.do_edit_periodic_review
        self.dialog.on_delete_periodic_review = self.do_delete_periodic_review

    def add(self) -> Any:
        """Shows an empty dialog, lets the user do what they will, then returns either a new model instance or None,
        depending on whether the form contents are "valid" or not. The "valid" determination is handled by the model
        as a feature of pydantic."""
        self.dialog.refresh_case_worker_visits()
        self.dialog.refresh_living_arrangements()
        self.dialog.refresh_permanency_plans()
        self.dialog.refresh_periodic_reviews()
        self.dialog.refresh_permanency_hearings()
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            return self.new_data
        return None

    def edit(self, data: MyBaseModel) -> None:
        """Pushes the model data into the form, shows the form, and lets the user do what they will. If the form
        contents are valid, the model instance is modified with the new form contents. Otherwise, the model contents are
        left unchanged. Like the add() method, "valid" is determined by rules in the model using pydantic."""
        data.scatter(self.dialog)
        self.dialog.refresh_case_worker_visits()
        self.dialog.refresh_living_arrangements()
        self.dialog.refresh_permanency_plans()
        self.dialog.refresh_periodic_reviews()
        self.dialog.refresh_permanency_hearings()
        self.dialog.exec()
        if self.dialog.result() == QDialog.Accepted:
            data.gather(self.dialog)
        else:
            # put the data back in to the dialog so that further queries of the form don't get confused by the form
            # state not matching the data state
            data.scatter(self.dialog)

    def do_accept(self) -> bool:
        try:
            if hasattr(self.dialog, 'validate_on_accept') and self.dialog.validate_on_accept:
                if not self.do_validate_clicked():
                    return False
            self.new_data = Removal2020.crib(self.dialog)
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
        controller = LivingArrangementController(self.dialog, self.dialog.child_name)
        data: LivingArrangement = controller.add()
        if data is not None:
            self.dialog.living_arrangements.append(data)
            self.dialog.refresh_living_arrangements()

    def do_edit_living_arrangement(self, *args, **kwargs):
        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.dialog.living_arrangements_current_row
        if current_row >= 0:
            controller = LivingArrangementController(self.dialog, self.dialog.child_name)
            data = self.dialog.living_arrangements[current_row]
            controller.edit(data)
            self.dialog.refresh_living_arrangements()

    def do_delete_living_arrangement(self, *args, **kwargs):
        current_row = self.dialog.living_arrangements_current_row
        if 0 <= current_row < len(self.dialog.living_arrangements):
            del self.dialog.living_arrangements[current_row]
            self.dialog.refresh_living_arrangements()

    def do_add_permanency_plan(self, *args, **kwargs):
        controller = PermanencyPlanController(self.dialog, self.dialog.child_name)
        data: PermanencyPlan = controller.add()
        if data is not None:
            self.dialog.permanency_plans.append(data)
            self.dialog.refresh_permanency_plans()

    def do_edit_permanency_plan(self, *args, **kwargs):
        current_row = self.dialog.permanency_plan_current_row
        if current_row >= 0:
            controller = PermanencyPlanController(self.dialog, self.dialog.child_name)
            data = self.dialog.permanency_plans[current_row]
            controller.edit(data)
            self.dialog.refresh_permanency_plans()

    def do_delete_permanency_plan(self, *args, **kwargs):
        current_row = self.dialog.permanency_plan_current_row
        if 0 <= current_row <= len(self.dialog.permanency_plans):
            del self.dialog.permanency_plans[current_row]
            self.dialog.refresh_permanency_plans()

    def do_add_case_worker_visit(self, *args, **kwargs):
        controller: CaseWorkerVisitController = CaseWorkerVisitController(self.dialog, self.dialog.child_name)
        data: CaseVisit = controller.add()
        if data is not None:
            self.dialog.case_worker_visits.append(data)
            self.dialog.refresh_case_worker_visits()

    def do_edit_case_worker_visit(self, *args, **kwargs):
        # if the case_worker_visit_table has a current row, pass the corresponding obj item to the dialog
        current_row: int = self.dialog.case_worker_visit_current_row
        if current_row >= 0:
            controller: CaseWorkerVisitController = CaseWorkerVisitController(self.dialog, self.dialog.child_name)
            controller.clear()
            data: CaseVisit = self.dialog.case_worker_visits[current_row]
            controller.edit(data)
            self.dialog.refresh_case_worker_visits()

    def do_delete_case_worker_visit(self, *args, **kwargs):
        # if the case_worker_visit_table has a current row, delete it from the obj and refresh the table
        current_row: int = self.dialog.case_worker_visit_current_row
        if 0 <= current_row < len(self.dialog.case_worker_visits):
            del self.dialog.case_worker_visits[current_row]
            self.dialog.refresh_case_worker_visits()

    def do_add_permanency_hearing(self) -> None:
        controller = PermanencyHearingController(self.dialog, self.dialog.child_name)
        data: PermanencyHearing = controller.add()
        if data is not None:
            self.dialog.permanency_hearings.append(data)
            self.dialog.refresh_permanency_hearings()

    def do_edit_permanency_hearing(self) -> None:
        # if the permanency_hearing_table has a current row, pass the corresponding obj item to the dialog
        current_row: int = self.dialog.permanency_hearings_current_row
        if current_row >= 0:
            controller: PermanencyHearingController = PermanencyHearingController(self.dialog, self.dialog.child_name)
            data: PermanencyHearing = self.dialog.permanency_hearings[current_row]
            controller.edit(data)
            self.dialog.refresh_permanency_hearings()

    def do_delete_permanency_hearing(self):
        current_row = self.dialog.permanency_hearings_current_row
        if 0 <= current_row < len(self.dialog.permanency_hearings):
            del self.dialog.permanency_hearings[current_row]
            self.dialog.refresh_permanency_plans()

    def do_add_periodic_review(self):
        controller: PeriodicReviewController = PeriodicReviewController(self.dialog, self.dialog.child_name)
        data: PeriodicReview = controller.add()
        if data is not None:
            self.dialog.periodic_reviews.append(data)
            self.dialog.refresh_periodic_reviews()

    def do_edit_periodic_review(self):
        current_row: int = self.dialog.periodic_reviews_current_row
        if current_row >= 0:
            controller: PeriodicReviewController = PeriodicReviewController(self.dialog, self.dialog.child_name)
            data: PeriodicReview = self.dialog.periodic_reviews[current_row]
            controller.edit(data)
            self.dialog.refresh_periodic_reviews()

    def do_delete_periodic_review(self):
        current_row: int = self.dialog.periodic_reviews_current_row
        if 0 <= current_row < len(self.dialog.periodic_reviews):
            del self.dialog.periodic_reviews[current_row]
            self.dialog.refresh_periodic_reviews()
