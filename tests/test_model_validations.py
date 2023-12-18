import datetime

import pytest
from pydantic import ValidationError

from model import Child, OOHRecord, RecognizedTribe, Removal2020


@pytest.fixture
def current_year():
    yield int(datetime.date.today().year)


@pytest.fixture
def current_date():
    today = datetime.date.today()
    yield today.year * 10000 + today.month * 100 + today.day


@pytest.fixture
def current_date_18_years_ago():
    today = datetime.date.today()
    yield (today.year - 18) * 10000 + today.month * 100 + today.day


@pytest.fixture
def as_tribe():
    from utils.e1 import set_E1
    yield set_E1('100')


@pytest.fixture
def as_state():
    from utils.e1 import set_E1
    yield set_E1('10')


@pytest.fixture
def removal2020(current_date, current_date_18_years_ago):
    yield Removal2020(
        ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
        e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
        e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
        e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
        e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
        e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
        e166=0,
        e167=0, e168=0, e169=1, e170=0, e171=0, e172=1, e173=current_date_18_years_ago, e174=1, e175=1,
        e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
        e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
        permanency_hearings=[], case_worker_visits=[]
    )


class TestChildModel:
    @staticmethod
    def test_e4():
        with pytest.raises(ValidationError, match=r".*\(E4\).e*"):
            Child(context_id=0, first_name=None, last_name=None,
                  e4=None, e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="12", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="123", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1234", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="12345", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="123456", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1234567", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None, e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="12345678", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="123456789", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1234567890", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=0
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1234567890A", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=0
                  )

        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )

    @staticmethod
    def test_e5_is_valid():
        with pytest.raises(ValidationError, match=".*e5.*"):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1234567890AB", e5=20202020, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=0
                  )
        with pytest.raises(ValidationError, match=".*e5.*"):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="1234567890AB", e5=20200132, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=0
                  )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200131, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200201, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200228, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200301, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200331, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200401, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200430, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200501, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200531, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200601, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200630, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200701, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200731, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200801, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200831, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200901, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20200930, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20201001, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20201031, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20201101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20201130, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20201201, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="1234567890AB", e5=20201231, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )

    @staticmethod
    def test_e6():
        with pytest.raises(ValidationError, match=r".*\(E6\).*"):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=None, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None, e20=1, e21=0
                  )
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None, e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None, e20=1, e21=0
              )

    @staticmethod
    def test_e6_e38():
        ooh = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=3, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        with pytest.raises(ValidationError, match=r".*\(E38\).*\(E6\).*"):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=2, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None, e20=1, e21=0, ooh=ooh
                  )

        ooh.e38 = 0

        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None, e20=1, e21=0, ooh=ooh
              )

    @staticmethod
    def test_one_of_e13_e14_e15_e16_e17_e18_e19_e20_is_required():
        with pytest.raises(ValidationError, match=r"At least one race must be selected \(E13-E20\)."):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=None, e21=None
                  )
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=0, e17=0, e18=0, e19=0, e20=0, e21=0)

        with pytest.raises(ValidationError,
                           match=r"No additional races may be selected \(E13-E18\) if child is abandoned \(E19\) or race is declined \(E20\)\."):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=1, e13=1, e14=0, e15=0, e16=0, e17=0, e18=0, e19=1, e20=0, e21=0)
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=1, e13=1, e14=0, e15=0, e16=0, e17=0, e18=0, e19=0, e20=1, e21=0)

        with pytest.raises(ValidationError,
                           match=r"Race may be either Abandoned \(E19\) or Declined \(E20\), but not both."):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=0, e17=0, e18=0, e19=1, e20=1, e21=0)

        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=1, e14=0, e15=0, e16=0, e17=0, e18=0, e19=0, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=1, e15=0, e16=0, e17=0, e18=0, e19=0, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=1, e16=0, e17=0, e18=0, e19=0, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=1, e17=0, e18=0, e19=0, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=0, e17=1, e18=0, e19=0, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=0, e17=0, e18=1, e19=0, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=0, e17=0, e18=0, e19=1, e20=0, e21=0)
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=0, e14=0, e15=0, e16=0, e17=0, e18=0, e19=0, e20=1, e21=0)

    # @unittest.expectedFailure
    @staticmethod
    def test_e21_is_required():
        with pytest.raises(ValidationError, match=r"Child's hispanic origin \(E21\) is required\."):
            Child(context_id=0, first_name=None, last_name=None,
                  e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
                  e19=None,
                  e20=1, e21=None
                  )
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=0
              )
        Child(context_id=0, first_name=None, last_name=None,
              e4="0123456789ab", e5=20200101, e6=1, e13=None, e14=None, e15=None, e16=None, e17=None, e18=None,
              e19=None,
              e20=1, e21=1
              )


