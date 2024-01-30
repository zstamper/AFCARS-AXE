import datetime

from PySide6.QtWidgets import QMainWindow
from peewee import DoesNotExist

from controllers.a_controller import AController
from controllers.ooh_controller import OOHController
from dialogs.child_dialog import ChildDialog
from dialogs.main_window2_dialog import ReportType
from model import Context, ContextTable, Child, BaseChildTable
from model.models import FileType, BaseChild, OOHRecord, ARecord


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

        def add_child():
            base_child = controller.base_child
            self.refresh_dates(base_child, controller.child)
            base_child_rec = BaseChildTable.create(e1=base_child.e1, e4=base_child.e4,
                                                   first_name=base_child.first_name, last_name=base_child.last_name,
                                                   date_created=datetime.date.today())
            context.data = controller.child
            ContextTable.create(base_child=base_child_rec, e2=context.e2, file_type=context.file_type,
                                data=context.data)
            self.do_refresh_data()

        controller = None
        if self.report_type == ReportType.OOH:
            controller = OOHController(parent=self.dialog, e1=self.e1)
        elif self.report_type == ReportType.A:
            controller = AController(parent=self.dialog)
        if controller:
            controller.base_child = BaseChild(e1=self.e1, e4="")
            context = Context(e2=self.reporting_period, file_type=self.file_type)
            child = context.data
            if self.report_type == ReportType.OOH:
                child.ooh = OOHRecord()
            elif self.report_type == ReportType.A:
                child.a = ARecord()
            controller.child = child
            controller.on_accept = add_child
            controller.show()

    def do_edit(self, *args, **kwargs):

        def update_child():
            self.refresh_dates(base_child, controller.child)
            BaseChildTable.persist_model(base_child)
            context_rec.base_child = base_child.id
            context_rec.data = controller.child
            context_rec.save()
            self.do_refresh_data()

        base_child = self.dialog.current_child
        if not base_child:
            return
        controller = None
        if self.report_type == ReportType.OOH:
            controller = OOHController(parent=self.dialog, e1=self.e1)
        elif self.report_type == ReportType.A:
            controller = AController(parent=self.dialog)
        if controller:
            context_rec = self._context_for(base_child, self.reporting_period, self.file_type)

            controller.clear()
            controller.base_child = base_child
            controller.child = context_rec.data
            controller.on_accept = update_child
            controller.show()

    def _context_for(self, base_child: BaseChild, reporting_period: str, file_type: FileType) -> ContextTable:
        """Retrieve the indicated context record. If the context doesn't exist, copy the most recent one, and
            if that doesn't exist, just create a new blank one.

            :param base_child: BaseChild - the base child associated with this context
            :param reporting_period: str - the requested reporting period
            :param file_type: FileType - the file type (production or testing)"""
        try:
            context_rec = ContextTable.get(ContextTable.base_child == base_child.id,
                                           ContextTable.e2 == reporting_period,
                                           ContextTable.file_type == file_type)
        except DoesNotExist:
            recent_context = ContextTable.select().where(ContextTable.base_child == base_child.id,
                                                         ContextTable.e2 < reporting_period,
                                                         ContextTable.file_type == file_type).order_by(
                ContextTable.e2.desc()).get_or_none()

            if not recent_context:
                context_rec = ContextTable(e2=self.reporting_period, file_type=self.file_type)
                if self.report_type == ReportType.OOH:
                    context_rec.data = Child(first_name=base_child.first_name, last_name=base_child.last_name,
                                             ooh=OOHRecord())
                elif self.report_type == ReportType.A:
                    context_rec.data = Child(first_name=base_child.first_name, last_name=base_child.last_name,
                                             a=ARecord())
            else:
                context_rec = ContextTable(base_child=recent_context.base_child, e2=recent_context.e2,
                                           file_type=recent_context.file_type, data=recent_context.data)
                if self.report_type == ReportType.OOH and context_rec.data.ooh:
                    context_rec.data.ooh.removals1993 = []
                    context_rec.data.ooh.removals2020 = []

        if self.report_type == ReportType.OOH and not context_rec.data.ooh:
            context_rec.data.ooh = OOHRecord()
        elif self.report_type == ReportType.A and not context_rec.data.a:
            context_rec.data.a = ARecord()

        return context_rec

    def refresh_dates(self, base_child: BaseChild, child: Child):
        if self.report_type == ReportType.OOH:
            dates = []
            if base_child.last_removal:
                dates.append(base_child.last_removal)
            if child.ooh and child.ooh.removals1993:
                for removal in child.ooh.removals1993:
                    if removal.e69:
                        dates.append(datetime.datetime.strptime(str(removal.e69), "%Y%m%d").date())
            if child.ooh and child.ooh.removals2020:
                for removal in child.ooh.removals2020:
                    if removal.e69:
                        dates.append(datetime.datetime.strptime(str(removal.e69), "%Y%m%d").date())
            base_child.last_removal = max(dates) if dates else None

            dates = []
            if base_child.last_exit:
                dates.append(base_child.last_exit)
            if child.ooh and child.ooh.removals1993:
                for removal in child.ooh.removals1993:
                    if removal.e153:
                        dates.append(datetime.datetime.strptime(str(removal.e153), "%Y%m%d").date())
            if child.ooh and child.ooh.removals2020:
                for removal in child.ooh.removals2020:
                    if removal.e153:
                        dates.append(datetime.datetime.strptime(str(removal.e153), "%Y%m%d").date())
            base_child.last_exit = max(dates) if dates else None

        if self.report_type == ReportType.A:
            dates = []
            if base_child.last_adoption:
                dates.append(base_child.last_adoption)
            if child.ooh and child.a:
                if child.a.a17:
                    dates.append(datetime.datetime.strptime(str(child.a.a17), "%Y%m%d").date())
            base_child.last_adoption = max(dates) if dates else None

            dates = []
            if base_child.last_termination:
                dates.append(base_child.last_adoption)
            if child.ooh and child.a:
                if child.a.a18:
                    dates.append(datetime.datetime.strptime(str(child.a.a18), "%Y%m%d").date())
            base_child.last_termination = max(dates) if dates else None
