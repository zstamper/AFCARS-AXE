from peewee import Model, SqliteDatabase, IntegerField, TextField, ForeignKeyField, DoesNotExist, AutoField

from .models import (OOHRecord, ARecord, Child, Context, RecognizedTribe, SecondParent, LivingArrangement,
                     PermanencyPlan, PeriodicReview, PermanencyHearing, CaseVisit,
                     Removal2020, Removal1993, Tribe, State)

database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class ConfigTable(BaseModel):
    # id = AutoField()
    agency = IntegerField()


class ContextTable(BaseModel):
    # id = AutoField()
    e1 = IntegerField(index=True)  # Title IV-E Agency ID (2-digit FIPS or 3-digit EPA tribal code)

    def to_model(self) -> Context:
        record = Context(id=self.id, e1=self.e1)
        return record

    @staticmethod
    def persist_model(model: Context):
        context = ContextTable(id=model.id, e1=model.e1)
        context.save()
        model.id = context.id


class ChildTable(BaseModel):
    id = AutoField()
    context = ForeignKeyField(ContextTable, backref='children')
    first_name = TextField()
    last_name = TextField()
    e4 = TextField(null=True)
    e5 = IntegerField(null=True)
    e6 = IntegerField(null=True)
    e13 = IntegerField(null=True)
    e14 = IntegerField(null=True)
    e15 = IntegerField(null=True)
    e16 = IntegerField(null=True)
    e17 = IntegerField(null=True)
    e18 = IntegerField(null=True)
    e19 = IntegerField(null=True)
    e20 = IntegerField(null=True)
    e21 = IntegerField(null=True)

    def to_model(self) -> Child:
        child_model = Child.crib(self)
        child_model.ooh = ooh.to_model() if (ooh := self.ooh.get_or_none()) is not None else None
        child_model.a = a.to_model() if (a := self.a.get_or_none()) is not None else None
        return child_model

    @staticmethod
    def persist_model(model: Child, context_id:int = None):
        # child = ChildTable(id=model.id, first_name=model.first_name,
        #                    last_name=model.last_name, e4=model.e4, e5=model.e5, e6=model.e6,
        #                    e13=model.e13, e14=model.e14, e15=model.e15, e16=model.e16, e17=model.e17, e18=model.e18,
        #                    e19=model.e19, e20=model.e20, e21=model.e21)
        child = ChildTable(**model.kwds())
        child.save()

        model.id = child.id
        if model.ooh:
            model.ooh.child_id = model.id
            OOHRecordTable.persist_model(model.ooh)
        if model.a:
            model.a.child_id = model.id
            ARecordTable.persist_model(model.a)


class ARecordTable(BaseModel):
    id = AutoField()
    child = ForeignKeyField(ChildTable, backref='a')
    # a1 == e1
    # a2 == e2
    # a3 == e4
    # a4 == e5
    # a5 == e6
    a5 = IntegerField(null=True)
    a6 = IntegerField(null=True)
    a7 = IntegerField(null=True)
    a8 = IntegerField(null=True)
    a9 = IntegerField(null=True)
    a10 = IntegerField(null=True)
    a11 = IntegerField(null=True)
    a12 = IntegerField(null=True)
    a13 = IntegerField(null=True)
    a14 = IntegerField(null=True)
    a15 = IntegerField(null=True)
    a16 = IntegerField(null=True)
    a17 = IntegerField(null=True)
    a18 = IntegerField(null=True)
    a19 = IntegerField(null=True)

    def to_model(self) -> ARecord:
        record = ARecord.crib(self)
        record.context = self.context.to_model()
        return record
        # record = ARecord(id=self.id, child=self.child, context=self.context.to_model(),
        #                  a6=self.a6, a7=self.a7, a8=self.a8, a9=self.a9,
        #                  a10=self.a10, a11=self.a11, a12=self.a12, a13=self.a13, a14=self.a14,
        #                  a15=self.a15, a16=self.a16, a17=self.a17, a18=self.a18, a19=self.a19)
        # return record

    @staticmethod
    def persist_model(model: ARecord, child: int = None):
        arecord = ARecordTable(id=model.id, child=child, context=model.context.id,
                               a5=model.a5, a6=model.a6, a7=model.a7, a8=model.a8, a9=model.a9,
                               a10=model.a10, a11=model.a11, a12=model.a12, a13=model.a13, a14=model.a14,
                               a15=model.a15, a16=model.a16, a17=model.a17, a18=model.a18, a19=model.a19)
        arecord.save()
        model.id = arecord.id


