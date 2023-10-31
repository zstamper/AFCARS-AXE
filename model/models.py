from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator, Field
from pydantic_core.core_schema import FieldValidationInfo


class MyBaseModel(BaseModel):
    def scatter(self, obj, ignore: Optional[list[str]] = None):
        "Copy model fields into another object"
        for fld in self.model_fields_set:
            if not ignore or fld not in ignore:
                setattr(obj, fld, getattr(self, fld))

    def gather(self, obj, ignore: Optional[list[str]] = None):
        "Copy model fields from another object"
        for fld in self.model_fields_set:
            if not ignore or fld not in ignore:
                setattr(self, fld, getattr(obj, fld))

    @classmethod
    def crib(cls, obj):
        "Create a new model based on values found in another object"
        d = {}
        for fld in cls.model_fields:
            try:
                if hasattr(obj, fld) and isinstance(getattr(obj, fld), cls.model_fields[fld].annotation):
                    d[fld] = getattr(obj, fld)
            except TypeError:
                pass
        # print(f"cribbing {cls.__name__} with {d}")
        return cls(**d)

    def kwds(self) -> dict:
        "Represent the model's fields as a set unpackable keyword/value pairs"
        d = {}
        for fld in self.model_fields:
            d[fld] = getattr(self, fld)
        # print(f"{self.__class__.__name__} kwds={d}")
        return d


class Tribe(MyBaseModel):
    id: int = Field(default=None)
    tribe: str
    epa_code: int
    states: list[str] = Field(default_factory=list)


class State(MyBaseModel):
    id: int = Field(default=None)
    state: str
    name: str
    fips_code: int
    tribes: list[str] = Field(default_factory=list)


class Removal1993(MyBaseModel):
    id: int | None = Field(default=None)
    ooh_id: int | None
    e69: int | None
    e153: int | None
    e155: int | None

    @field_validator('e69', 'e153')
    @classmethod
    def check_date(cls, v: int, info: FieldValidationInfo) -> int:
        s = str(v)
        y = s[0:4]
        m = s[4:6]
        d = s[6:]
        err_msg = f"{d} is not a valid date in YYYYMMDD format for {info.field_name}"
        if len(s) != 8 or \
                int(y) <= 1980 or \
                int(y) > datetime.today().year or \
                not ("01" <= m <= "12") or \
                not ("01" <= m <=
                     {"01": "31", "02": "29", "03": "31", "04": "30", "05": "31", "06": "30", "07": "31", "08": "31",
                      "09": "30", "10": "31", "11": "30", "12": "31"}[m]):
            raise ValueError(err_msg)
        return v

    @field_validator('e155')
    @classmethod
    def e155_valid(cls, v: int, info: FieldValidationInfo) -> int:
        if v not in (1, 2, 3, 4, 5, 6, 8):
            raise ValueError(f"Invalid selection for {info.field_name}")
        return v

    @model_validator(mode='after')
    def e69_e153(self):
        if self.e69 >= self.e153:
            raise ValueError(f"Date of Removal (e69) must be prior to the Date of Exit (e153) for the same removal")
        return self


class PermanencyPlan(MyBaseModel):
    id: int | None = Field(default=None)
    removal_id: int | None
    e147: int | None
    e148: int | None


class PermanencyHearing(MyBaseModel):
    id: int | None = Field(default=None)
    removal_id: int | None
    e150: int | None


class PeriodicReview(MyBaseModel):
    id: int | None = Field(default=None)
    removal_id: int | None
    e149: int | None


class CaseVisit(MyBaseModel):
    id: int | None
    removal_id: int | None
    e151: int | None
    e152: int | None


class LivingArrangement(MyBaseModel):
    id: int | None = Field(default=None)
    removal_id: int | None
    e40: int | None
    e58: int | None
    e112: int | None
    e113: int | None
    e114: int | None
    e115: int | None
    e116: int | None
    e117: int | None
    e118: int | None
    e119: int | None
    e120: int | None
    e121: int | None
    e122: int | None
    e123: int | None
    e124: int | None
    e125: int | None
    e126: int | None
    e127: int | None
    e128: int | None
    e129: int | None
    e130: int | None
    e131: int | None
    e132: int | None
    e133: int | None
    e134: int | None
    e135: int | None
    e136: int | None
    e137: int | None
    e138: int | None
    e139: int | None
    e140: int | None
    e141: int | None
    e142: int | None
    e143: int | None
    e144: int | None
    e145: int | None
    e146: int | None


