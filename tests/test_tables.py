# import os
# import sys
#
# import pytest
#
# import model
# from model import open_database, create_tables, close_database, database, ContextTable, Context, Child, \
#     OOHRecord, ARecord, SecondParent, Removal1993, Removal2020, LivingArrangement, \
#     PermanencyPlan, PeriodicReview, PermanencyHearing, CaseVisit
#
#
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#
#
# @pytest.fixture(scope='session')
# def db():
#     open_database('test.db')
#     create_tables()
#     yield database
#     close_database()
#
#
# @pytest.fixture
# def context(db):
#     with db:
#         record = ContextTable.create(e1=100)
#         assert record.id is not None
#     yield record
#     with db:
#         record.delete_instance()
#
#
# @pytest.fixture
# def child(db, context):
#     with db:
#         record = Child(first_name='Lars',
#                                    last_name='Smith',
#                                    context=context,
#                                    e4='0123456789AB',
#                                    e5=20200101,
#                                    e6=1,
#                                    e13=0,
#                                    e14=0,
#                                    e15=1,
#                                    e16=0,
#                                    e17=0,
#                                    e18=0,
#                                    e19=0,
#                                    e20=0,
#                                    e21=0
#                                    )
#         assert record.context is not None
#     yield record
#     with db:
#         record.delete_instance()
#
#
# def test_context_model(db, context):
#     record = ContextTable.get(ContextTable.e1 == 100)
#     model = record.to_model()
#     assert isinstance(model, Context)
#     assert model.e1 == 100
#
#
# def test_child_model(db, child):
#     record = ChildTable.get(ChildTable.first_name == child.first_name, ChildTable.last_name == child.last_name)
#     model = record.to_model()
#     assert isinstance(model, Child)
#     assert model.first_name == child.first_name
#     assert model.last_name == child.last_name
#
#
# def test_ooh_model(db, child):
#     record, _ = OOHRecordTable.get_or_create(child=child)
#     model = record.to_model()
#     assert isinstance(model, OOHRecord)
#     record.delete_instance()
#
#
# def test_edit_child_model(db, child, mocker):
#     mocker.patch('model.ChildTable.save')
#     record = ChildTable.get(ChildTable.first_name == child.first_name, ChildTable.last_name == child.last_name)
#     model = record.to_model()
#     model.e4 = 'BA9876543210'
#     assert model.context_id is not None
#     model.context_id = child.context_id
#     ChildTable.persist_model(model)
#     model.ChildTable.save.assert_called_once()
#
#
# def test_persist_fully_populated_child_model(db, context, mocker):
#     mocker.patch('model.ChildTable.save')
#     mocker.patch('model.ARecordTable.save')
#     mocker.patch('model.OOHRecordTable.save')
#     mocker.patch('model.SecondParentTable.save')
#     mocker.patch('model.Removal1993Table.save')
#     mocker.patch('model.Removal2020Table.save')
#     mocker.patch('model.LivingArrangementTable.save')
#     mocker.patch('model.PermanencyPlanTable.save')
#     mocker.patch('model.PeriodicReviewTable.save')
#     mocker.patch('model.PermanencyHearingTable.save')
#     mocker.patch('model.CaseWorkerVisitTable.save')
#
#     tribes = []
#     second_parents = [
#         SecondParent(id=None, ooh_id=None, e64=None, e66=None, e68=None)
#     ]
#
#     removals1993 = [
#         Removal1993(id=None, ooh_id=None, e69=20200101, e153=20200102, e155=1)
#     ]
#
#     living_arrangements = [
#         LivingArrangement(id=None, removal_id=None,
#                           e40=None,
#                           e58=None,
#                           e112=None, e113=None, e114=None,
#                           e115=None, e116=None, e117=None, e118=None, e119=None,
#                           e120=None, e121=None, e122=None, e123=None, e124=None,
#                           e125=None, e126=None, e127=None, e128=None, e129=None,
#                           e130=None, e131=None, e132=None, e133=None, e134=None,
#                           e135=None, e136=None, e137=None, e138=None, e139=None,
#                           e140=None, e141=None, e142=None, e143=None, e144=None,
#                           e145=None, e146=None)
#     ]
#
#     permanency_plans = [
#         PermanencyPlan(id=None, removal_id=None, e147=None, e148=None),
#         PermanencyPlan(id=None, removal_id=None, e147=None, e148=None),
#         PermanencyPlan(id=None, removal_id=None, e147=None, e148=None)
#     ]
#
#     periodic_reviews = [
#         PeriodicReview(id=None, removal_id=None, e149=None),
#         PeriodicReview(id=None, removal_id=None, e149=None),
#         PeriodicReview(id=None, removal_id=None, e149=None)
#     ]
#
#     permanency_hearings = [
#         PermanencyHearing(id=None, removal_id=None, e150=None),
#         PermanencyHearing(id=None, removal_id=None, e150=None),
#         PermanencyHearing(id=None, removal_id=None, e150=None)
#     ]
#
#     case_worker_visits = [
#         CaseVisit(id=None, removal_id=None, e151=None, e152=None),
#         CaseVisit(id=None, removal_id=None, e151=None, e152=None),
#         CaseVisit(id=None, removal_id=None, e151=None, e152=None)
#     ]
#
#     removals2020 = [
#         Removal2020(id=None, ooh_id=None,
#                     e3=None,
#                     e69=None,
#                     e70=None, e71=None, e72=None, e73=None, e74=None,
#                     e75=None, e76=None, e77=None, e78=None, e79=None,
#                     e80=None, e81=None, e82=None, e83=None, e84=None,
#                     e85=None, e86=None, e87=None, e88=None, e89=None,
#                     e90=None, e91=None, e92=None, e93=None, e94=None,
#                     e95=None, e96=None, e97=None, e98=None, e99=None,
#                     e100=None, e101=None, e102=None, e103=None, e104=None,
#                     e105=None,
#                     e153=None, e154=None,
#                     e155=1, e156=None, e157=None, e158=None, e159=None,
#                     e160=None, e161=None, e162=None, e163=None, e164=None,
#                     e165=None, e166=None, e167=None, e168=None, e169=None,
#                     e170=None, e171=None, e172=None, e173=None, e174=None,
#                     e175=None, e176=None, e177=None, e178=None, e179=None,
#                     e180=None, e181=None, e182=None, e183=None, e184=None,
#                     e185=None, e186=None,
#                     living_arrangements=living_arrangements,
#                     permanency_plans=permanency_plans,
#                     periodic_reviews=periodic_reviews,
#                     permanency_hearings=permanency_hearings,
#                     case_worker_visits=case_worker_visits,
#                     )
#     ]
#
#     ooh = OOHRecord(id=None, child_id=None, funding=None,
#                     e7=None, e8=None,
#                     e10=None, e11=None, e12=None,
#                     e22=None, e23=None, e24=None,
#                     e25=None, e26=None, e27=None, e28=None, e29=None,
#                     e30=None, e31=None, e32=None, e33=None, e34=None,
#                     e35=None, e36=None, e37=None, e38=None, e39=None,
#                     e41=None, e42=None, e43=None, e44=None,
#                     e45=None, e46=None, e47=None, e48=None, e49=None,
#                     e50=None, e51=None, e52=None, e53=None, e54=None,
#                     e55=None, e56=None, e57=None, e58=None, e59=None,
#                     e60=None, e61=None, e62=None, e63=None,
#                     e65=None, e67=None,
#                     e106=None, e107=None, e108=None, e109=None,
#                     e110=None, e111=None,
#                     second_parents=second_parents,
#                     removals1993=removals1993,
#                     removals2020=removals2020)
#
#     a = ARecord(id=None, child_id=None,
#                 a15=None, a16=None, a17=None, a18=None, a19=None)
#
#     child = Child(id=None,
#                   context_id=context.id,
#                   first_name=None, last_name=None,
#                   e4=None,
#                   e5=None, e6=None,
#                   e13=None, e14=None,
#                   e15=None, e16=None, e17=None, e18=None, e19=None,
#                   e20=None, e21=None,
#                   ooh=ooh, a=a)
#
#     ChildTable.persist_model(child)
#
#     assert model.ChildTable.save.call_count == 1
#     assert model.OOHRecordTable.save.call_count == 1
#     assert model.ARecordTable.save.call_count == 1
#     assert model.SecondParentTable.save.call_count == len(second_parents)
#     assert model.Removal1993Table.save.call_count == len(removals1993)
#     assert model.Removal2020Table.save.call_count == len(removals2020)
#     for removal in removals2020:
#         assert model.LivingArrangementTable.save.call_count == len(removal.living_arrangements)
#         assert model.PermanencyPlanTable.save.call_count == len(removal.permanency_plans)
#         assert model.PeriodicReviewTable.save.call_count == len(removal.periodic_reviews)
#         assert model.PermanencyHearingTable.save.call_count == len(removal.permanency_hearings)
#         assert model.CaseWorkerVisitTable.save.call_count == len(removal.case_worker_visits)
