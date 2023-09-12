from PySide6.QtWidgets import QWidget, QCheckBox, QLineEdit, QDateEdit, QRadioButton, QTableWidgetItem

from model import Removal2020, LivingArrangement, PermanencyPlan, CaseVisit, PermanencyHearing, PeriodicReview
from . import BaseDialog
from .case_worker_visit import CaseVisitDialog
from .living_arrangement_dialog import LivingArrangementDialog
from .periodic_review_dialog import PeriodicReviewDialog
from .permanency_hearing_dialog import PermanencyHearingDialog
from .permency_plan_dialog import PermanencyPlanDialog


def e120_to_str(v: int) -> str:
    # FIXME: hmm... wonder if this should just be captured from the form?
    mapper: dict = {0: 'Foster Family Home',
                    1: 'Group home-family operated',
                    2: 'Group home-staff operated',
                    3: 'Group home-shelter care',
                    4: 'Residential treatment center',
                    5: 'Qualified residential treatment program',
                    6: 'Child care institution',
                    7: 'Child care institution-shelter care',
                    8: 'Supervised independent living',
                    9: 'Juvenile justice facility',
                    10: 'Medical or rehabilitative facility',
                    11: 'Psychiatric hospital',
                    12: 'Runaway',
                    13: 'Whereabouts unknown',
                    14: 'Placed at home'
                    }
    if v is None or v not in mapper:
        return mapper[0]
    return mapper[v]


def e148_to_str(v: int) -> str:
    mapper: dict = {1: "Reunify with parent(s) or legal guardian(s)",
                    2: "Live with other relatives",
                    3: "Adoption",
                    4: "Guardianship",
                    5: "Planned permanent living arrangement"
                    }
    if v is None or v not in mapper:
        return "unknown"
    return mapper[v]


def e152_to_str(v: int) -> str:
    mapper: dict = {0: "Child's Residence",
                    1: "Other Location"
                    }
    if v is None or v not in mapper:
        return mapper[0]
    return mapper[v]