class Removal2020(MyBaseModel):
    id: int | None = Field(default=None)
    ooh_id: int | None
    e3: int | None
    e69: int | None
    e70: int | None
    e71: int | None
    e72: int | None
    e73: int | None
    e74: int | None
    e75: int | None
    e76: int | None
    e77: int | None
    e78: int | None
    e79: int | None
    e80: int | None
    e81: int | None
    e82: int | None
    e83: int | None
    e84: int | None
    e85: int | None
    e86: int | None
    e87: int | None
    e88: int | None
    e89: int | None
    e90: int | None
    e91: int | None
    e92: int | None
    e93: int | None
    e94: int | None
    e95: int | None
    e96: int | None
    e97: int | None
    e98: int | None
    e99: int | None
    e100: int | None
    e101: int | None
    e102: int | None
    e103: int | None
    e104: int | None
    e105: int | None
    living_arrangements: list[LivingArrangement] = Field(default_factory=list)
    permanency_plans: list[PermanencyPlan] = Field(default_factory=list)
    periodic_reviews: list[PeriodicReview] = Field(default_factory=list)
    permanency_hearings: list[PermanencyHearing] = Field(default_factory=list)
    case_worker_visits: list[CaseVisit] = Field(default_factory=list)
    e153: int | None
    e154: int | None
    e155: int | None
    e156: int | None
    e157: int | None
    e158: int | None
    e159: int | None
    e160: int | None
    e161: int | None
    e162: int | None
    e163: int | None
    e164: int | None
    e165: int | None
    e166: int | None
    e167: int | None
    e168: int | None
    e169: int | None
    e170: int | None
    e171: int | None
    e172: int | None
    e173: int | None
    e174: int | None
    e175: int | None
    e176: int | None
    e177: int | None
    e178: int | None
    e179: int | None
    e180: int | None
    e181: int | None
    e182: int | None
    e183: int | None
    e184: int | None
    e185: int | None
    e186: int | None

    @field_validator('e69', 'e153')
    @classmethod
    def check_date(cls, v: int | None, info: FieldValidationInfo) -> int | None:
        if v is not None:
            s = str(v)
            y = s[0:4]
            m = s[4:6]
            d = s[6:]
            err_msg = f"{d} is not a valid date in YYYYMMDD format for {info.field_name}"
            if len(s) != 8 or \
                    int(y) <= 1980 or \
                    int(y) > datetime.today().year or \
                    not ("01" <= m <= "12") or \
                    not ("01" <= m <=
                         {"01": "31", "02": "29", "03": "31", "04": "30", "05": "31", "06": "30", "07": "31",
                          "08": "31",
                          "09": "30", "10": "31", "11": "30", "12": "31"}[m]):
                raise ValueError(err_msg)
        return v

    @field_validator('e155')
    @classmethod
    def e155_valid(cls, v: int, info: FieldValidationInfo) -> int:
        if v not in (1, 2, 3, 4, 5, 6, 7, 8, 9):
            raise ValueError(f"Invalid selection for {info.field_name}")
        return v

    @model_validator(mode='after')
    def e69_e153(self):
        if self.e69 is not None and self.e153 is not None:
            if self.e69 >= self.e153:
                raise ValueError(f"Date of Removal (e69) must be prior to the Date of Exit (e153) for the same removal")
        return self


class SecondParent(MyBaseModel):
    id: int | None = Field(default=None)
    ooh_id: int | None
    e64: int | None
    e66: int | None
    e68: int | None


class RecognizedTribe(MyBaseModel):
    id: int | None = Field(default=None)
    ooh_id: int | None
    e9: int | None


class OOHRecord(MyBaseModel):
    ooh_id: int | None = Field(default=None)
    child_id: int | None
    funding: int | None
    e7: int | None
    e8: int | None
    e10: int | None
    e11: int | None
    e12: int | None
    e22: int | None
    e23: int | None
    e24: int | None
    e25: int | None
    e26: int | None
    e27: int | None
    e28: int | None
    e29: int | None
    e30: int | None
    e31: int | None
    e32: int | None
    e33: int | None
    e34: int | None
    e35: int | None
    e36: int | None
    e37: int | None
    e38: int | None
    e39: int | None
    # e40: int | None
    e41: int | None
    e42: int | None
    e43: int | None
    e44: int | None
    e45: int | None
    e46: int | None
    e47: int | None
    e48: int | None
    e49: int | None
    e50: int | None
    e51: int | None
    e52: int | None
    e53: int | None
    e54: int | None
    e55: int | None
    e56: int | None
    e57: int | None
    # e58: int | None
    e59: int | None
    e60: int | None
    e61: int | None
    e62: int | None
    e63: int | None
    e65: int | None
    e67: int | None
    e106: int | None
    e107: int | None
    e108: int | None
    e109: int | None
    e110: int | None
    e111: int | None
    tribes: list[RecognizedTribe] = Field(default_factory=list)
    second_parents: list[SecondParent] = Field(default_factory=list)
    removals1993: list[Removal1993] = Field(default_factory=list)
    removals2020: list[Removal2020] = Field(default_factory=list)


class ARecord(MyBaseModel):
    a_id: int | None = Field(default=None)
    child_id: int | None
    # a5: int | None
    # a6: int | None
    # a7: int | None
    # a8: int | None
    # a9: int | None
    # a10: int | None
    # a11: int | None
    # a12: int | None
    # a13: int | None
    # a14: int | None
    a15: int | None
    a16: int | None
    a17: int | None
    a18: int | None
    a19: int | None


class Context(MyBaseModel):
    id: int | None
    e1: int | None


class Child(MyBaseModel):
    child_id: int | None = Field(default=None)
    context_id: int  # = Field(default=None)
    first_name: str | None
    last_name: str | None
    e4: str | None
    e5: int | None
    e6: int | None
    e13: int | None
    e14: int | None
    e15: int | None
    e16: int | None
    e17: int | None
    e18: int | None
    e19: int | None
    e20: int | None
    e21: int | None
    ooh: OOHRecord | None = Field(default=None)
    a: ARecord | None = Field(default=None)


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
