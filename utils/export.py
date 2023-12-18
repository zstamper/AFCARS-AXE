from pathlib import Path

from jinja2 import Environment, select_autoescape, FileSystemLoader

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

    def export(self, e1: str, e2: str, children: list[tuple[BaseChild, Child]]):
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(),
        )
        env.filters['no_null'] = self._no_null
        ooh_template = env.get_template(self.TEMPLATE)
        data = [{'e4': base_child.e4, 'data':child} for base_child, child in children]
        self.outf.write(ooh_template.render(data=data, e1=e1, e2=e2))


class OOHExporter(BaseExporter):
    TEMPLATE = 'template_ooh.xml'


class AExporter(BaseExporter):
    TEMPLATE = 'template_a.xml'


def export_xml(file_name: Path, e1: str, e2: str, report_type: ReportType, selected_children: list[tuple[BaseChild, Child]]):
    if file_name.exists():
        file_name.unlink()
    if report_type == ReportType.OOH:
        OOHExporter(file_name.open("w")).export(e1, e2, selected_children)
    elif report_type == ReportType.A:
        AExporter(file_name).export(e1, e2, selected_children)
