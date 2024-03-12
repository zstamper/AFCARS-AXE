import datetime
import os
import sys
from pathlib import Path

from model import BaseChild, Child, ContextTable
from model.models import ReportType
from .e1 import afcars_to_date
from .id_generator import generate_id


def file_system_directories():
    app_dir = None
    if getattr(sys, 'frozen', False):
        bundle_dir = Path(sys._MEIPASS)
        if sys.platform.startswith('win32'):
            app_dir = Path(sys.executable).parent
        if sys.platform.startswith('darwin'):
            app_dir = Path(sys.executable).parent.parent.parent.parent
    else:
        bundle_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
        app_dir = bundle_dir
    return app_dir, bundle_dir


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
            ContextTable.e2.desc()).first()
        if context:
            base_child.e5 = afcars_to_date(context.data.e5)
            if hasattr(context.data.ooh, 'removals2020'):
                removal = sorted(context.data.ooh.removals2020, key=lambda x: x.e69, reverse=True)
            else:
                removal = sorted(child.ooh.removals2020, key=lambda x: x.e69, reverse=True)
            if removal:
                try:
                    base_child.last_removal = afcars_to_date(removal[0].e69)
                except ValueError:
                    pass
                try:
                    base_child.last_exit = afcars_to_date(removal[0].e153)
                except ValueError:
                    pass
            else:
                if hasattr(context.data.ooh, 'removals1993'):
                    removal = sorted(context.data.ooh.removals1993, key=lambda x: x.e69, reverse=True)
                else:
                    removal = sorted(child.ooh.removals1993, key=lambda x: x.e69, reverse=True)
                if removal:
                    try:
                        base_child.last_removal = afcars_to_date(removal[0].e69)
                    except ValueError:
                        pass
                    try:
                        base_child.last_exit = afcars_to_date(removal[0].e153)
                    except ValueError:
                        pass

    if report_type == ReportType.A:
        try:
            base_child.e5 = datetime.datetime.strptime(str(child.e5), "%Y%m%d").date()
        except ValueError:
            base_child.e5 = None
        base_child.last_adoption = None
        base_child.last_termination = None
        context = ContextTable.select().where(ContextTable.base_child == base_child.id).order_by(
            ContextTable.e2.desc()).first()
        if context:
            try:
                base_child.last_adoption = afcars_to_date(getattr(context.data.a, 'a17', None))
            except ValueError:
                pass
            try:
                base_child.last_termination = afcars_to_date(getattr(context.data.a, 'a18', None))
            except ValueError:
                pass
