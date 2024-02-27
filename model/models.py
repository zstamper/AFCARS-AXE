import re
from datetime import datetime, date
from enum import Enum
from typing import Optional, Any

from pydantic import BaseModel, field_validator, model_validator, Field
from pydantic_core.core_schema import FieldValidationInfo


class _Patterns:
    E59 = re.compile(r'7777|(19|20)[0-9]{2}')
    E60 = re.compile(r'7777|9999|(19|20)[0-9]{2}')
    E66 = re.compile(
        r'66666666|(19|20)[0-9]{2}(((01|03|05|07|08|10|12])(0[1-9]|[12][0-9]|30|31))|(02(0[1-9]|[12][0-9]))|((04|06|09|11)(0[1-9]|[12][0-9]|30)))')


class ReportType(Enum):
    OOH = 'Out of Home'
    A = 'Adoption/Guardianship Subsidy'


class FileType(Enum):
    PRODUCTION = 0
    TEST = 1


ReportingPeriod = str


class ReportingPeriodFileType:
    def __init__(self, reporting_period: ReportingPeriod, file_type: FileType):
        self.reporting_period: ReportingPeriod = reporting_period
        self.file_type: FileType = file_type

    def __str__(self) -> str:
        return str(self.reporting_period) + str(self.file_type.value)

    def __repr__(self) -> str:
        return str(self)


def is_valid_date(d: int) -> bool:
    try:
        s = str(d)
        year = int(s[0:4])
        month = int(s[4:6])
        day = int(s[6:8])
        date(year=year, month=month, day=day)
        return True
    except ValueError:
        return False


class MyBaseModel(BaseModel):
    def scatter(self, obj, ignore: Optional[list[str]] = None):
        """Copy model fields into another object"""
        for fld in self.model_fields_set:
            if not ignore or fld not in ignore:
                setattr(obj, fld, getattr(self, fld))

    def gather(self, obj, ignore: Optional[list[str]] = None):
        """Copy model fields from another object"""
        for fld in self.model_fields:
            if not ignore or fld not in ignore:
                setattr(self, fld, getattr(obj, fld))

    @classmethod
    def crib(cls, obj):
        """Create a new model based on values found in another object"""
        d = {}
        for fld in cls.model_fields:
            try:
                if hasattr(obj, fld) and isinstance(getattr(obj, fld), list) or isinstance(getattr(obj, fld), cls.model_fields[fld].annotation):
                    d[fld] = getattr(obj, fld)
            except TypeError as te:
                print(f"crib error: {te}, {te.args}, {fld}, {cls.model_fields[fld].annotation}")
                # pass
        # print(f"cribbing {cls.__name__} with {d}")
        return cls(**d)

    def kwds(self) -> dict:
        """Represent the model's fields as a set unpackable keyword/value pairs"""
        d = {}
        for fld in self.model_fields:
            d[fld] = getattr(self, fld)
        # print(f"{self.__class__.__name__} kwds={d}")
        return d


class Tribe(MyBaseModel):
    id: int = Field(default=None)
    tribe: str
    epa_code: str
    states: list[str] = Field(default_factory=list)

    def __str__(self):
        states = ", ".join([state for state in self.states])
        return f"{self.tribe} ({states})"


class State(MyBaseModel):
    id: int = Field(default=None)
    state: str
    name: str
    fips_code: int
    tribes: list[str] = Field(default_factory=list)