class OOHRecordTable(BaseModel):
    id = AutoField()
    funding = IntegerField(null=True)
    child = ForeignKeyField(ChildTable, backref="ooh")
    e7 = IntegerField(null=True)
    e8 = IntegerField(null=True)
    e9 = IntegerField(null=True)
    e10 = IntegerField(null=True)
    e11 = IntegerField(null=True)
    e12 = IntegerField(null=True)
    e13 = IntegerField(null=True)
    e14 = IntegerField(null=True)
    e15 = IntegerField(null=True)
    e16 = IntegerField(null=True)
    e17 = IntegerField(null=True)
    e18 = IntegerField(null=True)
    e19 = IntegerField(null=True)
    e20 = IntegerField(null=True)
    e21 = IntegerField(null=True)
    e22 = IntegerField(null=True)
    e23 = IntegerField(null=True)
    e24 = IntegerField(null=True)
    e25 = IntegerField(null=True)
    e26 = IntegerField(null=True)
    e27 = IntegerField(null=True)
    e28 = IntegerField(null=True)
    e29 = IntegerField(null=True)
    e30 = IntegerField(null=True)
    e31 = IntegerField(null=True)
    e32 = IntegerField(null=True)
    e33 = IntegerField(null=True)
    e34 = IntegerField(null=True)
    e35 = IntegerField(null=True)
    e36 = IntegerField(null=True)
    e37 = IntegerField(null=True)
    e38 = IntegerField(null=True)
    e39 = IntegerField(null=True)
    # e40 = IntegerField(null=True)
    e41 = IntegerField(null=True)
    e42 = IntegerField(null=True)
    e43 = IntegerField(null=True)
    e44 = IntegerField(null=True)
    e45 = IntegerField(null=True)
    e46 = IntegerField(null=True)
    e47 = IntegerField(null=True)
    e48 = IntegerField(null=True)
    e49 = IntegerField(null=True)
    e50 = IntegerField(null=True)
    e51 = IntegerField(null=True)
    e52 = IntegerField(null=True)
    e53 = IntegerField(null=True)
    e54 = IntegerField(null=True)
    e55 = IntegerField(null=True)
    e56 = IntegerField(null=True)
    e57 = IntegerField(null=True)
    e59 = IntegerField(null=True)
    e60 = IntegerField(null=True)
    e61 = IntegerField(null=True)
    e62 = IntegerField(null=True)
    e63 = IntegerField(null=True)
    # second_parents: e64, e66, e68
    e65 = IntegerField(null=True)
    e67 = IntegerField(null=True)
    e106 = IntegerField(null=True)
    e107 = IntegerField(null=True)
    e108 = IntegerField(null=True)
    e109 = IntegerField(null=True)
    e110 = IntegerField(null=True)
    e111 = IntegerField(null=True)

    def to_model(self) -> OOHRecord:
        ooh_model = OOHRecord.crib(self)
        ooh_model.tribes = [tribe.to_model() for tribe in self.tribes]
        ooh_model.second_parents = [second_parent.to_model() for second_parent in self.second_parents]
        ooh_model.removals1993 = [removal1993.to_model() for removal1993 in self.removals1993]
        ooh_model.removals2020 = [removal2020.to_model() for removal2020 in self.removals2020]
        return ooh_model

    @staticmethod
    def persist_model(model: OOHRecord):
        ChildTable.persist_model(model.child)
        ContextTable.persist_model(model.context)
        record = OOHRecordTable(**model.kwds())
        record.save()
        model.id = record.id
        for tribe in model.tribes:
            tribe.ooh_id = record.id
            TribeTable.persist_model(tribe)
        for second_parent in model.second_parents:
            second_parent.ooh_id = record.id
            SecondParentTable.persist_model(second_parent, ooh=int(model.id))
        for removal in model.removals1993:
            removal.ooh_id = record.id
            Removal1993Table.persist_model(removal, ooh=int(model.id))
        for removal in model.removals2020:
            removal.ooh_id = record.id
            Removal2020Table.persist_model(removal, ooh=int(model.id))


