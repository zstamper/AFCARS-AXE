import xml.etree.ElementTree as ET
from typing import Any, Optional
from xml.etree.ElementTree import Element

from model import ContextTable, BaseChildTable
from model.models import FileType, Child, ARecord, SecondParent, Removal2020, \
    Removal1993, LivingArrangement, PermanencyPlan, PeriodicReview, PermanencyHearing, CaseVisit, OOHRecord, ReportType, \
    RecognizedTribe
from utils import refresh_dates
from utils.e1 import is_valid_date


def _text_from(element: Element, path: str) -> str | None:
    try:
        value = element.find(path).text
        if value == "":
            value = None
        return value
    except AttributeError:
        return None


def _int_from(element: Element, path: str) -> int | None:
    try:
        value = element.find(path).text
        if value == "":
            value = None
        return int(value)
    except (AttributeError, ValueError, TypeError):
        return None


def _date_from(element: Element, path: str) -> int | None:
    try:
        value = element.find(path).text
        if value == "":
            value = None
        if is_valid_date(int(value)):
            return int(value)
        return None
    except (AttributeError, ValueError, TypeError):
        return None


def parse_file(xml_file: Any) -> Element:
    """Open and convert the designated file as an element tree.

    :param xml_file str | Path | file-like. The file or data to be parsed.
    """
    if isinstance(xml_file, str) and xml_file.startswith('<'):
        tree = ET.fromstring(xml_file)
        return tree
    tree = ET.parse(xml_file)
    return tree.getroot()


def import_a_tree(tree: Element, file_type: FileType) -> tuple[list, list]:
    a1 = _text_from(tree, 'A1_title_iv_agency')
    if a1 is None:
        raise ET.ParseError()
    a2 = _int_from(tree, 'A2_report_date')
    records = tree.find('records')
    imported_ids = []
    skipped_ids = []
    for record in records.findall('record'):
        a3 = _text_from(record, 'A3_child_record_number')
        a4 = _date_from(record, 'A4_child_date_of_birth')
        a5 = _int_from(record, 'A5_child_sex')
        a6 = _int_from(record, 'A6_child_race_american_indian_alaska_native')
        a7 = _int_from(record, 'A7_child_race_asian')
        a8 = _int_from(record, 'A8_child_race_black_african_american')
        a9 = _int_from(record, 'A9_child_race_hawaiian_pacific_islander')
        a10 = _int_from(record, 'A10_child_race_white')
        a11 = _int_from(record, 'A11_child_race_unknown')
        a12 = _int_from(record, 'A12_child_race_abandoned')
        a13 = _int_from(record, 'A13_child_race_declined')
        a14 = _int_from(record, 'A14_child_hispanic_latino')
        a15 = _int_from(record, 'A15_assistance_agreement_type')
        a16 = _int_from(record, 'A16_adoption_subsidy_amount')
        a17 = _date_from(record, 'A17_adoption_finalization_date')
        a18 = _date_from(record, 'A18_agreement_termination_date')
        a19 = _int_from(record, 'A19_adoption_placing_agency')
        base_child, _ = BaseChildTable.get_or_create(e1=a1, e4=a3)
        context, is_new = ContextTable.get_or_create(base_child=base_child, e2=a2, file_type=file_type)
        a = ARecord(a15=a15, a16=a16, a17=a17, a18=a18, a19=a19)

        # When importing data, if the child already exists and already has an A record, skip the child.
        # If the child exists but has no A record, just update the A record.
        # Otherwise, add a new child entirely.
        if not is_new and context.data and context.data.a:
            skipped_ids.append(a3)
        else:
            imported_ids.append(a3)
            if is_new:
                child = Child(e5=a4, e6=a5, e13=a6, e14=a7, e15=a8, e16=a9, e17=a10, e18=a11, e19=a12, e20=a13, e21=a14,
                              a=a)
                context.data = child
            else:
                context.data.a = a
            context.save()
            refresh_dates(base_child=base_child, child=context.data, report_type=ReportType.A)
            base_child.save()
    return imported_ids, skipped_ids


