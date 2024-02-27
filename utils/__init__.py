import datetime

from model import BaseChild, Child, ContextTable
from model.models import ReportType
from .e1 import afcars_to_date
from .id_generator import generate_id


def coalesce(v: str | int | float | None, d: int | float) -> int | float:
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        try:
            return int(v)
        except ValueError:
            try:
                return float(v)
            except ValueError:
                return d
    return d


def refresh_dates(base_child: BaseChild, child: Child, report_type: ReportType):
    if report_type == ReportType.OOH:
        base_child.last_removal = None
        base_child.last_exit = None
        context = ContextTable.select().where(ContextTable.base_child == base_child.id).order_by(
            ContextTable.e2.desc()).get_or_none()
        if context:
            removal = sorted(context.data.ooh.removals2020, key=lambda x: x.e69, reverse=True)
            if removal:
                base_child.last_removal = afcars_to_date(removal[0].e69)
                base_child.last_exit = afcars_to_date(removal[0].e153)
            else:
                removal = sorted(context.data.ooh.removals1993, key=lambda x: x.e69, reverse=True)
                if removal:
                    base_child.last_removal = afcars_to_date(removal[0].e69)
                    base_child.last_exit = afcars_to_date(removal[0].e153)

    if report_type == ReportType.A:
        base_child.e5 = datetime.datetime.strptime(str(child.e5), "%Y%m%d").date()
        base_child.last_adoption = None
        base_child.last_termination = None
        context = ContextTable.select().where(ContextTable.base_child == base_child.id).order_by(
            ContextTable.e2.desc()).get()
        if context:
            base_child.last_adoption = afcars_to_date(context.data.a.a17)
            base_child.last_termination = afcars_to_date(context.data.a.a19)
