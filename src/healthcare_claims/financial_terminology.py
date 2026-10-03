CMS_ADJUDICATION = (
    "https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication"
)

HL7_ADJUDICATION = (
    "http://terminology.hl7.org/CodeSystem/adjudication"
)

CARIN_ADJUDICATION = (
    "http://hl7.org/fhir/us/carin-bb/CodeSystem/C4BBAdjudication"
)

CARIN_DISCRIMINATOR = (
    "http://hl7.org/fhir/us/carin-bb/CodeSystem/"
    "C4BBAdjudicationDiscriminator"
)


CMS_SOURCE = (
    "https://bluebutton.cms.gov/fhir/CodeSystem/Adjudication/"
)

HL7_SOURCE = (
    "https://terminology.hl7.org/7.4.0/"
    "CodeSystem-adjudication.html"
)

CARIN_SOURCE = (
    "https://hl7.org/fhir/us/carin-bb/STU2.1/"
    "CodeSystem-C4BBAdjudication.html"
)

CARIN_DISCRIMINATOR_SOURCE = (
    "https://hl7.org/fhir/us/carin-bb/STU2.1/"
    "CodeSystem-C4BBAdjudicationDiscriminator.html"
)


CMS_TEXT = r"""
CLM_BLOOD_CHRG_AMT|Blood Charge Amount
CLM_BLOOD_LBLTY_AMT|Beneficiary Blood Deductible Liability Amount
CLM_BLOOD_NCVRD_CHRG_AMT|Blood Noncovered Charge Amount
CLM_HIPPS_UNCOMPD_CARE_AMT|Claim Uncompensated Care Payment Amount
CLM_HIPPS_READMSN_RDCTN_AMT|Readmission Reduction Amount
CLM_HIPPS_VBP_AMT|HIPPS Value Based Purchasing Amount
CLM_INSTNL_LOW_VOL_PMT_AMT|Low Volume Payment Amount
CLM_INSTNL_PRFNL_AMT|Professional Component Charge Amount
CLM_MDCR_IP_1ST_YR_RATE_AMT|First Year Rate Amount
CLM_MDCR_IP_SCND_YR_RATE_AMT|Second Year Rate Amount
CLM_PPS_MD_WVR_STDZD_VAL_AMT|Maryland Waiver Standardized Amount
CLM_INSTNL_CVRD_DAY_CNT|Claim Medicare Utilization Day Count
CLM_INSTNL_DRG_OUTLIER_AMT|DRG Outlier Approved Payment Amount
CLM_INSTNL_MDCR_COINS_DAY_CNT|Beneficiary Total Coinsurance Days Count
CLM_INSTNL_NCVRD_DAY_CNT|Claim Medicare Non Utilization Days Count
CLM_INSTNL_PER_DIEM_AMT|Claim Pass Thru Per Diem Amount
CLM_MDCR_HOSPC_PRD_CNT|Hospice Period Count
CLM_MDCR_INSTNL_PRMRY_PYR_AMT|Primary Payer (if not Medicare) Claim Paid Amount
CLM_MDCR_IP_BENE_DDCTBL_AMT|Beneficiary Inpatient (or other Part A) Deductible Amount
CLM_MDCR_IP_LRD_USE_CNT|Beneficiary Medicare Lifetime Reserve Days (LRD) Used Count
CLM_MDCR_IP_PPS_CPTL_FSP_AMT|Claim PPS Capital Federal Specific Portion (FSP) Amount
CLM_MDCR_IP_PPS_CPTL_HRMLS_AMT|Claim PPS Old Capital Hold Harmless Amount
CLM_MDCR_IP_PPS_CPTL_IME_AMT|Claim PPS Capital Indirect Medical Education (IME) Amount
CLM_MDCR_IP_PPS_CPTL_TOT_AMT|Claim Total PPS Capital Amount
CLM_MDCR_IP_PPS_DRG_WT_NUM|PPS DRG Weight Number
CLM_MDCR_IP_PPS_DSPRPRTNT_AMT|Claim PPS Capital Disproportionate Share Amount
CLM_MDCR_IP_PPS_EXCPTN_AMT|Claim PPS Capital Exception Amount
CLM_MDCR_IP_PPS_OUTLIER_AMT|Claim PPS Capital Outlier Amount
CLM_MDCR_PRFNL_PRMRY_PYR_AMT|Primary Payer Paid Amount
CLM_OPRTNL_DSPRTNT_AMT|Operating Disproportionate Share Amount
CLM_OPRTNL_IME_AMT|Operating Indirect Medical Education Amount
CLM_ALOWD_CHRG_AMT|Allowed Charge Amount
CLM_BENE_PMT_AMT|Paid By Beneficiary Amount
CLM_MDCR_COINSRNC_AMT|Beneficiary Coinsurance Liability Amount
CLM_MDCR_DDCTBL_AMT|Beneficiary Deductible Amount
CLM_MDCR_INSTNL_BENE_PD_AMT|Institutional Paid to Beneficiary Amount
CLM_NCVRD_CHRG_AMT|Inpatient(or other Part A) Non-covered Charge Amount
CLM_OTHR_TP_PD_AMT|Other Third Party Payer Paid Amount
CLM_PRVDR_PMT_AMT|Provider Payment Amount
CLM_SBMT_CHRG_AMT|Total Charge Amount
TOT_RX_CST_AMT|Total RX Cost Amount
CLM_BENE_PRMRY_PYR_PD_AMT|Line Primary Payer Paid Amount
CLM_LINE_ADD_ON_PYMT_AMT|Add On Payment Amount
CLM_LINE_ALOWD_CHRG_AMT|Line Allowed Charge Amount
CLM_LINE_BENE_PD_AMT|Payment Amount to Beneficiary
CLM_LINE_BENE_PMT_AMT|Line Paid By Beneficiary Amount
CLM_LINE_BLOOD_DDCTBL_AMT|Blood Deductible Amount
CLM_LINE_CARR_PSYCH_OT_LMT_AMT|Therapy Amount Applied to Limit
CLM_LINE_CVRD_PD_AMT|Payment Amount
CLM_LINE_DMERC_SCRN_SVGS_AMT|Screen Savings Amount
CLM_LINE_GRS_ABOVE_THRSHLD_AMT|Gross Drug Cost Above Out Of Pocket Threshold
CLM_LINE_GRS_BLW_THRSHLD_AMT|Gross Drug Cost Below Out Of Pocket Threshold
CLM_LINE_INSTNL_ADJSTD_AMT|Revenue Center Coinsurance/Wage Adjusted Coinsurance Amount
CLM_LINE_INSTNL_MSP1_PD_AMT|Revenue Center 1st MSP Paid Amount
CLM_LINE_INSTNL_MSP2_PD_AMT|Revenue Center 2nd MSP Paid Amount
CLM_LINE_INSTNL_RATE_AMT|Revenue Center Rate Amount
CLM_LINE_INSTNL_RDCD_AMT|Revenue Center Reduced Coinsurance Amount
CLM_LINE_LIS_AMT|Low Income Cost Sharing Subsidy Amount
CLM_LINE_MDCR_COINSRNC_AMT|Coinsurance Amount
CLM_LINE_MDCR_DDCTBL_AMT|Cash Deductible Amount
CLM_LINE_NCVRD_CHRG_AMT|Non-Covered Charge Amount
CLM_LINE_PLRO_AMT|Patient Liability Reduction Other Paid Amount
CLM_LINE_PRFNL_DME_PRICE_AMT|Purchase Price Amount
CLM_LINE_PRFNL_INTRST_AMT|Professional Interest Amount
CLM_LINE_PRVDR_PMT_AMT|Line Provider Payment Amount
CLM_LINE_RPTD_GAP_DSCNT_AMT|Claim Line Reported Gap Discount Amount
CLM_LINE_SBMT_CHRG_AMT|Line Submitted Charge Amount
CLM_MDCR_PRMRY_PYR_ALOWD_AMT|Line Primary Payer Allowed Amount
CLM_REV_CNTR_TDAPA_AMT|Transitional Drug Add-On Payment Adjustment
"""