class Removal1993(MyBaseModel):
    # id: int | None = Field(default=None)
    # ooh_id: int | None
    e69: int | None = Field(default=None)
    e153: int | None = Field(default=None)
    e155: int | None = Field(default=None)

    # @field_validator('e69', 'e153')
    # @classmethod
    # def check_date(cls, v: int, info: FieldValidationInfo) -> int:
    #     s = str(v)
    #     y = s[0:4]
    #     m = s[4:6]
    #     d = s[6:]
    #     err_msg = f"{d} is not a valid date in YYYYMMDD format for {info.field_name}"
    #     if len(s) != 8 or \
    #             int(y) <= 1980 or \
    #             int(y) > datetime.today().year or \
    #             not ("01" <= m <= "12") or \
    #             not ("01" <= d <=
    #                  {"01": "31", "02": "29", "03": "31", "04": "30", "05": "31", "06": "30", "07": "31", "08": "31",
    #                   "09": "30", "10": "31", "11": "30", "12": "31"}[m]):
    #         raise ValueError(err_msg)
    #     return v
    #
    # @field_validator('e155')
    # @classmethod
    # def e155_valid(cls, v: int, info: FieldValidationInfo) -> int:
    #     if v not in (1, 2, 3, 4, 5, 6, 8):
    #         raise ValueError(f"Invalid selection for {info.field_name.upper()}")
    #     return v
    #
    # @model_validator(mode='after')
    # def e69_e153(self):
    #     if self.e69 >= self.e153:
    #         raise ValueError(f"Date of Removal (E69) must be prior to the Date of Exit (E153) for the same removal")
    #     return self


class PermanencyPlan(MyBaseModel):
    # id: int | None = Field(default=None)
    # removal_id: int | None
    e147: int | None = Field(default=None)
    e148: int | None = Field(default=None)


class PermanencyHearing(MyBaseModel):
    # id: int | None = Field(default=None)
    # removal_id: int | None
    e150: int | None = Field(default=None)


class PeriodicReview(MyBaseModel):
    # id: int | None = Field(default=None)
    # removal_id: int | None
    e149: int | None = Field(default=None)


class CaseVisit(MyBaseModel):
    # id: int | None
    # removal_id: int | None
    e151: int | None = Field(default=None)
    e152: int | None = Field(default=None)


class LivingArrangement(MyBaseModel):
    # id: int | None = Field(default=None)
    # removal_id: int | None
    last_updated: datetime | None = Field(default=None)
    e40: int | None = Field(default=None)
    e58: int | None = Field(default=None)
    e112: int | None = Field(default=None)
    e113: int | None = Field(default=None)
    e114: int | None = Field(default=None)
    e115: int | None = Field(default=None)
    e116: int | None = Field(default=None)
    e117: int | None = Field(default=None)
    e118: int | None = Field(default=None)
    e119: int | None = Field(default=None)
    e120: int | None = Field(default=None)
    e121: int | None = Field(default=None)
    e122: str | None = Field(default=None)
    e123: int | None = Field(default=None)
    e124: int | None = Field(default=None)
    e125: int | None = Field(default=None)
    e126: int | None = Field(default=None)
    e127: int | None = Field(default=None)
    e128: int | None = Field(default=None)
    e129: int | None = Field(default=None)
    e130: int | None = Field(default=None)
    e131: int | None = Field(default=None)
    e132: int | None = Field(default=None)
    e133: int | None = Field(default=None)
    e134: int | None = Field(default=None)
    e135: int | None = Field(default=None)
    e136: int | None = Field(default=None)
    e137: int | None = Field(default=None)
    e138: int | None = Field(default=None)
    e139: int | None = Field(default=None)
    e140: int | None = Field(default=None)
    e141: int | None = Field(default=None)
    e142: int | None = Field(default=None)
    e143: int | None = Field(default=None)
    e144: int | None = Field(default=None)
    e145: int | None = Field(default=None)
    e146: int | None = Field(default=None)