def import_ooh_tree(tree: Element, file_type: FileType) -> tuple[list, list]:
    e1 = _text_from(tree, 'E1_title_iv_agency')
    if e1 is None:
        raise ET.ParseError()
    e2 = _text_from(tree, 'E2_report_date')
    records = tree.find('records')
    imported_ids = []
    skipped_ids = []
    for record in records.findall('record'):
        e4 = _text_from(record, 'E4_child_record_number')
        e5 = _date_from(record, 'E5_date_of_birth')
        e6 = _int_from(record, 'E6_sex')

        e7_e12 = record.find('E7_E12_tribal_information')
        e7 = _int_from(e7_e12, 'E7_agency_made_inquiries')
        e8 = _int_from(e7_e12, 'E8_tribal_membership')
        tribes = []
        e9_recognized_tribes = e7_e12.find('E9_recognized_tribes')
        for tribe in e9_recognized_tribes.findall('E9_recognized_tribe'):
            try:
                tribes.append(RecognizedTribe(e9=int(tribe.text)))
            except ValueError:
                pass
        e10 = _int_from(e7_e12, 'E10_icwa')
        e11 = _date_from(e7_e12, 'E11_icwa_date')
        e12 = _int_from(e7_e12, 'E12_icwa_notification')

        e13 = _int_from(record, 'E13_child_race_american_indian_alaska_native')
        e14 = _int_from(record, 'E14_child_race_asian')
        e15 = _int_from(record, 'E15_child_race_black')
        e16 = _int_from(record, 'E16_child_race_native_hawaiian_pacific_islander')
        e17 = _int_from(record, 'E17_child_race_white')
        e18 = _int_from(record, 'E18_child_race_unknown')
        e19 = _int_from(record, 'E19_child_race_abandoned')
        e20 = _int_from(record, 'E20_child_race_declined')
        e21 = _int_from(record, 'E21_child_hispanic_latino')
        e22 = _int_from(record, 'E22_health_assessment')
        e23 = _int_from(record, 'E23_health_conditions')

        e24_e34 = record.find('E24_34_specific_health_conditions')
        e24 = _int_from(e24_e34, 'E24_health_intellectual_disability')
        e25 = _int_from(e24_e34, 'E25_health_autism_spectrum_disorder')
        e26 = _int_from(e24_e34, 'E26_health_visual_impairment')
        e27 = _int_from(e24_e34, 'E27_health_hearing_impairment')
        e28 = _int_from(e24_e34, 'E28_health_orthopedic_impairment')
        e29 = _int_from(e24_e34, 'E29_health_mental_disorder')
        e30 = _int_from(e24_e34, 'E30_health_adhd_add')
        e31 = _int_from(e24_e34, 'E31_health_serious_mental_disorder')
        e32 = _int_from(e24_e34, 'E32_health_developmental_delay')
        e33 = _int_from(e24_e34, 'E33_health_developmental_disability')
        e34 = _int_from(e24_e34, 'E34_health_other_condition')

        e35 = _int_from(record, 'E35_school_enrollment')
        e36 = _int_from(record, 'E36_school_highest_completed')
        e37 = _int_from(record, 'E37_school_special_education')
        # if all three are null, leave it as null, else it's probably 'Not attended not based on age'
        e36 = 17 if e36 is None and e35 is not None and e37 is not None else e36
        e38 = _int_from(record, 'E38_pregnant')
        e39 = _int_from(record, 'E39_fathered_or_bore_child')
        e40 = _int_from(record, 'E40_child_and_children_together')
        e41 = _int_from(record, 'E41_prior_adoption')

        e42_e43 = record.find('E42_E43_prior_adoption_information')
        e42 = _date_from(e42_e43, 'E42_prior_adoption_date')
        e43 = _int_from(e42_e43, 'E43_prior_adoption_intercountry')

        e44 = _int_from(record, 'E44_prior_guardianship')
        e45 = _date_from(record, 'E45_prior_guardianship_date')
        e46 = _int_from(record, 'E46_support_assistance')

        e47_e54 = record.find('E47_E54_type_financial_assistance')
        e47 = _int_from(e47_e54, 'E47_state_tribal_adoption_assistance')
        e48 = _int_from(e47_e54, 'E48_state_tribal_foster_care')
        e49 = _int_from(e47_e54, 'E49_adoption_subsidy')
        e50 = _int_from(e47_e54, 'E50_guardianship_assistance')
        e51 = _int_from(e47_e54, 'E51_tanf_assistance')
        e52 = _int_from(e47_e54, 'E52_title_iv_b')
        e53 = _int_from(e47_e54, 'E53_chafee_foster_program')
        e54 = _int_from(e47_e54, 'E54_other_financial_support')

        e55 = _int_from(record, 'E55_foster_care_payment')
        e56 = _int_from(record, 'E56_total_siblings')

        e57_e58 = record.find('E57_E58_siblings_in_foster_care')
        e57 = _int_from(e57_e58, 'E57_siblings_in_foster_care')
        e58 = _int_from(e57_e58, 'E58_siblings_in_living_arrangement')

        e59 = _int_from(record, 'E59_first_parent_birth_year')
        e60 = _int_from(record, 'E60_second_parent_birth_year')
        e61 = _int_from(record, 'E61_tribal_membership_mother')
        e62 = _int_from(record, 'E62_tribal_membership_father')

        e63_e68 = record.find('E63_E68_termination_of_parental_rights')
        tpr_first_parent = e63_e68.find('tpr_first_parent')
        e63 = _int_from(tpr_first_parent, 'E63_tpr_parent1')
        e65 = _date_from(tpr_first_parent, 'E65_tpr_petition_date_parent1')
        e67 = _date_from(tpr_first_parent, 'E67_tpr_date_parent1')

        second_parents = []
        parent_num = 2
        for parent in record.find('E63_E68_termination_of_parental_rights').findall('tpr_second_parent'):
            second_parents.append(parse_second_parent(parent, parent_num))
            parent_num += 1

        # # if second parent exists, there has to be a tpr, but we'll mark it as N/A
        # checking with program team as to whether this should be enabled or not.
        # if e60 not in [None, 7777, 9999] and len(second_parents) == 0:
        #     second_parents.append(SecondParent(number=parent_num, e64=0))

        removals_1993 = []
        for removal in record.find('E69_E186_removals').findall('removal_1993'):
            removals_1993.append(parse_removal_1993(removal))

        removals_2020 = []
        for removal in record.find('E69_E186_removals').findall('removal_2020'):
            removals_2020.append(parse_removal_2020(removal, e40, e58))

        e106 = _int_from(record, 'E106_prior_victim_sex_trafficking')

        e107_e108 = record.find('E107_E108_prior_victim_sex_trafficking_reporting')
        e107 = _int_from(e107_e108, 'E107_prior_victim_sex_trafficking_reported')
        e108 = _date_from(e107_e108, 'E108_prior_victim_sex_trafficking_reported_date')
        e109 = _int_from(record, 'E109_victim_sex_trafficking')

        e110_e111 = record.find('E110_E111_victim_sex_trafficking_reporting')
        e110 = _int_from(e110_e111, 'E110_victim_sex_trafficking_reported')
        e111 = _date_from(e110_e111, 'E111_victim_sex_trafficking_reported_date')

        base_child, _ = BaseChildTable.get_or_create(e1=e1, e4=e4)
        context, is_new = ContextTable.get_or_create(base_child=base_child, e2=e2, file_type=file_type)

        # When importing data, if the child already exists and already has an OOH record, skip the child.
        # If the child exists but has no A record, just update the A record.
        # Otherwise, add a new child entirely.
        if not is_new and context.data and context.data.ooh:
            skipped_ids.append(e4)
        else:
            imported_ids.append(e4)
            e104 = 0
            if removals_2020 and removals_2020[-1].e104:
                e104 = 1
            ooh = OOHRecord(
                e7=e7, e8=e8, e10=e10, e11=e11, e12=e12, e22=e22, e23=e23, e24=e24, e25=e25, e26=e26, e27=e27, e28=e28,
                e29=e29, e30=e30, e31=e31, e32=e32, e33=e33, e34=e34, e35=e35, e36=e36, e37=e37, e38=e38, e39=e39,
                e41=e41, e42=e42, e43=e43, e44=e44, e45=e45, e46=e46, e47=e47, e48=e48, e49=e49, e50=e50, e51=e51,
                e52=e52, e53=e53, e54=e54, e55=e55, e56=e56, e57=e57, e59=e59, e60=e60, e61=e61, e62=e62, e63=e63,
                e65=e65, e67=e67, e106=e106, e107=e107, e108=e108, e109=e109, e110=e110, e111=e111, funding=e104,
                tribes=tribes, second_parents=second_parents, removals1993=removals_1993, removals2020=removals_2020
            )
            if is_new:
                child = Child(e5=e5, e6=e6, e13=e13, e14=e14, e15=e15, e16=e16, e17=e17, e18=e18, e19=e19, e20=e20,
                              e21=e21,
                              ooh=ooh)
                context.data = child
            else:
                context.data.ooh = ooh
            context.save()
            refresh_dates(base_child=base_child, child=context.data, report_type=ReportType.OOH)
            base_child.save()
    return imported_ids, skipped_ids