class RecognizedTribesTable(BaseModel):
    id = AutoField()
    ooh = ForeignKeyField(OOHRecordTable, backref='tribes')
    e9 = IntegerField(null=True)

    def to_model(self) -> RecognizedTribe:
        return RecognizedTribe.crib(self)

    @staticmethod
    def persist_model(model: RecognizedTribe):
        tribe = RecognizedTribesTable(**model.kwds())
        tribe.save()
        model.id = tribe.id


class SecondParentTable(BaseModel):
    id = AutoField()
    ooh = ForeignKeyField(OOHRecordTable, backref='second_parents')
    e64 = IntegerField(null=True)
    e66 = IntegerField(null=True)
    e68 = IntegerField(null=True)

    def to_model(self) -> SecondParent:
        return SecondParent.crib(self)

    @staticmethod
    def persist_model(model: SecondParent, ooh: int = None):
        parent = SecondParentTable(**model.kwds())
        parent.save()
        model.id = parent.id


class Removal1993Table(BaseModel):
    id = AutoField()
    ooh = ForeignKeyField(OOHRecordTable, backref='removals1993')
    e69 = IntegerField(null=True)
    e153 = IntegerField(null=True)
    e155 = IntegerField(null=True)

    def to_model(self) -> Removal1993:
        record = Removal1993.crib(self)
        return record

    @staticmethod
    def persist_model(model: Removal1993, ooh: int = None):
        removal = Removal1993Table(**model.kwds())
        removal.save()
        model.id = removal.id