CMS_NON_MONETARY = {
    "CLM_INSTNL_CVRD_DAY_CNT",
    "CLM_INSTNL_MDCR_COINS_DAY_CNT",
    "CLM_INSTNL_NCVRD_DAY_CNT",
    "CLM_MDCR_HOSPC_PRD_CNT",
    "CLM_MDCR_IP_LRD_USE_CNT",
    "CLM_MDCR_IP_PPS_DRG_WT_NUM",
}


def _cms_map():

    result = {}

    for line in CMS_TEXT.strip().splitlines():

        code, display = line.split("|", 1)

        role = (
            "NON_MONETARY_VALUE"
            if code in CMS_NON_MONETARY
            else "MONETARY_AMOUNT"
        )

        result[code] = {
            "display": display,
            "semantic_role": role,
        }

    return result


CMS_CODES = _cms_map()


HL7_CODES = {
    "submitted": {
        "display": "Submitted Amount",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "eligible": {
        "display": "Eligible Amount",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "deductible": {
        "display": "Deductible",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "benefit": {
        "display": "Benefit Amount",
        "semantic_role": "MONETARY_AMOUNT",
    },
}


CARIN_CODES = {
    "coinsurance": {
        "display": "Co-insurance",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "noncovered": {
        "display": "Noncovered",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "priorpayerpaid": {
        "display": "Prior payer paid",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "paidbypatient": {
        "display": "Paid by patient",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "paidtopatient": {
        "display": "Paid to patient",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "paidtoprovider": {
        "display": "Paid to provider",
        "semantic_role": "MONETARY_AMOUNT",
    },
    "discount": {
        "display": "Discount",
        "semantic_role": "MONETARY_AMOUNT",
    },
}


DISCRIMINATOR_CODES = {
    "benefitpaymentstatus": {
        "display": "Benefit Payment Status",
        "semantic_role": "STATUS_DISCRIMINATOR",
    },
}


SYSTEM_CONFIG = {
    CMS_ADJUDICATION: {
        "codes": CMS_CODES,
        "authority": "CMS Blue Button API",
        "authority_version": "Blue Button v3",
        "authority_url": CMS_SOURCE,
    },

    HL7_ADJUDICATION: {
        "codes": HL7_CODES,
        "authority": "HL7 Terminology",
        "authority_version": "THO 7.4.0 / CodeSystem 1.0.1",
        "authority_url": HL7_SOURCE,
    },

    CARIN_ADJUDICATION: {
        "codes": CARIN_CODES,
        "authority": "HL7 CARIN Blue Button IG",
        "authority_version": "2.1.0",
        "authority_url": CARIN_SOURCE,
    },

    CARIN_DISCRIMINATOR: {
        "codes": DISCRIMINATOR_CODES,
        "authority": "HL7 CARIN Blue Button IG",
        "authority_version": "2.1.0",
        "authority_url": CARIN_DISCRIMINATOR_SOURCE,
    },
}


def aggregation_rule(role):

    if role == "MONETARY_AMOUNT":
        return (
            "SAME_SYSTEM_CODE_CURRENCY_AND_GRAIN_ONLY"
        )

    if role == "NON_MONETARY_VALUE":
        return (
            "NOT_CURRENCY_REQUIRE_MEANINGFUL_UNIT"
        )

    if role == "STATUS_DISCRIMINATOR":
        return "NOT_SUMMABLE"

    return "UNRESOLVED"


def resolve_financial_code(system, code):

    config = SYSTEM_CONFIG.get(system)

    if not config:
        return None

    concept = config["codes"].get(code)

    if not concept:
        return None

    role = concept["semantic_role"]

    return {
        "system_uri": system,
        "code": code,
        "authoritative_display":
            concept["display"],
        "semantic_role": role,
        "aggregation_rule":
            aggregation_rule(role),
        "authority":
            config["authority"],
        "authority_version":
            config["authority_version"],
        "authority_url":
            config["authority_url"],
        "resolution_status":
            "AUTHORITATIVELY_RESOLVED",
        "kpi_status":
            "NOT_APPROVED",
    }


AUTHORITATIVE_FINANCIAL_CODES = {
    (system, code)
    for system, config
    in SYSTEM_CONFIG.items()
    for code in config["codes"]
}
