from pathlib import Path
from xml.etree.ElementTree import Element

import model
import utils.xml_parser
from model.models import FileType


class TestAImport:

    def test_parse_file(self):
        tree = utils.xml_parser.parse_file(Path('Test Cases Revised v5_Person 03 - Adopt - Safe Haven_OOH.xml'))
        assert isinstance(tree, Element)

        tree = utils.xml_parser.parse_file('Test Cases Revised v5_Person 03 - Adopt - Safe Haven_OOH.xml')
        assert isinstance(tree, Element)

        with open('Test Cases Revised v5_Person 03 - Adopt - Safe Haven_OOH.xml', 'r') as f:
            xml = f.read()
        tree = utils.xml_parser.parse_file(xml)
        assert isinstance(tree, Element)

    def test_import_a_tree(self, mocker):
        mocker.patch('model.BaseChildTable.get_or_create').return_value = (model.BaseChildTable(), True)
        mocker.patch('model.BaseChildTable.save')
        mocker.patch('model.ContextTable.get_or_create').return_value = (model.ContextTable(), True)
        mocker.patch('model.ContextTable.save')

        tree = utils.xml_parser.parse_file('Test Cases Revised v5_Person 03 - Adopt - Safe Haven_OOH.xml')
        assert isinstance(tree, Element)

        utils.xml_parser.import_a_tree(tree, FileType.TEST)

        assert model.BaseChildTable.get_or_create.call_count == 1
        assert model.BaseChildTable.save.call_count == 1
        assert model.ContextTable.get_or_create.call_count == 1
        assert model.ContextTable.save.call_count == 1