class Removal2020Table(BaseModel):
    id = AutoField()
    ooh = ForeignKeyField(OOHRecordTable, backref='removals2020')
    e3 = IntegerField(null=True)
    e69 = IntegerField(null=True)
    e70 = IntegerField(null=True)
    e71 = IntegerField(null=True)
    e72 = IntegerField(null=True)
    e73 = IntegerField(null=True)
    e74 = IntegerField(null=True)
    e75 = IntegerField(null=True)
    e76 = IntegerField(null=True)
    e77 = IntegerField(null=True)
    e78 = IntegerField(null=True)
    e79 = IntegerField(null=True)
    e80 = IntegerField(null=True)
    e81 = IntegerField(null=True)
    e82 = IntegerField(null=True)
    e83 = IntegerField(null=True)
    e84 = IntegerField(null=True)
    e85 = IntegerField(null=True)
    e86 = IntegerField(null=True)
    e87 = IntegerField(null=True)
    e88 = IntegerField(null=True)
    e89 = IntegerField(null=True)
    e90 = IntegerField(null=True)
    e91 = IntegerField(null=True)
    e92 = IntegerField(null=True)
    e93 = IntegerField(null=True)
    e94 = IntegerField(null=True)
    e95 = IntegerField(null=True)
    e96 = IntegerField(null=True)
    e97 = IntegerField(null=True)
    e98 = IntegerField(null=True)
    e99 = IntegerField(null=True)
    e100 = IntegerField(null=True)
    e101 = IntegerField(null=True)
    e102 = IntegerField(null=True)
    e103 = IntegerField(null=True)
    e104 = IntegerField(null=True)
    e105 = IntegerField(null=True)
    # living_arrangements e112..e146
    # permanency_plans e147..e148
    # periodic_reviews e149
    # permanency_hearings e150
    # case_worker_visits e151..e152
    e153 = IntegerField(null=True)
    e154 = IntegerField(null=True)
    e155 = IntegerField(null=True)
    e156 = IntegerField(null=True)
    e157 = IntegerField(null=True)
    e158 = IntegerField(null=True)
    e159 = IntegerField(null=True)
    e160 = IntegerField(null=True)
    e161 = IntegerField(null=True)
    e162 = IntegerField(null=True)
    e163 = IntegerField(null=True)
    e164 = IntegerField(null=True)
    e165 = IntegerField(null=True)
    e166 = IntegerField(null=True)
    e167 = IntegerField(null=True)
    e168 = IntegerField(null=True)
    e169 = IntegerField(null=True)
    e170 = IntegerField(null=True)
    e171 = IntegerField(null=True)
    e172 = IntegerField(null=True)
    e173 = IntegerField(null=True)
    e174 = IntegerField(null=True)
    e175 = IntegerField(null=True)
    e176 = IntegerField(null=True)
    e177 = IntegerField(null=True)
    e178 = IntegerField(null=True)
    e179 = IntegerField(null=True)
    e180 = IntegerField(null=True)
    e181 = IntegerField(null=True)
    e182 = IntegerField(null=True)
    e183 = IntegerField(null=True)
    e184 = IntegerField(null=True)
    e185 = IntegerField(null=True)
    e186 = IntegerField(null=True)

    def to_model(self) -> Removal2020:
        record = Removal2020.crib(self)
        record.living_arrangements = [living_arrangement.to_model() for living_arrangement in self.living_arrangements]
        record.permanency_plans = [permanency_plan.to_model() for permanency_plan in self.permanency_plans]
        record.periodic_reviews = [periodic_review.to_model() for periodic_review in self.periodic_reviews]
        record.permanency_hearings = [permanency_hearing.to_model() for permanency_hearing in self.permanency_hearings]
        record.case_worker_visits = [case_worker_visit.to_model() for case_worker_visit in self.case_worker_visits]
        return record
        # record = Removal2020(id=self.id, ooh=self.ooh_id, e3=self.e3, e69=self.e69,
        #                      e70=self.e70, e71=self.e71, e72=self.e72, e73=self.e73, e74=self.e74,
        #                      e75=self.e75, e76=self.e76, e77=self.e77, e78=self.e78, e79=self.e79,
        #                      e80=self.e80, e81=self.e81, e82=self.e82, e83=self.e83, e84=self.e84,
        #                      e85=self.e85, e86=self.e86, e87=self.e87, e88=self.e88, e89=self.e89,
        #                      e90=self.e90, e91=self.e91, e92=self.e92, e93=self.e93, e94=self.e94,
        #                      e95=self.e95, e96=self.e96, e97=self.e97, e98=self.e98, e99=self.e99,
        #                      e100=self.e100, e101=self.e101, e102=self.e102, e103=self.e103, e104=self.e104,
        #                      e105=self.e105, e106=self.e106, e107=self.e107, e108=self.e108, e109=self.e109,
        #                      e110=self.e110, e111=self.e111,
        #                      living_arrangements=[living_arrangement for living_arrangement in
        #                                           self.living_arrangements],
        #                      permanency_plans=[permanency_plan for permanency_plan in self.permanency_plans],
        #                      periodic_reviews=[periodic_review for periodic_review in self.periodic_reviews],
        #                      permanency_hearings=[permanency_hearing for permanency_hearing in
        #                                           self.permanency_hearings],
        #                      case_worker_visits=[case_worker_visit for case_worker_visit in self.case_worker_visits],
        #                      e153=self.e153, e154=self.e154, e155=self.e155, e156=self.e156, e157=self.e157,
        #                      e158=self.e158, e159=self.e159, e160=self.e160, e161=self.e161, e162=self.e162,
        #                      e163=self.e163, e164=self.e164, e165=self.e165, e166=self.e166, e167=self.e167,
        #                      e168=self.e168, e169=self.e169, e170=self.e170, e171=self.e171, e172=self.e172,
        #                      e173=self.e173, e174=self.e174, e175=self.e175, e176=self.e176, e177=self.e177,
        #                      e178=self.e178, e179=self.e179, e180=self.e180, e181=self.e181, e182=self.e182,
        #                      e183=self.e183, e184=self.e184, e185=self.e185, e186=self.e186
        #                      )
        # return record

    @staticmethod
    def persist_model(model: Removal2020, ooh: int = None):
        record = Removal2020Table(**model.kwds())
        record.save()
        model.id = record.id
        for living_arrangement in model.living_arrangements:
            living_arrangement.removal = model.id
            LivingArrangementTable.persist_model(living_arrangement)
        for permanency_plan in model.permanency_plans:
            permanency_plan.removal_id = model.id
            PermanencyPlanTable.persist_model(permanency_plan)
        for periodic_review in model.periodic_reviews:
            periodic_review.removal_id = model.id
            PeriodicReviewTable.persist_model(periodic_review)
        for permanency_hearing in model.permanency_hearings:
            permanency_hearing.removal_id = model.id
            PermanencyHearingTable.persist_model(permanency_hearing)
        for case_worker_visit in model.case_worker_visits:
            case_worker_visit.removal_id = model.id
            CaseWorkerVisitTable.persist_model(case_worker_visit)


