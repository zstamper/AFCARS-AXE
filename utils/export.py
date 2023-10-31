from pathlib import Path
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from peewee import JOIN

from model import OOHRecordTable, ContextTable, ChildTable, SecondParentTable, Removal1993Table, Removal2020Table, \
    LivingArrangementTable, PermanencyPlanTable, PeriodicReviewTable, PermanencyHearingTable, CaseWorkerVisitTable, \
    ARecordTable


class XMLExporter:

    def __init__(self, file_path: Path):
        self.file_path = file_path

    @staticmethod
    def _no_null(val):
        if val is None:
            return ''
        return val

    def export(self, e2: str):
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(),
        )
        env.filters['no_null'] = self._no_null
        base_path = Path(self.file_path)

        ooh_filepath = base_path.with_name(f"{base_path.stem}.ooh{base_path.suffix}")
        ooh_filepath.unlink(True)
        ooh_template = env.get_template('template_ooh.xml')
        ooh_query = (OOHRecordTable.select()
                     .join(ChildTable)
                     .switch(OOHRecordTable).join(SecondParentTable, JOIN.LEFT_OUTER)
                     .switch(OOHRecordTable).join(Removal1993Table, JOIN.LEFT_OUTER)
                     .switch(OOHRecordTable).join(Removal2020Table, JOIN.LEFT_OUTER)
                     .join(LivingArrangementTable, JOIN.LEFT_OUTER)
                     .switch(Removal2020Table).join(PermanencyPlanTable, JOIN.LEFT_OUTER)
                     .switch(Removal2020Table).join(PeriodicReviewTable, JOIN.LEFT_OUTER)
                     .switch(Removal2020Table).join(PermanencyHearingTable, JOIN.LEFT_OUTER)
                     .switch(Removal2020Table).join(CaseWorkerVisitTable, JOIN.LEFT_OUTER)
                     )
        context_record = ContextTable.select().first()
        with ooh_filepath.open("w") as outf:
            outf.write(ooh_template.render(
                data=ooh_query,
                context=context_record,
                e2=e2))

        a_filepath = base_path.with_name(f"{base_path.stem}.a{base_path.suffix}")
        a_filepath.unlink(True)
        a_template = env.get_template('template_assistance.xml')
        a_query = (ARecordTable.select()
                   .join(ChildTable))
        with a_filepath.open("w") as outf:
            outf.write(a_template.render(
                data=a_query,
                context=context_record,
                e2=e2))



def export_xml(filename: str, ooh_data: dict, a_data: dict):
    def no_null(val):
        if val is None:
            return ''
        return val

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(),
    )
    env.filters['no_null'] = no_null
    filepath = Path(f"{filename}_OOH.xml")
    filepath.unlink(True)
    if 'records' in ooh_data and len(ooh_data['records']) > 0:
        template = env.get_template('template_ooh.xml')
        with filepath.open("w") as outf:
            outf.write(template.render(data=ooh_data))
    filepath = Path(f"{filename}_A.xml")
    filepath.unlink(True)
    if 'records' in a_data and len(a_data['records']) > 0:
        template = env.get_template('template_assistance.xml')
        with filepath.open("w") as outf:
            outf.write(template.render(data=a_data))
