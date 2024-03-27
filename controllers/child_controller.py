import datetime

from PySide6.QtWidgets import QMainWindow, QMessageBox
from peewee import DoesNotExist

from controllers.a_controller import AController
from controllers.ooh_controller import OOHController
from dialogs.child_dialog import ChildDialog
from dialogs.main_window2_dialog import ReportType
from model import Context, ContextTable, Child, BaseChildTable
from model.models import FileType, BaseChild, OOHRecord, ARecord
from utils import refresh_dates


class ChildController:

    def __init__(self, parent: QMainWindow | None = None):
        self.dialog: ChildDialog = ChildDialog(parent)
        self.dialog.window_title = ""

        self.agency_name: str = ""
        self.e1: str = ""
        self.reporting_period: str = ""
        self.report_type: ReportType = ReportType.OOH
        self.file_type: FileType = FileType.PRODUCTION
        self.context: Context | None = None

        self.dialog.on_add = self.do_add
        self.dialog.on_edit = self.do_edit
        self.dialog.on_delete = self.do_delete
        self.dialog.on_refresh_data = self.do_refresh_data

    def show(self):
        self.dialog.reporting_period_choices = self.get_reporting_periods()
        self.dialog.agency_name = self.agency_name
        self.dialog.agency_code = self.e1
        self.dialog.file_type = self.file_type
        self.dialog.report_type = self.report_type
        self.dialog.reporting_period = self.reporting_period
        self.do_refresh_data()
        self.dialog.exec_()

    def fetch_child_data(self) -> list[Child]:
        report_type = self.dialog.report_type_filter
        reporting_period = self.dialog.reporting_period_filter
        if reporting_period != 'Any':
            reporting_period = f"{reporting_period[0:4]}{'03' if reporting_period.endswith('A') else '09'}"
        query = (BaseChildTable
                 .select()
                 .join(ContextTable)
                 .where(BaseChildTable.e1 == self.e1)
                 .order_by(BaseChildTable.last_name, BaseChildTable.first_name).distinct())
        query = query.where(ContextTable.file_type == self.file_type)
        if report_type == ReportType.A:
            query = query.where(ContextTable.data['a'].is_null(False))
        if report_type == ReportType.OOH:
            query = query.where(ContextTable.data['ooh'].is_null(False))
        if reporting_period != 'Any':
            query = query.where(ContextTable.e2 == reporting_period)
        return [BaseChild.crib(row) for row in query]

    def do_refresh_data(self):
        self.dialog.child_data = self.fetch_child_data()

    @staticmethod
    def get_reporting_periods() -> list[str]:
        return [f"{year}{period}" for year in range(2023, 2036) for period in ['A', 'B']]

    def do_add(self):

        def save():
            nonlocal controller, context
            # the child's birthdate needs to bubble up to the base child table so that it can show up
            # in the child listing. Don't forget, e5 in the child model is an int, while in the base_child
            # table it's a date.
            base_child = controller.base_child
            if controller.base_child_rec_id != 0 and controller.context_rec_id != 0:
                context_rec = ContextTable.get_by_id(controller.context_rec_id)
                self.do_edit_save(base_child, controller, context_rec)
                return

            base_child.e5 = datetime.datetime.strptime(str(controller.child.e5),
                                                       "%Y%m%d") if controller.child.e5 else None
            refresh_dates(base_child, controller.child, self.report_type)
            base_child_rec = BaseChildTable.create(e1=base_child.e1, e4=base_child.e4, e5=controller.child.e5,
                                                   first_name=base_child.first_name, last_name=base_child.last_name,
                                                   date_created=datetime.date.today(), last_exit=base_child.last_exit,
                                                   last_removal=base_child.last_removal,
                                                   last_adoption=base_child.last_adoption,
                                                   last_termination=base_child.last_termination)
            controller.base_child_rec_id = base_child_rec.id
            base_child.id = base_child_rec.id
            context.data = controller.child
            new_context = ContextTable.create(base_child=base_child_rec, e2=context.e2, file_type=context.file_type,
                                              data=context.data)
            controller.context_rec_id = new_context.id
            context.id = new_context.id
            self.do_refresh_data()

        controller = None
        if self.report_type == ReportType.OOH:
            controller = OOHController(self.dialog, self.e1, file_type=self.file_type)
        elif self.report_type == ReportType.A:
            controller = AController(self.dialog, file_type=self.file_type)
        if controller:
            controller.base_child = BaseChild(e1=self.e1, e4="")
            context = Context(e2=self.reporting_period, file_type=self.file_type)
            controller.base_child_rec_id = 0
            controller.context_rec_id = 0
            child = context.data
            if self.report_type == ReportType.OOH:
                child.ooh = OOHRecord()
            elif self.report_type == ReportType.A:
                child.a = ARecord()
            controller.child = child
            controller.on_save = save
            controller.exec()

    def do_edit_save(self, base_child: BaseChild, controller: OOHController | AController, context_rec: ContextTable):
        # the child's birthdate needs to bubble up to the base child table so that it can show up
        # in the child listing.
        refresh_dates(base_child, controller.child, self.report_type)
        base_child.e5 = datetime.datetime.strptime(str(controller.child.e5),
                                                   "%Y%m%d") if controller.child.e5 else None
        BaseChildTable.persist_model(base_child)
        context_rec.base_child = base_child.id
        context_rec.data = controller.child
        context_rec.save()
        self.do_refresh_data()

    def do_edit(self, *args, **kwargs):

        def save():
            self.do_edit_save(base_child, controller, context_rec)

        base_child = self.dialog.current_child
        if not base_child:
            return
        controller = None
        if self.report_type == ReportType.OOH:
            controller = OOHController(self.dialog, self.e1, file_type=self.file_type)
        elif self.report_type == ReportType.A:
            controller = AController(self.dialog, file_type=self.file_type)
        if controller:
            context_rec = self._context_for(base_child, self.reporting_period, self.file_type)
            if self.report_type == ReportType.OOH and not context_rec.data.ooh:
                context_rec.data.ooh = OOHRecord()
            if self.report_type == ReportType.A and not context_rec.data.a:
                context_rec.data.a = ARecord()
            controller.clear()
            controller.base_child_rec_id = base_child.id
            controller.context_rec_id = context_rec.id
            controller.base_child = base_child
            controller.child = context_rec.data
            controller.on_save = save
            controller.exec()

    def do_delete(self):
        base_child = self.dialog.current_child
        if not base_child:
            return
        if QMessageBox.question(self.dialog, "Delete",
                                "Are you sure you want to delete this record?") == QMessageBox.Yes:
            context_rec = self._context_for(base_child, self.reporting_period, self.file_type)
            if context_rec.data is None:        # an early bug allowed for invalid data in the database; this allows one to delete it safely.
                context_rec.delete_instance()
            else:
                if self.report_type == ReportType.OOH:
                    context_rec.data.ooh = None
                elif self.report_type == ReportType.A:
                    context_rec.data.a = None
                if context_rec.data.ooh is None and context_rec.data.a is None:
                    context_rec.delete_instance()
                else:
                    context_rec.save()
            self.do_refresh_data()

    def _context_for(self, base_child: BaseChild, reporting_period: str, file_type: FileType) -> ContextTable:
        """Retrieve the indicated context record. If the context doesn't exist, copy the most recent one, and
            if that doesn't exist, just create a new blank one.

            :param base_child: BaseChild - the base child associated with this context
            :param reporting_period: str - the requested reporting period
            :param file_type: FileType - the file type (production or testing)"""
        context_rec, is_new = ContextTable.get_or_create(base_child=base_child.id,
                                                         e2=reporting_period,
                                                         file_type=file_type)
        if not is_new:
            if self.report_type == ReportType.OOH and not context_rec.data.ooh:
                context_rec.data.ooh = OOHRecord()
            elif self.report_type == ReportType.A and not context_rec.data.a:
                context_rec.data.a = ARecord()
        else:
            recent_context = ContextTable.select().where(ContextTable.base_child == base_child.id,
                                                         ContextTable.e2 < reporting_period,
                                                         ContextTable.file_type == file_type).order_by(
                ContextTable.e2.desc()).get_or_none()
            if recent_context:
                context_rec.data = recent_context.data
            else:
                child = Child(first_name=base_child.first_name, last_name=base_child.last_name)
                child.ooh = OOHRecord()
                child.a = ARecord()
                context_rec.data = child
            context_rec.save()
        return context_rec