class LivingArrangementTable(BaseModel):
    id = AutoField()
    removal = ForeignKeyField(Removal2020Table, backref='living_arrangements')
    e40 = IntegerField(null=True)
    e58 = IntegerField(null=True)
    e112 = IntegerField(null=True)
    e113 = IntegerField(null=True)
    e114 = IntegerField(null=True)
    e115 = IntegerField(null=True)
    e116 = IntegerField(null=True)
    e117 = IntegerField(null=True)
    e118 = IntegerField(null=True)
    e119 = IntegerField(null=True)
    e120 = IntegerField(null=True)
    e121 = IntegerField(null=True)
    e122 = IntegerField(null=True)
    e123 = IntegerField(null=True)
    e124 = IntegerField(null=True)
    e125 = IntegerField(null=True)
    e126 = IntegerField(null=True)
    e127 = IntegerField(null=True)
    e128 = IntegerField(null=True)
    e129 = IntegerField(null=True)
    e130 = IntegerField(null=True)
    e131 = IntegerField(null=True)
    e132 = IntegerField(null=True)
    e133 = IntegerField(null=True)
    e134 = IntegerField(null=True)
    e135 = IntegerField(null=True)
    e136 = IntegerField(null=True)
    e137 = IntegerField(null=True)
    e138 = IntegerField(null=True)
    e139 = IntegerField(null=True)
    e140 = IntegerField(null=True)
    e141 = IntegerField(null=True)
    e142 = IntegerField(null=True)
    e143 = IntegerField(null=True)
    e144 = IntegerField(null=True)
    e145 = IntegerField(null=True)
    e146 = IntegerField(null=True)

    def to_model(self) -> LivingArrangement:
        return LivingArrangement.crib(self)
        # record = LivingArrangement(id=self.id, removal=self.removal_id, e112=self.e112, e113=self.e113, e114=self.e114,
        #                            e115=self.e115, e116=self.e116, e117=self.e117, e118=self.e118, e119=self.e119,
        #                            e120=self.e120, e121=self.e121, e122=self.e122, e123=self.e123, e124=self.e124,
        #                            e125=self.e125, e126=self.e126, e127=self.e127, e128=self.e128, e129=self.e129,
        #                            e130=self.e130, e131=self.e131, e132=self.e132, e133=self.e133, e134=self.e134,
        #                            e135=self.e135, e136=self.e136, e137=self.e137, e138=self.e138, e139=self.e139,
        #                            e140=self.e140, e141=self.e141, e142=self.e142, e143=self.e143, e144=self.e144,
        #                            e145=self.e145, e146=self.e146
        #                            )
        # return record

    @staticmethod
    def persist_model(model: LivingArrangement):
        living_arrangement = LivingArrangementTable(id=model.id, removal=model.removal,
                                                    e112=model.e112, e113=model.e113, e114=model.e114,
                                                    e115=model.e115, e116=model.e116, e117=model.e117, e118=model.e118,
                                                    e119=model.e119, e120=model.e120, e121=model.e121, e122=model.e122,
                                                    e123=model.e123, e124=model.e124, e125=model.e125, e126=model.e126,
                                                    e127=model.e127, e128=model.e128, e129=model.e129, e130=model.e130,
                                                    e131=model.e131, e132=model.e132, e133=model.e133, e134=model.e134,
                                                    e135=model.e135, e136=model.e136, e137=model.e137, e138=model.e138,
                                                    e139=model.e139, e140=model.e140, e141=model.e141, e142=model.e142,
                                                    e143=model.e143, e144=model.e144, e145=model.e145, e146=model.e146
                                                    )
        living_arrangement.save()
        model.id = living_arrangement.id


