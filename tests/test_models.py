import os
import sys

import pytest
from model import open_database, create_tables, close_database, database, ContextTable, Context, ChildTable, Child, \
    OOHRecordTable, OOHRecord, RecognizedTribesTable, TribeTable

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture(scope='session')
def db():
    open_database('test.db')
    create_tables()
    yield database
    close_database()


@pytest.fixture
def context(db):
    with db:
        record = ContextTable.create(e1=1, e2=2)
    yield record
    with db:
        record.delete_instance()


@pytest.fixture
def child(db):
    with db:
        record = ChildTable.create(first_name='Lars',
                                   last_name='Smith',
                                   e4='0123456789AB',
                                   e5=5,
                                   e6=6,
                                   e13=0,
                                   e14=0,
                                   e15=1,
                                   e16=0,
                                   e17=0,
                                   e18=0,
                                   e19=0,
                                   e20=0,
                                   e21=0
                                   )
    yield record
    with db:
        record.delete_instance()


def test_context_model(db, context):
    record = ContextTable.get(ContextTable.e1 == 1, ContextTable.e2 == 2)
    model = record.to_model()
    assert isinstance(model, Context)
    assert model.e1 == 1
    assert model.e2 == 2


def test_child_model(db, child):
    record = ChildTable.get(ChildTable.first_name == child.first_name, ChildTable.last_name == child.last_name)
    model = record.to_model()
    assert isinstance(model, Child)
    assert model.first_name == child.first_name
    assert model.last_name == child.last_name


def test_ooh_model(db, child, context):
    record, _ = OOHRecordTable.get_or_create(child=child, context=context)
    model = record.to_model()
    assert isinstance(model, OOHRecord)
    assert isinstance(model.child, Child)
    assert isinstance(model.context, Context)
    assert model.child.first_name == child.first_name
    assert model.child.last_name == child.last_name
    assert model.context.e1 == context.e1
    assert model.context.e2 == context.e2


def test_edit_child_model(db, child):
    record = ChildTable.get(ChildTable.first_name == child.first_name, ChildTable.last_name == child.last_name)
    model = record.to_model()
    model.e4 = 'BA9876543210'
    ChildTable.persist_model(model)
    record2 = ChildTable.get(ChildTable.first_name == child.first_name, ChildTable.last_name == child.last_name)
    assert record.e4 != record2.e4
    assert record.e4 == '0123456789AB'
    assert record2.e4 == 'BA9876543210'


