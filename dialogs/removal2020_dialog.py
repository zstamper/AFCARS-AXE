from typing import Optional, Callable

from PySide6.QtWidgets import QWidget, QTableWidgetItem

from . import BaseDialog


def e120_to_str(v: int | None) -> str:
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


def e148_to_str(v: int | None) -> str:
    mapper: dict = {1: "Reunify with parent(s) or legal guardian(s)",
                    2: "Live with other relatives",
                    3: "Adoption",
                    4: "Guardianship",
                    5: "Planned permanent living arrangement"
                    }
    if v is None or v not in mapper:
        return "unknown"
    return mapper[v]


def e152_to_str(v: int | None) -> str:
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
        # self.on_accept: Optional[Callable] = None
        self.living_arrangements = []
        self.permanency_plans = []
        self.periodic_reviews = []
        self.permanency_hearings = []
        self.case_worker_visits = []
        self.id: int | None = None
        self.ooh_id: int | None = None
        self._child_name: str = ""
        self.on_tab_changed: Optional[Callable] = None
        self.on_validate_clicked: Optional[Callable] = None
        self.on_add_living_arrangement: Optional[Callable] = None
        self.on_edit_living_arrangement: Optional[Callable] = None
        self.on_delete_living_arrangement: Optional[Callable] = None
        self.on_add_permanency_plan: Optional[Callable] = None
        self.on_edit_permanency_plan: Optional[Callable] = None
        self.on_delete_permanency_plan: Optional[Callable] = None
        self.on_add_permanency_hearing: Optional[Callable] = None
        self.on_edit_permanency_hearing: Optional[Callable] = None
        self.on_delete_permanency_hearing: Optional[Callable] = None
        self.on_add_case_worker_visit: Optional[Callable] = None
        self.on_edit_case_worker_visit: Optional[Callable] = None
        self.on_delete_case_worker_visit: Optional[Callable] = None
        self.on_add_periodic_review: Optional[Callable] = None
        self.on_edit_periodic_review: Optional[Callable] = None
        self.on_delete_periodic_review: Optional[Callable] = None

    # ------------------------------------------------------------------------

    def clear(self) -> None:
        super().clear()
        self.child_name = ""
        self.ooh_id = None

    def _wire_ui(self) -> None:
        self.setModal(True)

        ui = self.ui
        """add event handlers to the form"""
        ui.form_action.accepted.connect(self.accept)
        ui.form_action.rejected.connect(self.reject)

        ui.living_arrangement_add_button.clicked.connect(self._on_add_living_arrangement)
        ui.living_arrangement_delete_button.clicked.connect(self._on_delete_living_arrangement)
        ui.living_arrangements_table.cellDoubleClicked.connect(self._on_edit_living_arrangement)

        ui.permanency_plan_add_button.clicked.connect(self._on_add_permanency_plan)
        ui.permanency_plan_delete_button.clicked.connect(self._on_delete_permanency_plan)
        ui.permanency_plans_table.cellDoubleClicked.connect(self._on_edit_permanency_plan)

        ui.case_visit_add_button.clicked.connect(self._on_add_case_worker_visit)
        ui.case_visit_edit_button.clicked.connect(self._on_edit_case_worker_visit)
        ui.case_visit_delete_button.clicked.connect(self._on_delete_case_worker_visit)
        ui.case_visits_table.cellDoubleClicked.connect(self._on_edit_case_worker_visit)

        ui.permanency_hearing_add_button.clicked.connect(self._on_add_permanency_hearing)
        ui.permanency_hearing_delete_button.clicked.connect(self._on_delete_permanency_hearing)
        ui.permanency_hearings_table.cellDoubleClicked.connect(self._on_edit_permanency_hearing)

        ui.periodic_review_add_button.clicked.connect(self._on_add_periodic_review)
        ui.periodic_review_delete_button.clicked.connect(self._on_delete_periodic_review)
        ui.periodic_reviews_table.cellDoubleClicked.connect(self._on_edit_periodic_review)

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

        self.ui.validate_button.clicked.connect(self.validate_button_clicked)
        self.ui.tab_widget.currentChanged.connect(self.tab_changed)

    # ----- Living Arrangements Automation ------------------------------------

    def do_validate_button_clicked(self):
        if self.on_validate_clicked:
            self.on_validate_clicked()

    def do_tab_changed(self, new_index: int):
        if self.on_tab_changed:
            self.on_tab_changed(new_index)

    def _on_add_living_arrangement(self, *args, **kwargs) -> None:
        if self.on_add_living_arrangement:
            self.on_add_living_arrangement(self, *args, **kwargs)

    def _on_edit_living_arrangement(self, *args, **kwargs) -> None:
        if self.on_edit_living_arrangement:
            self.on_edit_living_arrangement(self, *args, **kwargs)

    def _on_delete_living_arrangement(self, *args, **kwargs) -> None:
        # if the living_arrangement_table has a current row, delete it from the obj and refresh the table
        if self.on_delete_living_arrangement:
            self.on_delete_living_arrangement(*args, **kwargs)

    @property
    def living_arrangements_current_row(self) -> int:
        return self.ui.living_arrangements_table.currentRow()

    @living_arrangements_current_row.setter
    def living_arrangements_current_row(self, v: int) -> None:
        self.ui.living_arrangements_table.setCurrentRow(v)

    def refresh_living_arrangements(self):
        self.ui.living_arrangements_table.clearContents()
        row = 0
        for data in self.living_arrangements:
            if row >= self.ui.living_arrangements_table.rowCount():
                self.ui.living_arrangements_table.insertRow(row)
            self.ui.living_arrangements_table.setItem(row, 0, QTableWidgetItem(str(data.e112)))
            self.ui.living_arrangements_table.setItem(row, 1, QTableWidgetItem(e120_to_str(data.e120)))
            self.ui.living_arrangements_table.setItem(row, 2, QTableWidgetItem(""))
            row += 1
        max_len: int = len(self.living_arrangements)
        while self.ui.living_arrangements_table.rowCount() > max_len:
            self.ui.living_arrangements_table.removeRow(max_len - 1)

    # ----- Permanency Plan Automation ----------------------------------------

    def _on_add_permanency_plan(self, *args, **kwargs) -> None:
        if self.on_add_permanency_plan:
            self.on_add_permanency_plan(*args, **kwargs)

    def _on_edit_permanency_plan(self, *args, **kwargs) -> None:
        if self.on_edit_permanency_plan:
            self.on_edit_permanency_plan(*args, **kwargs)

    def _on_delete_permanency_plan(self, *args, **kwargs) -> None:
        if self.on_delete_permanency_plan:
            self.on_delete_permanency_plan(*args, **kwargs)

    def refresh_permanency_plans(self):
        row: int = 0
        for data in self.permanency_plans:
            if row >= self.ui.permanency_plans_table.rowCount():
                self.ui.permanency_plans_table.insertRow(row)
            self.ui.permanency_plans_table.setItem(row, 0, QTableWidgetItem(str(data.e147)))
            self.ui.permanency_plans_table.setItem(row, 1, QTableWidgetItem(e148_to_str(data.e148)))
            row += 1
        max_len: int = len(self.permanency_plans)
        while self.ui.permanency_plans_table.rowCount() > max_len:
            self.ui.permanency_plans_table.removeRow(max_len - 1)

    @property
    def permanency_plan_current_row(self) -> int:
        return self.ui.permanency_plans_table.currentRow()

    @permanency_plan_current_row.setter
    def permanency_plan_current_row(self, v: int) -> None:
        self.ui.permanency_plans_table.setCurrentRow(v)

    # ----- Case Visit Automation ---------------------------------------------

    def _on_add_case_worker_visit(self, *args, **kwargs) -> None:
        if self.on_add_case_worker_visit:
            self.on_add_case_worker_visit(*args, **kwargs)

    def _on_edit_case_worker_visit(self, *args, **kwargs) -> None:
        if self.on_edit_case_worker_visit:
            self.on_edit_case_worker_visit(*args, **kwargs)

    def _on_delete_case_worker_visit(self, *args, **kwargs) -> None:
        if self.on_delete_case_worker_visit:
            self.on_delete_case_worker_visit(*args, **kwargs)

    def refresh_case_worker_visits(self):
        row: int = 0
        for data in self.case_worker_visits:
            if row >= self.ui.case_visits_table.rowCount():
                self.ui.case_visits_table.insertRow(row)
            self.ui.case_visits_table.setItem(row, 0, QTableWidgetItem(str(data.e151)))
            self.ui.case_visits_table.setItem(row, 1, QTableWidgetItem(e148_to_str(data.e152)))
            row += 1
        max_len: int = len(self.permanency_plans)
        while self.ui.case_visits_table.rowCount() > max_len:
            self.ui.case_visits_table.removeRow(max_len - 1)

    @property
    def case_worker_visit_current_row(self) -> int:
        return self.ui.case_visits_table.currentRow()

    @case_worker_visit_current_row.setter
    def case_worker_visit_current_row(self, v: int) -> None:
        self.ui.case_visits_table.setCurrentRow(v)

    # ----- Permanency Hearing Automation -------------------------------------

    def _on_add_permanency_hearing(self, *args, **kwargs):
        if self.on_add_permanency_hearing:
            self.on_add_permanency_hearing(*args, **kwargs)

    def _on_edit_permanency_hearing(self, *args, **kwargs):
        if self.on_edit_permanency_hearing:
            self.on_edit_permanency_hearing(*args, **kwargs)

    def _on_delete_permanency_hearing(self, *args, **kwargs):
        if self.on_delete_permanency_hearing:
            self.on_delete_permanency_hearing(*args, **kwargs)

    def refresh_permanency_hearings(self):
        row: int = 0
        for data in self.permanency_hearings:
            if row >= self.ui.permanency_hearings_table.rowCount():
                self.ui.permanency_hearings_table.inserRow(row)
            self.ui.permanency_hearings_table.setItem(row, 0, QTableWidgetItem(str(data.e150)))
            row += 1
        max_len: int = len(self.permanency_hearings)
        while self.ui.permanency_hearings_table.rowCount() > max_len:
            self.ui.permanency_hearings_table.removeRow(max_len - 1)

    @property
    def permanency_hearings_current_row(self) -> int:
        return self.ui.permanency_hearings_table.currentRow()

    @permanency_hearings_current_row.setter
    def permanency_hearings_current_row(self, v: int) -> None:
        self.ui.permanency_hearings_table.setCurrentRow(v)

    # ----- Period Review Automation ------------------------------------------

    def _on_add_periodic_review(self, *args, **kwargs):
        if self.on_add_periodic_review:
            self.on_add_periodic_review(*args, **kwargs)

    def _on_edit_periodic_review(self, *args, **kwargs):
        if self.on_edit_periodic_review:
            self.on_edit_periodic_review(*args, **kwargs)

    def _on_delete_periodic_review(self, *args, **kwargs):
        if self.on_delete_periodic_review:
            self.on_delete_periodic_review(*args, **kwargs)

    def refresh_periodic_reviews(self):
        row: int = 0
        for data in self.periodic_reviews:
            if row >= self.ui.periodic_reviews_table.rowCount():
                self.ui.periodic_reviews_table.insertRow(row)
            self.ui.periodic_reviews_table.setItem(row, 0, QTableWidgetItem(str(data.e149)))
            row += 1
        max_len: int = len(self.periodic_reviews)
        while self.ui.periodic_reviews_table.rowCount() > max_len:
            self.ui.periodic_reviews_table.removeRow(max_len - 1)

    @property
    def periodic_reviews_current_row(self) -> int:
        return self.ui.periodic_reviews_table.currentRow()

    @periodic_reviews_current_row.setter
    def periodic_reviews_current_row(self, v: int) -> None:
        self.ui.periodic_reviews_table.setCurrentRow(v)

    # -------------------------------------------------------------------------
    #                       Form Fields As Properties
    # -------------------------------------------------------------------------

    @property
    def current_tab(self) -> int:
        return self.tabWidget.currentIndex()

    @current_tab.setter
    def current_tab(self, v: int) -> None:
        self.tabWidget.setCurrentIndex(v)

    @property
    def child_name(self) -> str:
        return self._child_name

    @child_name.setter
    def child_name(self, v: str) -> None:
        self._child_name = v
        # print(f"removal2020: child_name={v}")
        if v:
            self.setWindowTitle(f"2020 Removal : {v}")
        else:
            self.setWindowTitle("")

    @property
    def e3(self) -> str | None:
        return self._get_text_field(self.ui.e3)

    @e3.setter
    def e3(self, e3: int) -> None:
        self._set_text_field(self.ui.e3, e3)

    @property
    def e69(self) -> int | None:
        return self._get_int_field(self.ui.e69)

    @e69.setter
    def e69(self, e69: int) -> None:
        self._set_int_field(self.ui.e69, e69)

    @property
    def e70(self) -> int | None:
        return self.e69

    @e70.setter
    def e70(self, v: int | None) -> None:
        pass

    @property
    def e71(self) -> int | None:
        return self._get_combobox_selection(self.ui.e71, 1)

    @e71.setter
    def e71(self, e71) -> None:
        self._set_combobox_selection(self.ui.e71, e71, -1)

    @property
    def e72(self) -> int:
        return 1 if self.ui.e72.isChecked() else 0

    @e72.setter
    def e72(self, e72: int) -> None:
        self.ui.e72.setChecked(e72 == 1)

    @property
    def e73(self) -> int:
        return 1 if self.ui.e73.isChecked() else 0

    @e73.setter
    def e73(self, e73: int) -> None:
        self.ui.e73.setChecked(e73 == 1)

    @property
    def e74(self) -> int:
        return 1 if self.ui.e74.isChecked() else 0

    @e74.setter
    def e74(self, e74: int) -> None:
        self.ui.e74.setChecked(e74 == 1)

    @property
    def e75(self) -> int:
        return 1 if self.ui.e75.isChecked() else 0

    @e75.setter
    def e75(self, e75: int) -> None:
        self.ui.e75.setChecked(e75 == 1)

    @property
    def e76(self) -> int:
        return 1 if self.ui.e76.isChecked() else 0

    @e76.setter
    def e76(self, e76: int) -> None:
        self.ui.e76.setChecked(e76 == 1)

    @property
    def e77(self) -> int:
        return 1 if self.ui.e77.isChecked() else 0

    @e77.setter
    def e77(self, e77: int) -> None:
        self.ui.e77.setChecked(e77 == 1)

    @property
    def e78(self) -> int:
        return 1 if self.ui.e78.isChecked() else 0

    @e78.setter
    def e78(self, e78: int) -> None:
        self.ui.e78.setChecked(e78 == 1)

    @property
    def e79(self) -> int:
        return 1 if self.ui.e79.isChecked() else 0

    @e79.setter
    def e79(self, e79: int) -> None:
        self.ui.e79.setChecked(e79 == 1)

    @property
    def e80(self) -> int:
        return 1 if self.ui.e80.isChecked() else 0

    @e80.setter
    def e80(self, e80: int) -> None:
        self.ui.e80.setChecked(e80 == 1)

    @property
    def e81(self) -> int:
        return 1 if self.ui.e81.isChecked() else 0

    @e81.setter
    def e81(self, e81: int) -> None:
        self.ui.e81.setChecked(e81 == 1)

    @property
    def e82(self) -> int:
        return 1 if self.ui.e82.isChecked() else 0

    @e82.setter
    def e82(self, e82: int) -> None:
        self.ui.e82.setChecked(e82 == 1)

    @property
    def e83(self) -> int:
        return 1 if self.ui.e83.isChecked() else 0

    @e83.setter
    def e83(self, e83: int) -> None:
        self.ui.e83.setChecked(e83 == 1)

    @property
    def e84(self) -> int:
        return 1 if self.ui.e84.isChecked() else 0

    @e84.setter
    def e84(self, e84: int) -> None:
        self.ui.e84.setChecked(e84 == 1)

    @property
    def e85(self) -> int:
        return 1 if self.ui.e85.isChecked() else 0

    @e85.setter
    def e85(self, e85: int) -> None:
        self.ui.e85.setChecked(e85 == 1)

    @property
    def e86(self) -> int:
        return 1 if self.ui.e86.isChecked() else 0

    @e86.setter
    def e86(self, e86: int) -> None:
        self.ui.e86.setChecked(e86 == 1)

    @property
    def e87(self) -> int:
        return 1 if self.ui.e87.isChecked() else 0

    @e87.setter
    def e87(self, e87: int) -> None:
        self.ui.e87.setChecked(e87 == 1)

    @property
    def e88(self) -> int:
        return 1 if self.ui.e88.isChecked() else 0

    @e88.setter
    def e88(self, e88: int) -> None:
        self.ui.e88.setChecked(e88 == 1)

    @property
    def e89(self) -> int:
        return 1 if self.ui.e89.isChecked() else 0

    @e89.setter
    def e89(self, e89: int) -> None:
        self.ui.e89.setChecked(e89 == 1)

    @property
    def e90(self) -> int:
        return 1 if self.ui.e90.isChecked() else 0

    @e90.setter
    def e90(self, e90: int) -> None:
        self.ui.e90.setChecked(e90 == 1)

    @property
    def e91(self) -> int:
        return 1 if self.ui.e91.isChecked() else 0

    @e91.setter
    def e91(self, e91: int) -> None:
        self.ui.e91.setChecked(e91 == 1)

    @property
    def e92(self) -> int:
        return 1 if self.ui.e92.isChecked() else 0

    @e92.setter
    def e92(self, e92: int) -> None:
        self.ui.e92.setChecked(e92 == 1)

    @property
    def e93(self) -> int:
        return 1 if self.ui.e93.isChecked() else 0

    @e93.setter
    def e93(self, e93: int) -> None:
        self.ui.e93.setChecked(e93 == 1)

    @property
    def e94(self) -> int:
        return 1 if self.ui.e94.isChecked() else 0

    @e94.setter
    def e94(self, e94: int) -> None:
        self.ui.e94.setChecked(e94 == 1)

    @property
    def e95(self) -> int:
        return 1 if self.ui.e95.isChecked() else 0

    @e95.setter
    def e95(self, e95: int) -> None:
        self.ui.e95.setChecked(e95 == 1)

    @property
    def e96(self) -> int:
        return 1 if self.ui.e96.isChecked() else 0

    @e96.setter
    def e96(self, e96: int) -> None:
        self.ui.e96.setChecked(e96 == 1)

    @property
    def e97(self) -> int:
        return 1 if self.ui.e97.isChecked() else 0

    @e97.setter
    def e97(self, e97: int) -> None:
        self.ui.e97.setChecked(e97 == 1)

    @property
    def e98(self) -> int:
        return 1 if self.ui.e98.isChecked() else 0

    @e98.setter
    def e98(self, e98: int) -> None:
        self.ui.e98.setChecked(e98 == 1)

    @property
    def e99(self) -> int:
        return 1 if self.ui.e99.isChecked() else 0

    @e99.setter
    def e99(self, e99: int) -> None:
        self.ui.e99.setChecked(e99 == 1)

    @property
    def e100(self) -> int:
        return 1 if self.ui.e100.isChecked() else 0

    @e100.setter
    def e100(self, e100: int) -> None:
        self.ui.e100.setChecked(e100 == 1)

    @property
    def e101(self) -> int:
        return 1 if self.ui.e101.isChecked() else 0

    @e101.setter
    def e101(self, e101: int) -> None:
        self.ui.e101.setChecked(e101 == 1)

    @property
    def e102(self) -> int:
        return 1 if self.ui.e102.isChecked() else 0

    @e102.setter
    def e102(self, e102: int) -> None:
        self.ui.e102.setChecked(e102 == 1)

    @property
    def e103(self) -> int:
        return 1 if self.ui.e103.isChecked() else 0

    @e103.setter
    def e103(self, e103: int) -> None:
        self.ui.e103.setChecked(e103 == 1)

    @property
    def e104(self) -> int:
        return 1 if self.ui.e104.isChecked() else 0

    @e104.setter
    def e104(self, e104: int) -> None:
        self.ui.e104.setChecked(e104 == 1)

    @property
    def e105(self) -> int:
        return 1 if self.ui.e105.isChecked() else 0

    @e105.setter
    def e105(self, e105: int) -> None:
        self.ui.e105.setChecked(e105 == 1)

    @property
    def e153(self) -> int | None:
        return self._get_int_field(self.ui.e153)

    @e153.setter
    def e153(self, e153: int) -> None:
        self._set_int_field(self.ui.e153, e153)

    @property
    def e154(self) -> int | None:
        return self._get_int_field(self.ui.e154)

    @e154.setter
    def e154(self, e154: int) -> None:
        self._set_int_field(self.ui.e154, e154)

    @property
    def e155(self) -> int | None:
        return self._get_combobox_selection(self.ui.e155, 1)

    @e155.setter
    def e155(self, e155: int) -> None:
        self._set_combobox_selection(self.ui.e155, e155, -1)

    @property
    def e156(self) -> int | None:
        return self._get_combobox_selection(self.ui.e156, 1)

    @e156.setter
    def e156(self, e156: int) -> None:
        self._set_combobox_selection(self.ui.e156, e156, -1)

    @property
    def e157(self) -> int | None:
        return self._get_combobox_selection(self.ui.e157, 1)

    @e157.setter
    def e157(self, e157: int) -> None:
        self._set_combobox_selection(self.ui.e157, e157, -1)

    @property
    def e158(self) -> int:
        return 1 if self.ui.e158.isChecked() else 0

    @e158.setter
    def e158(self, e158: int) -> None:
        self.ui.e158.setChecked(e158 == 1)

    @property
    def e159(self) -> int:
        return 1 if self.ui.e159.isChecked() else 0

    @e159.setter
    def e159(self, e159: int) -> None:
        self.ui.e159.setChecked(e159 == 1)

    @property
    def e160(self) -> int:
        return 1 if self.ui.e160.isChecked() else 0

    @e160.setter
    def e160(self, e160: int) -> None:
        self.ui.e160.setChecked(e160 == 1)

    @property
    def e161(self) -> int:
        return 1 if self.ui.e161.isChecked() else 0

    @e161.setter
    def e161(self, e161: int) -> None:
        self.ui.e161.setChecked(e161 == 1)

    @property
    def e162(self) -> int | None:
        return self._get_int_field(self.ui.e162)

    @e162.setter
    def e162(self, e162: int) -> None:
        self._set_int_field(self.ui.e162, e162)

    @property
    def e163(self) -> int:
        return self._get_radio_button(self.ui.e163)

    @e163.setter
    def e163(self, e163: int) -> None:
        self._set_radio_button(self.ui.e163, e163)

    @property
    def e164(self) -> int:
        return 1 if self.ui.e164.isChecked() else 0

    @e164.setter
    def e164(self, e164: int) -> None:
        self.ui.e164.setChecked(e164 == 1)

    @property
    def e165(self) -> int:
        return 1 if self.ui.e165.isChecked() else 0

    @e165.setter
    def e165(self, e165: int) -> None:
        self.ui.e165.setChecked(e165 == 1)

    @property
    def e166(self) -> int:
        return 1 if self.ui.e166.isChecked() else 0

    @e166.setter
    def e166(self, e166: int) -> None:
        self.ui.e166.setChecked(e166 == 1)

    @property
    def e167(self) -> int:
        return 1 if self.ui.e167.isChecked() else 0

    @e167.setter
    def e167(self, e167: int) -> None:
        self.ui.e167.setChecked(e167 == 1)

    @property
    def e168(self) -> int:
        return 1 if self.ui.e168.isChecked() else 0

    @e168.setter
    def e168(self, e168: int) -> None:
        self.ui.e168.setChecked(e168 == 1)

    @property
    def e169(self) -> int:
        return 1 if self.ui.e169.isChecked() else 0

    @e169.setter
    def e169(self, e169: int) -> None:
        self.ui.e169.setChecked(e169 == 1)

    @property
    def e170(self) -> int:
        return 1 if self.ui.e170.isChecked() else 0

    @e170.setter
    def e170(self, e170: int) -> None:
        self.ui.e170.setChecked(e170 == 1)

    @property
    def e171(self) -> int:
        return self._get_radio_button(self.ui.e171)

    @e171.setter
    def e171(self, e171: int) -> None:
        self._set_radio_button(self.ui.e171, e171)

    @property
    def e172(self) -> None:
        return self._get_radio_button(self.ui.e172)

    @e172.setter
    def e172(self, e172: int) -> None:
        self._set_radio_button(self.ui.e172, e172)

    @property
    def e173(self) -> int | None:
        return self._get_int_field(self.ui.e173)

    @e173.setter
    def e173(self, e173: int) -> None:
        self._set_int_field(self.ui.e173, e173)

    @property
    def e174(self) -> int:
        return self._get_radio_button(self.ui.e174)

    @e174.setter
    def e174(self, e174) -> None:
        self._set_radio_button(self.ui.e174, e174)

    @property
    def e175(self) -> int:
        return 1 if self.ui.e175.isChecked() else 0

    @e175.setter
    def e175(self, e175: int) -> None:
        self.ui.e175.setChecked(e175 == 1)

    @property
    def e176(self) -> int:
        return 1 if self.ui.e176.isChecked() else 0

    @e176.setter
    def e176(self, e176: int) -> None:
        self.ui.e176.setChecked(e176 == 1)

    @property
    def e177(self) -> int:
        return 1 if self.ui.e177.isChecked() else 0

    @e177.setter
    def e177(self, e177: int) -> None:
        self.ui.e177.setChecked(e177 == 1)

    @property
    def e178(self) -> int:
        return 1 if self.ui.e178.isChecked() else 0

    @e178.setter
    def e178(self, e178: int) -> None:
        self.ui.e178.setChecked(e178 == 1)

    @property
    def e179(self) -> int:
        return 1 if self.ui.e179.isChecked() else 0

    @e179.setter
    def e179(self, e179: int) -> None:
        self.ui.e179.setChecked(e179 == 1)

    @property
    def e180(self) -> int:
        return 1 if self.ui.e180.isChecked() else 0

    @e180.setter
    def e180(self, e180: int) -> None:
        self.ui.e180.setChecked(e180 == 1)

    @property
    def e181(self) -> int:
        return 1 if self.ui.e181.isChecked() else 0

    @e181.setter
    def e181(self, e181: int) -> None:
        self.ui.e181.setChecked(e181 == 1)

    @property
    def e182(self) -> int:
        return self._get_radio_button(self.ui.e182)

    @e182.setter
    def e182(self, e182: int) -> None:
        self._set_radio_button(self.ui.e182, e182)

    @property
    def e183(self) -> int:
        return self._get_radio_button(self.ui.e183)

    @e183.setter
    def e183(self, e183: int) -> None:
        self._set_radio_button(self.ui.e183, e183)

    @property
    def e184(self) -> int | None:
        return self._get_combobox_selection(self.ui.e184, 1)

    @e184.setter
    def e184(self, e184: int) -> None:
        self._set_combobox_selection(self.ui.e184, e184, -1)

    @property
    def e185(self) -> int | None:
        return self._get_combobox_selection(self.ui.e185)

    @e185.setter
    def e185(self, e185: int) -> None:
        self._set_combobox_selection(self.ui.e185, e185)

    @property
    def e186(self) -> int | None:
        return self._get_int_field(self.ui.e186)

    @e186.setter
    def e186(self, e186: int) -> None:
        self._set_int_field(self.ui.e186, e186)