class Removal2020(MyBaseModel):
    # id: int | None = Field(default=None)
    # ooh_id: int | None
    e3: str | None = Field(default=None)
    e69: int | None = Field(default=None)
    e70: int | None = Field(default=None)
    e71: int | None = Field(default=None)
    e72: int | None = Field(default=None)
    e73: int | None = Field(default=None)
    e74: int | None = Field(default=None)
    e75: int | None = Field(default=None)
    e76: int | None = Field(default=None)
    e77: int | None = Field(default=None)
    e78: int | None = Field(default=None)
    e79: int | None = Field(default=None)
    e80: int | None = Field(default=None)
    e81: int | None = Field(default=None)
    e82: int | None = Field(default=None)
    e83: int | None = Field(default=None)
    e84: int | None = Field(default=None)
    e85: int | None = Field(default=None)
    e86: int | None = Field(default=None)
    e87: int | None = Field(default=None)
    e88: int | None = Field(default=None)
    e89: int | None = Field(default=None)
    e90: int | None = Field(default=None)
    e91: int | None = Field(default=None)
    e92: int | None = Field(default=None)
    e93: int | None = Field(default=None)
    e94: int | None = Field(default=None)
    e95: int | None = Field(default=None)
    e96: int | None = Field(default=None)
    e97: int | None = Field(default=None)
    e98: int | None = Field(default=None)
    e99: int | None = Field(default=None)
    e100: int | None = Field(default=None)
    e101: int | None = Field(default=None)
    e102: int | None = Field(default=None)
    e103: int | None = Field(default=None)
    e104: int | None = Field(default=None)
    e105: int | None = Field(default=None)
    living_arrangements: list[LivingArrangement] = Field(default_factory=list)
    permanency_plans: list[PermanencyPlan] = Field(default_factory=list)
    periodic_reviews: list[PeriodicReview] = Field(default_factory=list)
    permanency_hearings: list[PermanencyHearing] = Field(default_factory=list)
    case_worker_visits: list[CaseVisit] = Field(default_factory=list)
    e153: int | None = Field(default=None)
    e154: int | None = Field(default=None)
    e155: int | None = Field(default=None)
    e156: int | None = Field(default=None)
    e157: int | None = Field(default=None)
    e158: int | None = Field(default=None)
    e159: int | None = Field(default=None)
    e160: int | None = Field(default=None)
    e161: int | None = Field(default=None)
    e162: int | None = Field(default=None)
    e163: int | None = Field(default=None)
    e164: int | None = Field(default=None)
    e165: int | None = Field(default=None)
    e166: int | None = Field(default=None)
    e167: int | None = Field(default=None)
    e168: int | None = Field(default=None)
    e169: int | None = Field(default=None)
    e170: int | None = Field(default=None)
    e171: int | None = Field(default=None)
    e172: int | None = Field(default=None)
    e173: int | None = Field(default=None)
    e174: int | None = Field(default=None)
    e175: int | None = Field(default=None)
    e176: int | None = Field(default=None)
    e177: int | None = Field(default=None)
    e178: int | None = Field(default=None)
    e179: int | None = Field(default=None)
    e180: int | None = Field(default=None)
    e181: int | None = Field(default=None)
    e182: int | None = Field(default=None)
    e183: int | None = Field(default=None)
    e184: int | None = Field(default=None)
    e185: int | None = Field(default=None)
    e186: int | None = Field(default=None)


class SecondParent(MyBaseModel):
    # id: int | None = Field(default=None)
    # ooh_id: int | None
    number: int = Field(default=0)
    e64: int | None = Field(default=None)
    e66: int | None = Field(default=None)
    e68: int | None = Field(default=None)

    def __init__(self, **data: Any):
        super().__init__(**data)

    def e64_as_str(self) -> str:
        return {0: 'Not Applicable', 1: 'Voluntary', 2: 'Involuntary'}[self.e64]


class RecognizedTribe(MyBaseModel):
    # id: int | None = Field(default=None)
    # ooh_id: int | None
    e9: int | None = Field(default=None)