def parse_living_arrangement(living_arrangement: Element, e40: Optional[int],
                             e58: Optional[int]) -> LivingArrangement:
    e112 = _date_from(living_arrangement, 'E112_date_living_arrangement')
    e113 = _int_from(living_arrangement, 'E113_foster_family_home')

    e114_e146 = living_arrangement.find('E114_E146_foster_family_home_type')
    e114 = _int_from(e114_e146, 'E114_licensed_home')
    e115 = _int_from(e114_e146, 'E115_therapeutic_home')
    e116 = _int_from(e114_e146, 'E116_shelter_care_home')
    e117 = _int_from(e114_e146, 'E117_relative_foster_family')
    e118 = _int_from(e114_e146, 'E118_pre_adopt_home')
    e119 = _int_from(e114_e146, 'E119_kin_foster_family')

    e123_e146 = e114_e146.find('E123_E146_foster_parent_information')
    if not e123_e146:
        e123 = e124 = e125 = e126 = e127 = e128 = e129 = e130 = e131 = e132 = e133 = e134 = e135 = e136 = e137 = None
        e138 = e139 = e140 = e141 = e142 = e143 = e144 = e145 = e146 = None
    else:
        e123 = _int_from(e123_e146, 'E123_marital_status_of_foster_parents')
        e124 = _int_from(e123_e146, 'E124_relationship_to_foster_parents')

        e125_e135 = e123_e146.find('E125_E135_first_foster_parent_information')
        e125 = _int_from(e125_e135, 'E125_foster_parent1_birth_year')
        e126 = _int_from(e125_e135, 'E126_foster_parent1_tribal_membership')
        e127 = _int_from(e125_e135, 'E127_foster_parent1_race_american_indian_alaska_native')
        e128 = _int_from(e125_e135, 'E128_foster_parent1_race_asian')
        e129 = _int_from(e125_e135, 'E129_foster_parent1_race_black')
        e130 = _int_from(e125_e135, 'E130_foster_parent1_race_native_hawaiian_pacific_islander')
        e131 = _int_from(e125_e135, 'E131_foster_parent1_race_white')
        e132 = _int_from(e125_e135, 'E132_foster_parent1_race_unknown')
        e133 = _int_from(e125_e135, 'E133_foster_parent1_race_declined')
        e134 = _int_from(e125_e135, 'E134_foster_parent1_hispanic_latino')
        e135 = _int_from(e125_e135, 'E135_foster_parent1_sex')

        e136_e146 = e123_e146.find('E136_E146_second_foster_parent_information')
        e136 = _int_from(e136_e146, 'E136_foster_parent2_birth_year')
        e137 = _int_from(e136_e146, 'E137_foster_parent2_tribal_membership')
        e138 = _int_from(e136_e146, 'E138_foster_parent2_race_american_indian_alaska_native')
        e139 = _int_from(e136_e146, 'E139_foster_parent2_race_asian')
        e140 = _int_from(e136_e146, 'E140_foster_parent2_race_black')
        e141 = _int_from(e136_e146, 'E141_foster_parent2_race_native_hawaiian_pacific_islander')
        e142 = _int_from(e136_e146, 'E142_foster_parent2_race_white')
        e143 = _int_from(e136_e146, 'E143_foster_parent2_race_unknown')
        e144 = _int_from(e136_e146, 'E144_foster_parent2_race_declined')
        e145 = _int_from(e136_e146, 'E145_foster_parent2_hispanic_latino')
        e146 = _int_from(e136_e146, 'E146_foster_parent2_sex')

    e120 = _int_from(living_arrangement, 'E120_other_living_arrangement_type')
    e121 = _int_from(living_arrangement, 'E121_location_of_living_arrangement')
    e122 = _text_from(living_arrangement, 'E122_jurisdiction_or_country')

    return LivingArrangement(e40=e40, e58=e58, e112=e112, e113=e113, e114=e114, e115=e115, e116=e116, e117=e117,
                             e118=e118, e119=e119, e120=e120, e121=e121, e122=e122, e123=e123, e124=e124, e125=e125,
                             e126=e126, e127=e127, e128=e128, e129=e129, e130=e130, e131=e131, e132=e132, e133=e133,
                             e134=e134, e135=e135, e136=e136, e137=e137, e138=e138, e139=e139, e140=e140, e141=e141,
                             e142=e142, e143=e143, e144=e144, e145=e145, e146=e146)