class PermanencyPlanTable(BaseModel):
    id = AutoField()
    removal = ForeignKeyField(Removal2020Table, backref='permanency_plans')
    e147 = IntegerField(null=True)
    e148 = IntegerField(null=True)

    def to_model(self) -> PermanencyPlan:
        return PermanencyPlan.crib(self)
        # record = PermanencyPlan(
        #     id=self.id,
        #     removal=self.removal_id,
        #     e147=self.e147,
        #     e148=self.e148
        # )
        # return record

    @staticmethod
    def persist_model(model: PermanencyPlan):
        permanency_plan = PermanencyPlanTable(id=model.id, e147=model.e147, e148=model.e148)
        permanency_plan.save()
        model.id = permanency_plan.id


class PeriodicReviewTable(BaseModel):
    id = AutoField()
    removal = ForeignKeyField(Removal2020Table, backref='periodic_reviews')
    e149 = IntegerField(null=True)

    def to_model(self) -> PeriodicReview:
        return PeriodicReview.crib(self)
        # record = PeriodicReview(id=self.id, removal=self.removal_id, e149=self.e149)
        # return record

    @staticmethod
    def persist_model(model: PeriodicReview):
        periodic_review = PeriodicReviewTable(id=model.id, e149=model.e149)
        periodic_review.save()
        model.id = periodic_review.id


class PermanencyHearingTable(BaseModel):
    id = AutoField()
    removal = ForeignKeyField(Removal2020Table, backref='permanency_hearings')
    e150 = IntegerField(null=True)

    def to_model(self) -> PermanencyHearing:
        return PermanencyHearing.crib(self)
        # record = PermanencyHearing(id=self.id, removal=self.removal_id, e150=self.e150)
        # return record

    @staticmethod
    def persist_model(model: PermanencyHearing):
        permanency_hearing = PermanencyHearingTable(**model.kwds())
        permanency_hearing.save()
        model.id = permanency_hearing.id


class CaseWorkerVisitTable(BaseModel):
    id = AutoField()
    removal = ForeignKeyField(Removal2020Table, backref='case_worker_visits')
    e151 = IntegerField(null=True)
    e152 = IntegerField(null=True)

    def to_model(self) -> CaseVisit:
        return CaseVisit.crib(self)
        # record = CaseVisit(id=self.id, removal=self.removal_id, e151=self.e151, e152=self.e152)
        # return record

    @staticmethod
    def persist_model(model: CaseVisit):
        case_worker_visit = CaseWorkerVisitTable(**model.kwds())
        case_worker_visit.save()
        model.id = case_worker_visit.id


# class AdoptiveParentsTable(BaseModel):
#     removal = ForeignKeyField(Removal2020Table, backref='adoptive_parents')
#     e157 = IntegerField(null=True)
#     e158 = IntegerField(null=True)
#     e159 = IntegerField(null=True)
#     e160 = IntegerField(null=True)
#     e161 = IntegerField(null=True)
#     e162 = IntegerField(null=True)
#     e163 = IntegerField(null=True)
#     e164 = IntegerField(null=True)
#     e165 = IntegerField(null=True)
#     e166 = IntegerField(null=True)
#     e167 = IntegerField(null=True)
#     e168 = IntegerField(null=True)
#     e169 = IntegerField(null=True)
#     e170 = IntegerField(null=True)
#     e171 = IntegerField(null=True)
#     e172 = IntegerField(null=True)
#     e173 = IntegerField(null=True)
#     e174 = IntegerField(null=True)
#     e175 = IntegerField(null=True)
#     e176 = IntegerField(null=True)
#     e177 = IntegerField(null=True)
#     e178 = IntegerField(null=True)
#     e179 = IntegerField(null=True)
#     e180 = IntegerField(null=True)
#     e181 = IntegerField(null=True)
#     e182 = IntegerField(null=True)
#     e183 = IntegerField(null=True)
#     e184 = IntegerField(null=True)
#     e185 = IntegerField(null=True)
#     e186 = IntegerField(null=True)
#
#     def to_model(self) -> AdoptiveParents:
#         record = AdoptiveParents(id=self.id, removal=self.removal_id, e157=self.e157, e158=self.e158, e159=self.e159,
#                                  e160=self.e160, e161=self.e161, e162=self.e162, e163=self.e163, e164=self.e164,
#                                  e165=self.e165, e166=self.e166, e167=self.e167, e168=self.e168, e169=self.e169,
#                                  e170=self.e170, e171=self.e171, e172=self.e172, e173=self.e173, e174=self.e174,
#                                  e175=self.e175, e176=self.e176, e177=self.e177, e178=self.e178, e179=self.e179,
#                                  e180=self.e180, e181=self.e181, e182=self.e182, e183=self.e183, e184=self.e184,
#                                  e185=self.e185, e186=self.e186
#                                  )
#         return record
#
#     @staticmethod
#     def persist_model(model: AdoptiveParents):
#         adoptive_parent = AdoptiveParentsTable(id=model.id, removal_id=model.removal, e157=model.e157, e158=model.e158,
#                                                e159=model.e159, e160=model.e160, e161=model.e161, e162=model.e162,
#                                                e163=model.e163, e164=model.e164, e165=model.e165, e166=model.e166,
#                                                e167=model.e167, e168=model.e168, e169=model.e169, e170=model.e170,
#                                                e171=model.e171, e172=model.e172, e173=model.e173, e174=model.e174,
#                                                e175=model.e175, e176=model.e176, e177=model.e177, e178=model.e178,
#                                                e179=model.e179, e180=model.e180, e181=model.e181, e182=model.e182,
#                                                e183=model.e183, e184=model.e184, e185=model.e185, e186=model.e186)
#         adoptive_parent.save()
#         model.id = adoptive_parent.id