class OOHRecord(MyBaseModel):
    # ooh_id: int | None = Field(default=None)
    # context_id: int  # = Field(default=None)
    funding: int | None = Field(default=None)
    e7: int | None = Field(default=None)
    e8: int | None = Field(default=None)
    e10: int | None = Field(default=None)
    e11: int | None = Field(default=None)
    e12: int | None = Field(default=None)
    e22: int | None = Field(default=None)
    e23: int | None = Field(default=None)
    e24: int | None = Field(default=None)
    e25: int | None = Field(default=None)
    e26: int | None = Field(default=None)
    e27: int | None = Field(default=None)
    e28: int | None = Field(default=None)
    e29: int | None = Field(default=None)
    e30: int | None = Field(default=None)
    e31: int | None = Field(default=None)
    e32: int | None = Field(default=None)
    e33: int | None = Field(default=None)
    e34: int | None = Field(default=None)
    e35: int | None = Field(default=None)
    e36: int | None = Field(default=None)
    e37: int | None = Field(default=None)
    e38: int | None = Field(default=None)
    e39: int | None = Field(default=None)
    # e40: int | None
    e41: int | None = Field(default=None)
    e42: int | None = Field(default=None)
    e43: int | None = Field(default=None)
    e44: int | None = Field(default=None)
    e45: int | None = Field(default=None)
    e46: int | None = Field(default=None)
    e47: int | None = Field(default=None)
    e48: int | None = Field(default=None)
    e49: int | None = Field(default=None)
    e50: int | None = Field(default=None)
    e51: int | None = Field(default=None)
    e52: int | None = Field(default=None)
    e53: int | None = Field(default=None)
    e54: int | None = Field(default=None)
    e55: int | None = Field(default=None)
    e56: int | None = Field(default=None)
    e57: int | None = Field(default=None)
    # e58: int | None
    e59: int | None = Field(default=None)
    e60: int | None = Field(default=None)
    e61: int | None = Field(default=None)
    e62: int | None = Field(default=None)
    e63: int | None = Field(default=None)
    e65: int | None = Field(default=None)
    e67: int | None = Field(default=None)
    e106: int | None = Field(default=None)
    e107: int | None = Field(default=None)
    e108: int | None = Field(default=None)
    e109: int | None = Field(default=None)
    e110: int | None = Field(default=None)
    e111: int | None = Field(default=None)
    tribes: list[RecognizedTribe] = Field(default_factory=list)
    second_parents: list[SecondParent] = Field(default_factory=list)
    removals1993: list[Removal1993] = Field(default_factory=list)
    removals2020: list[Removal2020] = Field(default_factory=list)


class ARecord(MyBaseModel):
    # a_id: int | None = Field(default=None)
    # context_id: int  # = Field(default=None)
    a15: int | None = Field(default=None)
    a16: int | None = Field(default=None)
    a17: int | None = Field(default=None)
    a18: int | None = Field(default=None)
    a19: int | None = Field(default=None)


class Child(MyBaseModel):
    e5: int | None = Field(default=None)
    e6: int | None = Field(default=None)
    e13: int | None = Field(default=None)
    e14: int | None = Field(default=None)
    e15: int | None = Field(default=None)
    e16: int | None = Field(default=None)
    e17: int | None = Field(default=None)
    e18: int | None = Field(default=None)
    e19: int | None = Field(default=None)
    e20: int | None = Field(default=None)
    e21: int | None = Field(default=None)
    ooh: OOHRecord | None = Field(default=None)
    a: ARecord | None = Field(default=None)


class Context(MyBaseModel):
    # context_id: int | None
    # first_name: str | None = Field(default="")
    # last_name: str | None = Field(default="")
    id: int | None = Field(default=None)
    e2: str | None = Field(default=None)
    file_type: FileType
    data: Child = Field(default_factory=Child)


class BaseChild(MyBaseModel):
    id: int | None = Field(default=None)
    first_name: str | None = Field(default="")
    last_name: str | None = Field(default="")
    date_created: date = Field(default=date.today())
    last_removal: date | None = Field(default=None)
    last_adoption: date | None = Field(default=None)
    last_exit: date | None = Field(default=None)
    last_termination: date | None = Field(default=None)
    e1: str | None = Field(default=None)
    e4: str | None = Field(default=None)
    e5: date | None = Field(default=None)


class Agency(MyBaseModel):
    fips_code: str | None
    epa_code: str | None

    @property
    def e1(self) -> str | None:
        return self.fips_code if self.fips_code else self.epa_code if self.epa_code else None

    @model_validator(mode='after')
    def fips_code_epa_code(self):
        if self.fips_code is None and self.epa_code is None:
            raise ValueError("Select either a FIPS code or an EPA Tribal code.")
        if self.fips_code and self.epa_code:
            raise ValueError("Select either a FIPS code or an EPA Tribal code, but not both.")
        return self


class Export(MyBaseModel):
    e2: int | None
    file_name: str | None
