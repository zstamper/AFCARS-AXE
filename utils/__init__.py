import datetime

from model import BaseChild, Child, ContextTable
from model.models import ReportType
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
        base_child.e5 = datetime.datetime.strptime(str(child.e5), "%Y%m%d").date()
        dates = []
        for context in ContextTable.select().where(ContextTable.base_child_id == base_child.id):
            if hasattr(context.data, 'ooh') and hasattr(context.data.ooh, 'removals1993'):
                for removal in context.data.ooh.removals1993:
                    if removal.e69:
                        dates.append(datetime.datetime.strptime(str(removal.e69), "%Y%m%d").date())
            if hasattr(context.data, 'ooh') and hasattr(context.data.ooh, 'removals2020'):
                for removal in context.data.ooh.removals2020:
                    if removal.e69:
                        dates.append(datetime.datetime.strptime(str(removal.e69), "%Y%m%d").date())
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
        for context in ContextTable.select().where(ContextTable.base_child_id == base_child.id):
            if hasattr(context.data, 'ooh') and hasattr(context.data.ooh, 'removals1993'):
                for removal in context.data.ooh.removals1993:
                    if removal.e153:
                        dates.append(datetime.datetime.strptime(str(removal.e69), "%Y%m%d").date())
            if hasattr(context.data, 'ooh') and hasattr(context.data.ooh, 'removals2020'):
                for removal in context.data.ooh.removals2020:
                    if removal.e153:
                        dates.append(datetime.datetime.strptime(str(removal.e69), "%Y%m%d").date())
        if child.ooh and child.ooh.removals1993:
            for removal in child.ooh.removals1993:
                if removal.e153:
                    dates.append(datetime.datetime.strptime(str(removal.e153), "%Y%m%d").date())
        if child.ooh and child.ooh.removals2020:
            for removal in child.ooh.removals2020:
                if removal.e153:
                    dates.append(datetime.datetime.strptime(str(removal.e153), "%Y%m%d").date())
        base_child.last_exit = max(dates) if dates else None

    if report_type == ReportType.A:
        base_child.e5 = datetime.datetime.strptime(str(child.e5), "%Y%m%d").date()
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
