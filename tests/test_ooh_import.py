from pathlib import Path
from xml.etree.ElementTree import Element

import model
import utils.xml_parser

TEST_DATA_FILE_NAME = 'Test Cases Revised v5_Person 01 -Multi-Removals_OOH.xml'


class TestOOHImport:

    def test_parse_file(self):
        tree = utils.xml_parser.parse_file(Path(TEST_DATA_FILE_NAME))
        assert isinstance(tree, Element)

        tree = utils.xml_parser.parse_file(TEST_DATA_FILE_NAME)
        assert isinstance(tree, Element)

        with open(TEST_DATA_FILE_NAME, 'r') as f:
            xml = f.read()
        tree = utils.xml_parser.parse_file(xml)
        assert isinstance(tree, Element)

    def test_import_ooh_tree(self, mocker):
        mocker.patch('model.BaseChildTable.get_or_create').return_value = (model.BaseChildTable(), True)
        mocker.patch('model.BaseChildTable.save')
        mocker.patch('model.ContextTable.get_or_create').return_value = (model.ContextTable(), True)
        mocker.patch('model.ContextTable.save')

        tree = utils.xml_parser.parse_file(TEST_DATA_FILE_NAME)
        assert isinstance(tree, Element)

        utils.xml_parser.import_ooh_tree(tree)

        assert model.BaseChildTable.get_or_create.call_count == 1
        assert model.BaseChildTable.save.call_count == 1
        assert model.ContextTable.get_or_create.call_count == 1
        assert model.ContextTable.save.call_count == 1