def parse_second_parent(parent: Element, parent_num: int) -> SecondParent:
    e64 = _int_from(parent, 'E64_tpr_parent2')
    e66 = _date_from(parent, 'E66_tpr_petition_date_parent2')
    e68 = _date_from(parent, 'E68_tpr_date_parent2')
    return SecondParent(number=parent_num, e64=e64, e66=e66, e68=e68)


def parse_removal_1993(removal: Element) -> Removal1993:
    e69 = _date_from(removal, 'E69_removal_date')
    e153 = _date_from(removal, 'E153_exit_date')
    e155 = _int_from(removal, 'E155_exit_reason')
    return Removal1993(e69=e69, e153=e153, e155=e155)


def parse_removal_2020(removal: Element, e40: Optional[int], e58: Optional[int]) -> Removal2020:
    e69 = _date_from(removal, 'E69_removal_date')
    e70 = _date_from(removal, 'E70_removal_transaction_date')
    e71 = _int_from(removal, 'E71_removal_environment')
    e3 = _text_from(removal, 'E3_local_agency')
    e72 = _int_from(removal, 'E72_runaway')
    e73 = _int_from(removal, 'E73_whereabouts_unknown')
    e74 = _int_from(removal, 'E74_physical_abuse')
    e75 = _int_from(removal, 'E75_sexual_abuse')
    e76 = _int_from(removal, 'E76_psychological_abuse')
    e77 = _int_from(removal, 'E77_neglect')
    e78 = _int_from(removal, 'E78_medical_neglect')
    e79 = _int_from(removal, 'E79_domestic_violence')
    e80 = _int_from(removal, 'E80_abandonment')
    e81 = _int_from(removal, 'E81_failure_to_return')
    e82 = _int_from(removal, 'E82_caretaker_alcohol_use')
    e83 = _int_from(removal, 'E83_caretaker_drug_use')
    e84 = _int_from(removal, 'E84_child_alcohol_use')
    e85 = _int_from(removal, 'E85_child_drug_use')
    e86 = _int_from(removal, 'E86_prenatal_alcohol_exposure')
    e87 = _int_from(removal, 'E87_prenatal_drug_exposure')
    e88 = _int_from(removal, 'E88_diagnosed_condition')
    e89 = _int_from(removal, 'E89_inadequate_access_to_mental_health')
    e90 = _int_from(removal, 'E90_inadequate_access_to_medical_service')
    e91 = _int_from(removal, 'E91_child_behavior_problem')
    e92 = _int_from(removal, 'E92_death_of_caretaker')
    e93 = _int_from(removal, 'E93_incarceration_of_caretaker')
    e94 = _int_from(removal, 'E94_caretaker_impairment_physical_emotional')
    e95 = _int_from(removal, 'E95_caretaker_impairment_cognitive')
    e96 = _int_from(removal, 'E96_inadequate_housing')
    e97 = _int_from(removal, 'E97_voluntary_adoption')
    e98 = _int_from(removal, 'E98_child_requested_placement')
    e99 = _int_from(removal, 'E99_sex_trafficking')
    e100 = _int_from(removal, 'E100_parental_immigration_detainment_deportation')
    e101 = _int_from(removal, 'E101_family_conflict_gender_orientation')
    e102 = _int_from(removal, 'E102_educational_neglect')
    e103 = _int_from(removal, 'E103_public_agency_title_iv_agreement')
    e104 = _int_from(removal, 'E104_tribal_agreement')
    e105 = _int_from(removal, 'E105_homelessness')

    living_arrangements = []
    for living_arrangement in removal.find('E112_E146_living_arrangements').findall('living_arrangement'):
        living_arrangements.append(parse_living_arrangement(living_arrangement, e40, e58))

    permanency_plans = []
    for permanency_plan in removal.find('E147_E148_permanency_plans').findall('permanency_plan'):
        permanency_plans.append(parse_permanency_plan(permanency_plan))

    periodic_reviews = []
    for periodic_review in removal.find('E149_periodic_reviews').findall('E149_periodic_review_date'):
        periodic_reviews.append(parse_periodic_review(periodic_review))

    permanency_hearings = []
    for permanency_hearing in removal.find('E150_permanency_hearings').findall('E150_permanency_hearing_date'):
        permanency_hearings.append(parse_permanency_hearing(permanency_hearing))

    case_worker_visits = []
    for case_worker_visit in removal.find('E151_E152_case_worker_visits').findall('case_worker_visit'):
        case_worker_visits.append(parse_case_worker_visit(case_worker_visit))

    e153 = _date_from(removal, 'E153_exit_date')
    e154 = _date_from(removal, 'E154_exit_transaction_date')
    e155 = _int_from(removal, 'E155_exit_reason')
    e156 = _int_from(removal, 'E156_transfer_to_another_agency')

    e157_e186 = removal.find('E157_E186_adoptive_parents_information')
    e157 = _int_from(e157_e186, 'E157_marital_status_of_adoptive_parents')
    e158 = _int_from(e157_e186, 'E158_relationship_to_adoptive_parents_relative')
    e159 = _int_from(e157_e186, 'E159_relationship_to_adoptive_parents_kin')
    e160 = _int_from(e157_e186, 'E160_relationship_to_adoptive_parents_non_relative')
    e161 = _int_from(e157_e186, 'E161_relationship_to_adoptive_parents_foster_parent')

    e162_e172 = e157_e186.find('E162_E172_first_adoptive_parent_information')
    try:
        e162 = _date_from(e162_e172, 'E162_adoptive_parent1_birth_date')
        e163 = _int_from(e162_e172, 'E163_adoptive_parent1_tribal_membership')
        e164 = _int_from(e162_e172, 'E164_adoptive_parent1_race_american_indian_alaska_native')
        e165 = _int_from(e162_e172, 'E165_adoptive_parent1_race_asian')
        e166 = _int_from(e162_e172, 'E166_adoptive_parent1_race_black')
        e167 = _int_from(e162_e172, 'E167_adoptive_parent1_race_native_hawaiian_pacific_islander')
        e168 = _int_from(e162_e172, 'E168_adoptive_parent1_race_white')
        e169 = _int_from(e162_e172, 'E169_adoptive_parent1_race_unknown')
        e170 = _int_from(e162_e172, 'E170_adoptive_parent1_race_declined')
        e171 = _int_from(e162_e172, 'E171_adoptive_parent1_hispanic_latino')
        e172 = _int_from(e162_e172, 'E172_adoptive_parent1_sex')
    except AttributeError:
        e162 = e163 = e164 = e165 = e166 = e167 = e168 = e169 = e170 = e171 = e172 = None

    e173_e183 = e157_e186.find('E173_E183_second_adoptive_parent_information')
    try:
        e173 = _date_from(e173_e183, 'E173_adoptive_parent2_birth_date')
        e174 = _int_from(e173_e183, 'E174_adoptive_parent2_tribal_membership')
        e175 = _int_from(e173_e183, 'E175_adoptive_parent2_race_american_indian_alaska_native')
        e176 = _int_from(e173_e183, 'E176_adoptive_parent2_race_asian')
        e177 = _int_from(e173_e183, 'E177_adoptive_parent2_race_black')
        e178 = _int_from(e173_e183, 'E178_adoptive_parent2_race_native_hawaiian_pacific_islander')
        e179 = _int_from(e173_e183, 'E179_adoptive_parent2_race_white')
        e180 = _int_from(e173_e183, 'E180_adoptive_parent2_race_unknown')
        e181 = _int_from(e173_e183, 'E181_adoptive_parent2_race_declined')
        e182 = _int_from(e173_e183, 'E182_adoptive_parent2_hispanic_latino')
        e183 = _int_from(e173_e183, 'E183_adoptive_parent2_sex')
    except AttributeError:
        e173 = e174 = e175 = e176 = e177 = e178 = e179 = e180 = e181 = e182 = e183 = None

    e184 = _int_from(e157_e186, 'E184_inter_intrajurisdictional_adoption')
    e185 = _int_from(e157_e186, 'E185_assistance_agreement_type')
    e186 = _int_from(e157_e186, 'E186_siblings_in_adoptive_home')

    return Removal2020(
        e3=e3, e69=e69, e70=e70, e71=e71, e72=e72, e73=e73, e74=e74, e75=e75, e76=e76, e77=e77, e78=e78, e79=e79,
        e80=e80, e81=e81, e82=e82, e83=e83, e84=e84, e85=e85, e86=e86, e87=e87, e88=e88, e89=e89, e90=e90, e91=e91,
        e92=e92, e93=e93, e94=e94, e95=e95, e96=e96, e97=e97, e98=e98, e99=e99, e100=e100, e101=e101, e102=e102,
        e103=e103, e104=e104, e105=e105, living_arrangements=living_arrangements, permanency_plans=permanency_plans,
        periodic_reviews=periodic_reviews, permanency_hearings=permanency_hearings,
        case_worker_visits=case_worker_visits, e153=e153, e154=e154, e155=e155, e156=e156, e157=e157, e158=e158,
        e159=e159, e160=e160, e161=e161, e162=e162, e163=e163, e164=e164, e165=e165, e166=e166, e167=e167,
        e168=e168,
        e169=e169, e170=e170, e171=e171, e172=e172, e173=e173, e174=e174, e175=e175, e176=e176, e177=e177,
        e178=e178,
        e179=e179, e180=e180, e181=e181, e182=e182, e183=e183, e184=e184, e185=e185, e186=e186
    )


def parse_permanency_plan(permanency_plan: Element) -> PermanencyPlan:
    e147 = _date_from(permanency_plan, 'E147_permanency_plan_date')
    e148 = _int_from(permanency_plan, 'E148_permanency_plan_type')
    return PermanencyPlan(e147=e147, e148=e148)


def parse_periodic_review(periodic_review: Element) -> PeriodicReview:
    try:
        return PeriodicReview(e149=int(periodic_review.text))
    except ValueError:
        return PeriodicReview()


def parse_permanency_hearing(permanency_hearing: Element) -> PermanencyHearing:
    try:
        return PermanencyHearing(e150=permanency_hearing.text)
    except ValueError:
        return PermanencyHearing()


def parse_case_worker_visit(case_worker_visit: Element) -> CaseVisit:
    e151 = _date_from(case_worker_visit, 'E151_case_worker_visit_date')
    e152 = _int_from(case_worker_visit, 'E152_case_worker_visit_location')
    return CaseVisit(e151=e151, e152=e152)
