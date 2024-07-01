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

from pathlib import Path

from jinja2 import Environment, select_autoescape, FileSystemLoader

import utils
from model.models import ReportType, BaseChild, Child


class BaseExporter:
    TEMPLATE = None

    def __init__(self, outf):
        self.outf = outf

    @staticmethod
    def _no_null(val):
        if val is None:
            return ''
        return val

    @staticmethod
    def e40(ooh):
        if ooh.e39 != 1:
            return 9
        e40 = 0
        for removal in ooh.removals2020:
            for living_arrangement in removal.living_arrangements:
                if living_arrangement.e40 == 1:
                    e40 = 1
                elif e40 != 1 and living_arrangement.e40 == 9:
                    e40 = 9
        return e40

    @staticmethod
    def e58(ooh):
        e112e58_list = [(la.e112, la.e58) for r in ooh.removals2020 for la in r.living_arrangements]
        e58s = sorted(e112e58_list, key=lambda x: x[0], reverse=True)
        if len(e58s) > 0:
            return sorted(e112e58_list, key=lambda x: x[0], reverse=True)[0][1]
        return None

    def export(self, e1: str, e2: str, children: list[tuple[BaseChild, Child]]):
        _, bundle_dir = utils.file_system_directories()
        env = Environment(
            loader=FileSystemLoader(bundle_dir / "templates"),
            autoescape=select_autoescape(),
        )
        env.filters['no_null'] = self._no_null
        env.filters['e40'] = self.e40
        env.filters['e58'] = self.e58
        ooh_template = env.get_template(self.TEMPLATE)
        data = [{'e4': base_child.e4, 'data': child} for base_child, child, error_flag in children]
        self.outf.write(ooh_template.render(data=data, e1=e1, e2=e2))


class OOHExporter(BaseExporter):
    TEMPLATE = 'template_ooh.xml'


class AExporter(BaseExporter):
    TEMPLATE = 'template_assistance.xml'


def export_xml(file_name: Path, e1: str, e2: str, report_type: ReportType,
               selected_children: list[tuple[BaseChild, Child]]):
    if file_name.exists():
        file_name.unlink()
    with file_name.open("w") as outf:
        if report_type == ReportType.OOH:
            OOHExporter(outf).export(e1, e2, selected_children)
        elif report_type == ReportType.A:
            AExporter(outf).export(e1, e2, selected_children)
