import unittest

import pytest
from pydantic import ValidationError

from model import Child, OOHRecord, RecognizedTribe


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
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
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
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E8\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=None, e10=0, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E10\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=0, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=1,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
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
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=9, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[RecognizedTribe(ooh_id=None, e9=None)], second_parents=[], removals1993=[],
            removals2020=[]
        )

    @staticmethod
    def test_e11_e12_is_required_if_e10_is_1():
        with pytest.raises(ValidationError, match=r".*\(E11\).*\(E10\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=0, e10=1, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E12\).*\(E10\).*"):
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=0,
                e7=0, e8=0, e10=1, e11=20200101, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=0,
            e7=0, e8=0, e10=1, e11=20200101, e12=1,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e22():
        with pytest.raises(ValidationError, match=r".*\(E22\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=None, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        with pytest.raises(ValidationError, match=r".*\(E22\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=3, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=1, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e23():
        with pytest.raises(ValidationError, match=r".*\(E23\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=None, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E23\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=4, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=1, e24=1, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
            e31=0, e32=0, e33=0, e34=0, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=2, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=3, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e24_e25_e26_e27_e28_e29_e30_e31_e32_e33_e34():
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E(23|24|25|26|27|28|29|30|31|32|33|34)\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=1, e24=0, e25=0, e26=0, e27=0, e28=0, e29=0, e30=0,
                e31=0, e32=0, e33=0, e34=0, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )
        with pytest.raises(ValidationError, match=r".*\(E23\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=4, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e41_is_required():
        with pytest.raises(ValidationError, match=r".*\(E41\).*"):
            OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=None, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=1, e42=20200101, e43=0, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

        OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=7, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )

    @staticmethod
    def test_e43_is_required_if_e42_is_not_empty():
        pattern = r".*E43.*E42.*"
        with pytest.raises(ValidationError, match=pattern) as excinfo:
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=20200101, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=None, e57=None, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

    @staticmethod
    def test_e57_is_not_greater_than_e56():
        pattern = r".*E57.*E56.*"
        with pytest.raises(ValidationError, match=pattern) as excinfo:
            ooh_record = OOHRecord(
                ooh_id=None, child_id=None, funding=None,
                e7=None, e8=None, e10=None, e11=None, e12=None,
                e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
                e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
                e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
                e51=None, e52=None, e53=None, e54=None, e55=None, e56=1, e57=2, e59=None, e60=None,
                e61=None, e62=None, e63=None, e65=None, e67=None,
                e106=None, e107=None, e108=None, e109=None, e110=None,
                e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
            )

        ooh_record = OOHRecord(
            ooh_id=None, child_id=None, funding=None,
            e7=None, e8=None, e10=None, e11=None, e12=None,
            e22=0, e23=0, e24=None, e25=None, e26=None, e27=None, e28=None, e29=None, e30=None,
            e31=None, e32=None, e33=None, e34=None, e35=None, e36=None, e37=None, e38=None, e39=0,  # e40=None,
            e41=0, e42=None, e43=None, e44=None, e45=None, e46=None, e47=None, e48=None, e49=None, e50=None,
            e51=None, e52=None, e53=None, e54=None, e55=None, e56=1, e57=1, e59=None, e60=None,
            e61=None, e62=None, e63=None, e65=None, e67=None,
            e106=None, e107=None, e108=None, e109=None, e110=None,
            e111=None, tribes=[], second_parents=[], removals1993=[], removals2020=[]
        )