class TestOOHRecordModel:
    @staticmethod
    def test_e7_e8_e10_is_required_if_funding_is_0():
        with pytest.raises(ValidationError, match=r".*\(E7\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=None, e8=0, e10=0, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E8\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=None, e10=0, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E10\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=0, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=1,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e9_is_required_if_e8_is_1():
        pattern = r".*\(E9\).*\(E8\).*"
        with pytest.raises(ValidationError, match=pattern):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=1, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=9, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[RecognizedTribe(ooh_id=None, e9=None)], second_parents=[], removals1993=[],
            removals2020=[]
        )

    @staticmethod
    def test_e11_e12_is_required_if_e10_is_1(as_tribe):
        # running as a tribe disables some non-applicable checks from mucking without test
        with pytest.raises(ValidationError, match=r".*\(E11\).*\(E10\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=0, e10=1, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E12\).*\(E10\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=0, e10=1, e11=20200101, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=0,
            e7=0, e8=0, e10=1, e11=20200101, e12=1,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e22(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E22\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=None, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E22\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=3, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=1, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e23(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E23\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=None, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E23\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=4, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=1, e24=1, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
            e31=0, e32=0, e33=0, e34=0, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=2, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=3, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e24_e25_e26_e27_e28_e29_e30_e31_e32_e33_e34(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E23\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=4, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e35_is_required(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E35\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=None, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E35\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=6, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
            e31=0, e32=0, e33=0, e34=0, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e36_is_required_if_e35_is_not_0(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E35\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=1, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
            e31=0, e32=0, e33=0, e34=0, e35=2, e36=1, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e37_is_not_null(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E37\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=2, e36=1, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E37\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=2, e36=1, e37=3, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
            e31=0, e32=0, e33=0, e34=0, e35=2, e36=1, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
            e31=0, e32=0, e33=0, e34=0, e35=2, e36=1, e37=1, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e41_is_required(as_tribe):
        with pytest.raises(ValidationError, match=r".*\(E41\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=None, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=1, e42=20200101, e43=0, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e43_is_required_if_e42_is_not_empty(as_tribe):
        pattern = r".*E43.*E42.*"
        with pytest.raises(ValidationError, match=pattern) as excinfo:
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=20200101, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=None, e57=None, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e44_e55():
        # Only e55 needs to be validated

        # Failing tests:
        # e55 is empty
        with pytest.raises(ValueError, match=r".*\(E55\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e57_is_not_greater_than_e56(as_tribe):
        pattern = r".*E57.*E56.*"
        with pytest.raises(ValidationError, match=pattern) as excinfo:
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=2, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e59(as_state):
        # Failing tests:

        # E59 is null
        with pytest.raises(ValidationError, match=r".*\(E59\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=None, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # E59 contains invalid year
        with pytest.raises(ValidationError, match=r".*\(E59\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=0, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

            # Passing tests:
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=2000, e59=0, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e60(current_year, as_state):
        # Failing tests:

        # Invalid date
        with pytest.raises(ValidationError, match=r".*\(E60\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=None,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # Invalid date
        with pytest.raises(ValidationError, match=r".*\(E60\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=0,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # Parent is less than 10 years old
        with pytest.raises(ValidationError, match=r".*\(E60\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 9,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # Parent is more than 100 years old
        with pytest.raises(ValidationError, match=r".*\(E60\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 101,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

            # Passing Tests:
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=9999,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 20,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e61_as_state(current_year, as_state):
        # The rules are confusing. Basically, this field is required if:
        #   Child has a mother (E59 is not 7777)
        #   It's not a tribe that's reporting (E1 is not a tribal code)
        #   There's no tribal IV-E agreement (E104 is not checked)

        # Failing tests

        # Child has a mother
        with pytest.raises(ValidationError, match=r'.*\(E61\).*'):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year, e60=7777,
                e61=None, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # Reporting for a state
        with pytest.raises(ValidationError, match=r'.*\(E61\).*'):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year, e60=7777,
                e61=None, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # E104 is not checked
        with pytest.raises(ValidationError, match=r'.*\(E61\).*'):
            removal2020 = Removal2020(
                ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=0, e105=0, e153=None, e154=None, e155=9, e156=None, e157=None,
                e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
                e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year, e60=7777,
                e61=None, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[removal2020]
            )

        # Passing tests:
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # State is reporting and E104 is checked
        removal2020 = Removal2020(
            ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=None, e154=None, e155=9, e156=None, e157=None,
            e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
            e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[removal2020]
        )

    @staticmethod
    def test_e61_as_tribe(current_year, as_tribe):
        # The rules are confusing. Basically, this field is required if:
        #   Child has a mother (E59 is not 7777)
        #   It's not a tribe that's reporting (E1 is not a tribal code)
        #   There's no tribal IV-E agreement (E104 is not checked)

        # Passing tests:

        # Tribe is reporting and Child has a mother
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # Tribe is reporting and Child has no mother
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # Tribe is reporting and E104 is checked
        removal2020 = Removal2020(
            ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=None, e154=None, e155=9, e156=None, e157=None,
            e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
            e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[removal2020]
        )

    @staticmethod
    def test_e62_as_state(current_year, as_state):
        # The rules are confusing. Basically, this field is required if:
        #   Child has a father (E60 is not 7777 or 9999)
        #   It's not a tribe that's reporting (E1 is not a tribal code)
        #   There's no tribal IV-E agreement (E104 is not checked)

        # Failing tests

        # Child has a father
        with pytest.raises(ValidationError, match=r'.*\(E62\).*'):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18,
                e60=current_year - 18,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # Reporting for a state
        with pytest.raises(ValidationError, match=r'.*\(E62\).*'):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18,
                e60=current_year - 18,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # E104 is not checked
        with pytest.raises(ValidationError, match=r'.*\(E62\).*'):
            removal2020 = Removal2020(
                ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=0, e105=0, e153=None, e154=None, e155=9, e156=None, e157=None,
                e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
                e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18,
                e60=current_year - 18,
                e61=9, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[removal2020]
            )

        # Passing tests:

        # State is reporting and E104 is checked
        removal2020 = Removal2020(
            ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=None, e154=None, e155=9, e156=None, e157=None,
            e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
            e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[removal2020]
        )

        # Father is deceased
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18, e60=9999,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # Father has abandoned
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=current_year - 18, e60=7777,
            e61=9, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e62_as_tribe(current_year, as_tribe):
        # The rules are confusing. Basically, this field is required if:
        #   Child has a father (E60 is not 7777 and not 9999)
        #   It's not a tribe that's reporting (E1 is not a tribal code)
        #   There's no tribal IV-E agreement (E104 is not checked)

        # Passing tests:

        # Tribe is reporting and Child has a father
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 18,
            e61=None, e62=9, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # Tribe is reporting and Child has no father
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # Tribe is reporting and Child has no father
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=9999,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # Tribe is reporting and E104 is checked
        removal2020 = Removal2020(
            ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=None, e154=None, e155=9, e156=None, e157=None,
            e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
            e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 18,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[removal2020]
        )

    @staticmethod
    def test_e63(current_year):
        # Failing test:

        # e63 is None
        with pytest.raises(ValueError, match=r".*\(E63\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 18,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # e63 contains illegal selection
        with pytest.raises(ValueError, match=r".*\(E63\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 18,
                e61=None, e62=None, e63=9, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

            # Passing test
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=current_year - 18,
                e61=None, e62=None, e63=0, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e65(current_date):
        # Failing tests

        # Petition date is required if TPR is indicated
        with pytest.raises(ValueError, match=r".*TPR.*\(E65\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=1, e65=None, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # Passing tests

        # TPR is NA, date is optional
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # TPR is indicated, date is required
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=1, e65=current_date, e67=current_date,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e67(current_date):
        # Failing tests

        # Petition date is required if TPR is indicated
        with pytest.raises(ValueError, match=r".*TPR.*\(E67\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=1, e65=current_date, e67=None,
                e106=0, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        # Passing tests

        # TPR is NA, date is optional
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=0, e65=None, e67=None,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        # TPR is NA, date is optional
        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
            e106=0, e107=None, e108=None, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e106_e108(current_date):
        # Failing tests:
        # Failed to report E106
        with pytest.raises(ValueError, match=r".*\(E106\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
                e106=None, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # E106 is checked, E107 is not
        with pytest.raises(ValueError, match=r".*\(E107\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
                e106=1, e107=None, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # e107 is checked, e108 is empty
        with pytest.raises(ValueError, match=r".*\(E108\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
                e106=1, e107=1, e108=None, e109=0, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # Passing test
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
            e106=1, e107=1, e108=current_date, e109=0, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e109_e111(current_date):
        # Failing tests:
        # Failed to report E109
        with pytest.raises(ValueError, match=r".*\(E109\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
                e106=1, e107=1, e108=current_date, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # E109 is checked, E110 is not
        with pytest.raises(ValueError, match=r".*\(E110\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
                e106=1, e107=1, e108=current_date, e109=1, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # e110 is checked, e111 is empty
        with pytest.raises(ValueError, match=r".*\(E111\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
                e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
                e106=1, e107=0, e108=None, e109=1, e110=1,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        # Passing test
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=0, e36=None, e37=0, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=0, e56=1, e57=1, e59=7777, e60=7777,
            e61=None, e62=None, e63=2, e65=current_date, e67=current_date,
            e106=1, e107=1, e108=current_date, e109=1, e110=1,
            e111=current_date, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )


class TestRemoval2020Model:

    @staticmethod
    def test_removal2020(removal2020):
        # Fails if our base removal record doesn't pass all of the tests.
        Removal2020.model_validate(removal2020)

    @staticmethod
    def test_e3(removal2020):
        # E3 is required
        with pytest.raises(ValueError, match=r".*\(E3\).*"):
            removal2020.e3 = None
            Removal2020.model_validate(removal2020)

        # E3 must be 5 digits
        for fips_code in ['1', '12', '123', '1234', '123456']:
            with pytest.raises(ValueError, match=r".*\(E3\).*"):
                removal2020.e3 = fips_code
                Removal2020.model_validate(removal2020)

        # E3 is present and is exactly 5 digits long
        removal2020.e3 = '12345'
        Removal2020.model_validate(removal2020)

    @staticmethod
    def test_e80_e81_e97(removal2020):
        # Only one of E80, E81, E97 may be checked at a time.
        with pytest.raises(ValueError, match=r"(.*E(80|81|97))+.*"):
            for e80, e81, e97 in [(1, 1, 0), (1, 0, 1), (1, 1, 1), (0, 1, 1)]:
                removal2020.e80 = e80
                removal2020.e81 = e81
                removal2020.e97 = e97
                Removal2020.model_validate(removal2020)

        for e80, e81, e97 in [(0,0,0), (0, 0, 1), (0, 1, 0), (1, 0, 0)]:
            removal2020.e80 = e80
            removal2020.e81 = e81
            removal2020.e97 = e97
            Removal2020.model_validate(removal2020)

    @staticmethod
    def test_e153(current_date):

        # E153 must be after 2022-09-30
        with pytest.raises(ValueError, match=r".*\(E153\).*"):
            Removal2020(
                ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=19990101, e154=None, e155=9, e156=None, e157=None,
                e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
                e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

        # E153 must be after E69
        with pytest.raises(ValueError, match=r".*\(E153\).*\(E69\).*"):
            Removal2020(
                ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=9, e156=None, e157=None,
                e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
                e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

    @staticmethod
    def test_e155(current_date):
        # E155 must be 9 if E153 is null
        with pytest.raises(ValueError, match=r".*\(E155\).*\(E153\).*"):
            Removal2020(
                ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=None, e154=None, e155=1, e156=None, e157=None,
                e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
                e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )
        Removal2020(
            ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=1, e156=None, e157=None,
            e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
            e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )

    @staticmethod
    def test_e156(current_date):
        # E155 must be 9 if E153 is null
        with pytest.raises(ValueError, match=r".*\(E155\).*\(E153\).*"):
            Removal2020(
                ooh_id=None, e3='00000', e69=None, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=None, e154=None, e155=8, e156=None, e157=None,
                e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
                e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )
        Removal2020(
            ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=8, e156=1, e157=None,
            e158=None, e159=None, e160=None, e161=None, e162=None, e163=None, e164=None, e165=None, e166=None,
            e167=None, e168=None, e169=None, e170=None, e171=None, e172=None, e173=None, e174=None, e175=None,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )

    @staticmethod
    def test_e157(current_date, current_date_18_years_ago):
        # E157 is required if e155 is 3 or 5.
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*\(E157\).*\(E155\).*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=None,
                    e158=None, e159=None, e160=None, e161=None, e162=current_date_18_years_ago, e163=None, e164=0,
                    e165=0, e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=None, e172=None, e173=current_date_18_years_ago, e174=1,
                    e175=0,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )
        for e155, e156, e157 in (
                (1, None, None), (2, None, None), (3, None, 1), (4, None, None), (5, None, 1), (6, None, None),
                (7, None, None),
                (8, 1, None), (9, None, None)):
            Removal2020(
                ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=e156, e157=e157,
                e158=None, e159=None, e160=None, e161=None, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
                e166=0,
                e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

    @staticmethod
    def test_e158_e159_e160_e161(current_date, current_date_18_years_ago):

        # When e155 is 3 or 5, at least one of E158-E161 must be selected.
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E158, E159, E160, E161.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=0, e159=0, e160=0, e161=0, e162=None, e163=None, e164=0, e165=0, e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )
        for e155 in (3, 5):
            for e158, e159, e160, e161 in (
                    (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
                    (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0),
                    (1, 1, 1, 1)):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=e158, e159=e159, e160=e160, e161=e161, e162=current_date_18_years_ago, e163=0, e164=0,
                    e165=0, e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

    @staticmethod
    def test_e162(current_date, current_date_18_years_ago):
        # When e155 is 3 or 5, E162 is required
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E162.*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=None, e163=None, e164=0, e165=0, e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )
        for e155, e162 in (
                (1, None), (2, None), (3, current_date_18_years_ago), (4, None), (5, current_date_18_years_ago),
                (6, None),
                (7, None), (8, None), (9, None)):
            Removal2020(
                ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                e158=1, e159=1, e160=1, e161=1, e162=e162, e163=0, e164=0, e165=0, e166=0,
                e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

    @staticmethod
    def test_e163(current_date, current_date_18_years_ago):
        # When e155 is 3 or 5, E163 is required
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E163.*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=None, e164=0, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )
        for e155, e163 in ((1, None), (2, None), (3, 0), (4, None), (5, 0), (6, None), (7, None), (8, None), (9, None)):
            Removal2020(
                ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=e163, e164=0, e165=0,
                e166=0,
                e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

    @staticmethod
    def test_e164_e165_e166_e167_e168_e169_e170(current_date, current_date_18_years_ago):
        # if e155 is 3 or 5, at least one of e164-e170 must be 1.
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E1(64|65|66|67|68|69|70).*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=None, e165=None,
                    e166=None,
                    e167=0, e168=0, e169=0, e170=0, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

        # E155 is 3 or 5, E170 is 1 and at least one other of E164-E169 is one
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E170.*no other.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=1, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
                    e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

        # E155 is 3 or 5 and at least one of e164-170 is 1
        Removal2020(
            ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
            e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
            e166=0,
            e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
            e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )

    @staticmethod
    def test_e171(current_date, current_date_18_years_ago):
        # required if E155 is 3 or 5
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E171.*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=1, e170=0, e171=None, e172=1, e173=None, e174=None, e175=None,
                    e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

        Removal2020(
            ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
            e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
            e166=0,
            e167=0, e168=0, e169=1, e170=0, e171=1, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )

    @staticmethod
    def test_e172(current_date, current_date_18_years_ago):
        # required if E155 is 3 or 5
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E172.*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=1, e170=0, e171=1, e172=None, e173=None, e174=None, e175=None,
                    e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

        Removal2020(
            ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
            e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
            e166=0,
            e167=0, e168=0, e169=1, e170=0, e171=1, e172=1, e173=current_date_18_years_ago, e174=0, e175=1,
            e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )

    @staticmethod
    def test_e173(current_date, current_date_18_years_ago):
        # When e155 is 3 or 5, E162 is required
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E173.*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0, e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=None, e174=None, e175=None,
                    e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )
        for e155, e173 in (
                (1, None), (2, None), (3, current_date_18_years_ago), (4, None), (5, current_date_18_years_ago),
                (6, None),
                (7, None), (8, None), (9, None)):
            Removal2020(
                ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0, e166=0,
                e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=e173, e174=0, e175=1,
                e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

    @staticmethod
    def test_e174(current_date, current_date_18_years_ago):
        # When e155 is 3 or 5, E174 is required
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E174.*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=None,
                    e175=None,
                    e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )
        for e155, e174 in ((1, None), (2, None), (3, 0), (4, None), (5, 0), (6, None), (7, None), (8, None), (9, None)):
            Removal2020(
                ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
                e166=0,
                e167=0, e168=0, e169=0, e170=1, e171=0, e172=1, e173=current_date_18_years_ago, e174=e174, e175=1,
                e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
                e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                permanency_hearings=[], case_worker_visits=[]
            )

    @staticmethod
    def test_e175_e176_e177_e178_e179_e180_e181(current_date, current_date_18_years_ago):
        # if e155 is 3 or 5, at least one of e175-e181 must be 1.
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E1(75|76|77|78|79|80|81).*E155.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=1, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=0, e170=0, e171=0, e172=1, e173=current_date_18_years_ago, e174=0, e175=None,
                    e176=None, e177=None, e178=None, e179=None, e180=None, e181=None, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

        # E155 is 3 or 5, E181 is 1 and at least one other of E175-E180 is one
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E181.*no other.*"):
                Removal2020(
                    ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
                    e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
                    e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
                    e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
                    e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=e155, e156=None, e157=1,
                    e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=1, e165=0,
                    e166=0,
                    e167=0, e168=0, e169=0, e170=0, e171=0, e172=1, e173=current_date_18_years_ago, e174=1, e175=0,
                    e176=0, e177=0, e178=0, e179=0, e180=1, e181=1, e182=0, e183=1, e184=None,
                    e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
                    permanency_hearings=[], case_worker_visits=[]
                )

        # E155 is 3 or 5 and at least one of e164-170 is 1
        Removal2020(
            ooh_id=None, e3='00000', e69=current_date - 1, e70=None, e71=7, e72=0,
            e73=0, e74=0, e75=0, e76=0, e77=0, e78=0, e79=0, e80=0, e81=0, e82=0,
            e83=0, e84=0, e85=0, e86=0, e87=0, e88=0, e89=0, e90=0, e91=0, e92=0,
            e93=0, e94=0, e95=0, e96=0, e97=0, e98=0, e99=0, e100=0, e101=0, e102=0,
            e103=0, e104=1, e105=0, e153=current_date, e154=None, e155=3, e156=None, e157=1,
            e158=1, e159=1, e160=1, e161=1, e162=current_date_18_years_ago, e163=0, e164=0, e165=0,
            e166=0,
            e167=0, e168=0, e169=1, e170=0, e171=0, e172=1, e173=current_date_18_years_ago, e174=1, e175=1,
            e176=0, e177=0, e178=0, e179=0, e180=0, e181=0, e182=0, e183=1, e184=None,
            e185=None, e186=None, living_arrangements=[], permanency_plans=[], periodic_reviews=[],
            permanency_hearings=[], case_worker_visits=[]
        )

    @staticmethod
    def test_e182(removal2020):
        # required if E155 is 3 or 5
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E182.*E155.*"):
                removal2020.e155 = e155
                removal2020.e182 = None
                Removal2020.model_validate(removal2020)

    @staticmethod
    def test_e183(removal2020):
        # required if E155 is 3 or 5
        for e155 in (3, 5):
            with pytest.raises(ValueError, match=r".*E183.*E155.*"):
                removal2020.e155 = e155
                removal2020.e183 = None
                Removal2020.model_validate(removal2020)
