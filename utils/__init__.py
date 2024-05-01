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

import datetime
import os
import sys
from pathlib import Path
from typing import Any

from model import BaseChild, Child, ContextTable
from model.models import ReportType
from .e1 import afcars_to_date, E2
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


def coalesce(*args, default: Any = None) -> Any:
    for x in args:
        if x is not None:
            return x
    return default


def refresh_dates(base_child: BaseChild, child: Child, report_type: ReportType):
    if report_type == ReportType.OOH:
        base_child.last_removal = None
        base_child.last_exit = None
        context = ContextTable.select().where(ContextTable.base_child == base_child.id).order_by(
            ContextTable.e2.desc()).first()
        if context and context.e2 != E2():
            data = context.data
        else:
            data = child
        base_child.e5 = afcars_to_date(data.e5)
        removal = None
        if hasattr(data.ooh, 'removals2020'):
            removal = sorted(data.ooh.removals2020, key=lambda x: x.e69, reverse=True)
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
            if hasattr(data.ooh, 'removals1993'):
                removal = sorted(data.ooh.removals1993, key=lambda x: x.e69, reverse=True)
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
        if context and context.e2 != E2():
            data = context.data
        else:
            data = child
        try:
            base_child.last_adoption = afcars_to_date(data.a.a17)
        except ValueError:
            pass
        try:
            base_child.last_termination = afcars_to_date(data.a.a18)
        except ValueError:
            pass