class Removal2020Dialog(BaseDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui: QWidget = self.load_ui('ui_removal2020.ui')
        self._wire_ui()
        self.setLayout(self.ui.layout())
        self.setFixedSize(self.ui.size())
        self.obj: Removal2020 | None = None

    def populate(self, obj: Removal2020):
        self.obj = obj
        self._from_obj()
        self.errors = []
        self.is_dirty = False

    def validate(self):
        self._validate()
        return len(self.errors) == 0

    # ------------------------------------------------------------------------

    def _wire_ui(self):
        self.setModal(True)

        ui = self.ui
        """add event handlers to the form"""
        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)

        ui.living_arrangement_add_button.clicked.connect(self.add_living_arrangement)
        ui.living_arrangement_delete_button.clicked.connect(self.delete_living_arrangement)
        ui.living_arrangements_table.cellDoubleClicked.connect(self.edit_living_arrangement)

        ui.permanency_plan_add_button.clicked.connect(self.add_permanency_plan)
        ui.permanency_plan_delete_button.clicked.connect(self.delete_permanency_plan)
        ui.permanency_plans_table.cellDoubleClicked.connect(self.edit_permanency_plan)

        ui.case_visit_add_button.clicked.connect(self.add_case_visit)
        ui.case_visit_delete_button.clicked.connect(self.delete_case_visit)
        ui.case_visits_table.cellDoubleClicked.connect(self.edit_case_visit)

        ui.permanency_hearing_add_button.clicked.connect(self.add_permanency_hearing)
        ui.permanency_hearing_delete_button.clicked.connect(self.delete_permanency_hearing)
        ui.permanency_hearings_table.cellDoubleClicked.connect(self.edit_permanency_hearing)

        ui.periodic_review_add_button.clicked.connect(self.add_periodic_review)
        ui.periodic_review_delete_button.clicked.connect(self.delete_periodic_review)
        ui.periodic_reviews_table.cellDoubleClicked.connect(self.edit_periodic_review)

        # e71 item data values are 1..7 (they can't be set via the ui creator)
        for i, d in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7)):
            ui.e71.setItemData(i, d)

        # E113, E120 are combined; E120 contains null or 1..14; E113 should be computed from E120.
        self._init_radio_ynu(ui, 'e163')
        self._init_radio_ynud(ui, 'e171')
        self._init_radio_mf(ui, 'e172')
        self._init_radio_ynu(ui, 'e174')
        self._init_radio_ynud(ui, 'e182')
        self._init_radio_mf(ui, 'e183')

    def add_living_arrangement(self):
        living_arrangement: LivingArrangement = LivingArrangement(removal=self.obj)
        dialog: LivingArrangementDialog = LivingArrangementDialog(self, relaxed_rules=self.relaxed_rules)
        dialog.populate(living_arrangement)
        dialog.show()
        if dialog.exec():
            if self.obj.living_arrangements is None:
                self.obj.living_arrangements = []
            self.obj.living_arrangements.append(living_arrangement)
            row: int = self.ui.living_arrangements.rowCount()
            self.ui.living_arrangements_table.insertRow(row)
            self.ui.living_arrangements_table.setItem(row, 0, QTableWidgetItem(str(living_arrangement.e112)))
            self.ui.living_arrangements_table.setItem(row, 1, QTableWidgetItem(e120_to_str(living_arrangement.e120)))
            self.ui.living_arrangements_table.setItem(row, 2, QTableWidgetItem(""))

    def delete_living_arrangement(self):
        # if the livint_arrangement_table has a current row, delete it from the obj and refresh the table
        current_row = self.ui.living_arrangements_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            self.obj.living_arrangements.remove(current_row)
            self.ui.living_arrangements_table.removeRow(current_row)

    def edit_living_arrangement(self):
        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.ui.living_arrangements_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            living_arrangement: LivingArrangement = self.obj.living_arrangements[current_row]
            dialog: LivingArrangementDialog = LivingArrangementDialog(self, relaxed_rules=self.relaxed_rules)
            dialog.populate(living_arrangement)
            dialog.show()
            if dialog.exec():
                self.obj.living_arrangements[current_row] = living_arrangement
                self.ui.living_arrangements_table.setItem(current_row, 0,
                                                          QTableWidgetItem(str(living_arrangement.e112)))
                self.ui.living_arrangements_table.setItem(current_row, 1,
                                                          QTableWidgetItem(e120_to_str(living_arrangement.e120)))
                self.ui.living_arrangements_table.setItem(current_row, 2, QTableWidgetItem(""))

    def add_permanency_plan(self):
        permanency_plan: PermanencyPlan = PermanencyPlan(removal=self.obj)
        dialog: PermanencyPlanDialog = PermanencyPlanDialog(self, relaxed_rules=self.relaxed_rules)
        dialog.populate(permanency_plan)
        dialog.show()
        if dialog.exec():
            if self.obj.permanency_plans is None:
                self.obj.permanency_plans = []
            self.obj.permanency_plans.append(permanency_plan)
            row: int = self.ui.permanency_plans.rowCount()
            self.ui.permanency_plans_table.insertRow(row)
            self.ui.permanency_plans_table.setItem(row, 0, QTableWidgetItem(str(permanency_plan.e147)))
            self.ui.permanency_plans_table.setItem(row, 1, QTableWidgetItem(e148_to_str(permanency_plan.e148)))

    def delete_permanency_plan(self):
        # if the livint_arrangement_table has a current row, delete it from the obj and refresh the table
        current_row = self.ui.permanency_plans_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            self.obj.living_arrangements.remove(current_row)
            self.ui.permanency_plans_table.removeRow(current_row)

    def edit_permanency_plan(self):
        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.ui.permanency_plans_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            permanency_plan: PermanencyPlan = self.obj.permanency_plans[current_row]
            dialog: PermanencyPlanDialog = PermanencyPlanDialog(self, relaxed_rules=self.relaxed_rules)
            dialog.populate(permanency_plan)
            dialog.show()
            if dialog.exec():
                self.obj.living_arrangements[current_row] = permanency_plan
                self.ui.permanency_plans_table.setItem(current_row, 0,
                                                       QTableWidgetItem(str(permanency_plan.e147)))
                self.ui.permanency_plans_table.setItem(current_row, 1,
                                                       QTableWidgetItem(e148_to_str(permanency_plan.e148)))

    def add_case_visit(self):
        case_visit: CaseVisit = CaseVisit(removal=self.obj)
        dialog: CaseVisitDialog = CaseVisitDialog(self, relaxed_rules=self.relaxed_rules)
        dialog.populate(case_visit)
        dialog.show()
        if dialog.exec():
            if self.obj.case_worker_visits is None:
                self.obj.case_worker_visits = []
            self.obj.case_visits.append(case_visit)
            row: int = self.ui.case_visits.rowCount()
            self.ui.case_visits_table.insertRow(row)
            self.ui.case_visits_table.setItem(row, 0, QTableWidgetItem(str(case_visit.e151)))
            self.ui.case_visits_table.setItem(row, 1, QTableWidgetItem(e152_to_str(case_visit.e152)))

    def delete_case_visit(self):
        # if the livint_arrangement_table has a current row, delete it from the obj and refresh the table
        current_row = self.ui.case_visits_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            self.obj.living_arrangements.remove(current_row)
            self.ui.case_visits_table.removeRow(current_row)

    def edit_case_visit(self):
        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.ui.case_visits_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            case_visit: CaseVisit = self.obj.case_visits[current_row]
            dialog: CaseVisitDialog = CaseVisitDialog(self, relaxed_rules=self.relaxed_rules)
            dialog.populate(case_visit)
            dialog.show()
            if dialog.exec():
                self.obj.living_arrangements[current_row] = case_visit
                self.ui.case_visits_table.setItem(current_row, 0,
                                                  QTableWidgetItem(str(case_visit.e151)))
                self.ui.case_visits_table.setItem(current_row, 1,
                                                  QTableWidgetItem(e152_to_str(case_visit.e152)))

    def add_permanency_hearing(self):
        permanency_hearing: PermanencyHearing = PermanencyHearing(removal=self.obj)
        dialog: PermanencyHearingDialog = PermanencyHearingDialog(self, relaxed_rules=self.relaxed_rules)
        dialog.populate(permanency_hearing)
        dialog.show()
        if dialog.exec():
            if self.obj.permanency_hearings is None:
                self.obj.permanency_hearings = []
            self.obj.permanency_hearings.append(permanency_hearing)
            row: int = self.ui.permanency_hearings.rowCount()
            self.ui.permanency_hearings_table.insertRow(row)
            self.ui.permanency_hearings_table.setItem(row, 0, QTableWidgetItem(str(permanency_hearing.e150)))

    def delete_permanency_hearing(self):
        # if the livint_arrangement_table has a current row, delete it from the obj and refresh the table
        current_row = self.ui.permanency_hearings_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            self.obj.living_arrangements.remove(current_row)
            self.ui.permanency_hearings_table.removeRow(current_row)

    def edit_permanency_hearing(self):
        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.ui.permanency_hearings_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            permanency_hearing: PermanencyHearing = self.obj.permanency_hearings[current_row]
            dialog: PermanencyHearingDialog = PermanencyHearingDialog(self, relaxed_rules=self.relaxed_rules)
            dialog.populate(permanency_hearing)
            dialog.show()
            if dialog.exec():
                self.obj.living_arrangements[current_row] = permanency_hearing
                self.ui.permanency_hearings_table.setItem(current_row, 0,
                                                          QTableWidgetItem(str(permanency_hearing.e150)))

    def add_periodic_review(self):
        periodic_review: PeriodicReview = PeriodicReview(removal=self.obj)
        dialog: PeriodicReviewDialog = PeriodicReviewDialog(self, relaxed_rules=self.relaxed_rules)
        dialog.populate(periodic_review)
        dialog.show()
        if dialog.exec():
            if self.obj.periodic_reviews is None:
                self.obj.periodic_reviews = []
            self.obj.periodic_reviews.append(periodic_review)
            row: int = self.ui.periodic_reviews.rowCount()
            self.ui.periodic_reviews_table.insertRow(row)
            self.ui.periodic_reviews_table.setItem(row, 0, QTableWidgetItem(str(periodic_review.e149)))

    def delete_periodic_review(self):
        # if the livint_arrangement_table has a current row, delete it from the obj and refresh the table
        current_row = self.ui.periodic_reviews_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            self.obj.living_arrangements.remove(current_row)
            self.ui.periodic_reviews_table.removeRow(current_row)

    def edit_periodic_review(self):
        # if the living_arrangement_table has a current row, pass the corresponding obj item to the dialog
        current_row = self.ui.periodic_reviews_table.currentRow()
        if 0 <= current_row < len(self.obj.living_arrangements):
            periodic_review: PeriodicReview = self.obj.periodic_reviews[current_row]
            dialog: PeriodicReviewDialog = PeriodicReviewDialog(self, relaxed_rules=self.relaxed_rules)
            dialog.populate(periodic_review)
            dialog.show()
            if dialog.exec():
                self.obj.living_arrangements[current_row] = periodic_review
                self.ui.periodic_reviews_table.setItem(current_row, 0,
                                                       QTableWidgetItem(str(periodic_review.e149)))

    def _validate(self):
        """validates the form by iterating over the validation rules, return true if the error message list is empty"""
        ...

    def _to_obj(self):
        """copy form field contents into the model"""
        ...

    def _from_obj(self):
        """copy model fields into the form"""
        ui = self.ui
        obj = self.obj

        self._set_int_field(ui.e3, obj.e3)
        self._set_int_field(ui.e69, obj.e69)
        self._set_combobox_selection(ui.e71, obj.e71, -1)
        ui.e72.setChecked(obj.e72 == 1)
        ui.e73.setChecked(obj.e73 == 1)
        ui.e74.setChecked(obj.e74 == 1)
        ui.e75.setChecked(obj.e75 == 1)
        ui.e76.setChecked(obj.e76 == 1)
        ui.e77.setChecked(obj.e77 == 1)
        ui.e78.setChecked(obj.e78 == 1)
        ui.e79.setChecked(obj.e79 == 1)
        ui.e80.setChecked(obj.e80 == 1)
        ui.e81.setChecked(obj.e81 == 1)
        ui.e82.setChecked(obj.e82 == 1)
        ui.e83.setChecked(obj.e83 == 1)
        ui.e84.setChecked(obj.e84 == 1)
        ui.e85.setChecked(obj.e85 == 1)
        ui.e86.setChecked(obj.e86 == 1)
        ui.e87.setChecked(obj.e87 == 1)
        ui.e88.setChecked(obj.e88 == 1)
        ui.e89.setChecked(obj.e89 == 1)
        ui.e90.setChecked(obj.e90 == 1)
        ui.e91.setChecked(obj.e91 == 1)
        ui.e92.setChecked(obj.e92 == 1)
        ui.e93.setChecked(obj.e93 == 1)
        ui.e94.setChecked(obj.e94 == 1)
        ui.e95.setChecked(obj.e95 == 1)
        ui.e96.setChecked(obj.e96 == 1)
        ui.e97.setChecked(obj.e97 == 1)
        ui.e98.setChecked(obj.e98 == 1)
        ui.e99.setChecked(obj.e99 == 1)
        ui.e100.setChecked(obj.e100 == 1)
        ui.e101.setChecked(obj.e101 == 1)
        ui.e102.setChecked(obj.e102 == 1)
        ui.e103.setChecked(obj.e103 == 1)
        ui.e104.setChecked(obj.e104 == 1)
        ui.e105.setChecked(obj.e105 == 1)
        self._set_int_field(ui.e153, obj.e153)
        self._set_int_field(ui.e154, obj.e154)
        self._set_combobox_selection(ui.e155, obj.e155, -1)
        self._set_combobox_selection(ui.e156, obj.e156, -1)
        self._set_combobox_selection(ui.e157, obj.e157, -1)
        ui.e158.setChecked(obj.e158 == 1)
        ui.e159.setChecked(obj.e159 == 1)
        ui.e160.setChecked(obj.e160 == 1)
        ui.e161.setChecked(obj.e161 == 1)
        self._set_int_field(ui.e162, obj.e162)
        self._set_radio_button(ui.e163, obj.e163)
        ui.e164.setChecked(obj.e164 == 1)
        ui.e165.setChecked(obj.e165 == 1)
        ui.e166.setChecked(obj.e166 == 1)
        ui.e167.setChecked(obj.e167 == 1)
        ui.e168.setChecked(obj.e168 == 1)
        ui.e169.setChecked(obj.e169 == 1)
        ui.e170.setChecked(obj.e170 == 1)
        self._set_radio_button(ui.e171, obj.e171)
        self._set_radio_button(ui.e172, obj.e172)
        self._set_int_field(ui.e173, obj.e173)
        self._set_radio_button(ui.e174, obj.e174)
        ui.e175.setChecked(obj.e175 == 1)
        ui.e176.setChecked(obj.e176 == 1)
        ui.e177.setChecked(obj.e177 == 1)
        ui.e178.setChecked(obj.e178 == 1)
        ui.e179.setChecked(obj.e179 == 1)
        ui.e180.setChecked(obj.e180 == 1)
        ui.e181.setChecked(obj.e181 == 1)
        self._set_radio_button(ui.e182, obj.e182)
        self._set_radio_button(ui.e183, obj.e183)
        self._set_combobox_selection(ui.e184, obj.e184, -1)
        self._set_combobox_selection(ui.e185, obj.e185)
        self._set_int_field(ui.e186, obj.e186)