# class FirstAdoptiveParentTable(BaseModel):
#     guardian = ForeignKeyField(AdoptiveParentsTable, backref='first_adoptive_parent')
#     e162 = IntegerField(null=True)
#     e163 = IntegerField(null=True)
#     e164 = IntegerField(null=True)
#     e165 = IntegerField(null=True)
#     e166 = IntegerField(null=True)
#     e167 = IntegerField(null=True)
#     e168 = IntegerField(null=True)
#     e169 = IntegerField(null=True)
#     e170 = IntegerField(null=True)
#     e171 = IntegerField(null=True)
#     e172 = IntegerField(null=True)


# class SecondAdoptiveParentTable(BaseModel):
#     parent = ForeignKeyField(AdoptiveParentsTable, backref='second_adoptive_parent')
#     e173 = IntegerField(null=True)
#     e174 = IntegerField(null=True)
#     e175 = IntegerField(null=True)
#     e176 = IntegerField(null=True)
#     e177 = IntegerField(null=True)
#     e178 = IntegerField(null=True)
#     e179 = IntegerField(null=True)
#     e180 = IntegerField(null=True)
#     e181 = IntegerField(null=True)
#     e182 = IntegerField(null=True)
#     e183 = IntegerField(null=True)
#
#     def to_model(self) -> SecondAdoptiveParent:
#         record = SecondAdoptiveParent(id=self.id, parent=self.parent_id, e173=self.e173, e174=self.e174,
#                                       e175=self.e175, e176=self.e176, e177=self.e177, e178=self.e178, e179=self.e179,
#                                       e180=self.e180, e181=self.e181, e182=self.e182, e183=self.e183)
#         return record
#


class StateTable(BaseModel):
    id = AutoField()
    code = TextField()
    name = TextField()
    fips_code = IntegerField(null=True)

    def to_model(self) -> State:
        record = State.crib(self)
        record.tribes = [tribe.tribe for tribe in TribeStateTable.select().where(TribeStateTable.state == self)]
        return record


class TribeTable(BaseModel):
    id = AutoField()
    tribe = TextField()
    epa_code = TextField()

    def to_model(self) -> Tribe:
        record = Tribe.crib(self)
        record.states = [state.code for state in TribeStateTable.select().where(TribeStateTable.tribe == self)]
        return record


class TribeStateTable(BaseModel):
    id = AutoField()
    tribe = ForeignKeyField(TribeTable, backref='states')
    state = ForeignKeyField(StateTable, backref='tribes')


class FIPSCodeTable(BaseModel):
    id = AutoField()
    state = TextField()
    fips_code = TextField()
