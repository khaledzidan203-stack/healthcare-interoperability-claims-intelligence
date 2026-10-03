import unittest

from healthcare_claims.financial_terminology import (
    AUTHORITATIVE_FINANCIAL_CODES,
    CARIN_ADJUDICATION,
    CARIN_DISCRIMINATOR,
    CMS_ADJUDICATION,
    HL7_ADJUDICATION,
    resolve_financial_code,
)


class FinancialTerminologyTests(unittest.TestCase):

    def test_current_authoritative_pair_count(self):

        self.assertEqual(
            len(
                AUTHORITATIVE_FINANCIAL_CODES
            ),
            81,
        )

    def test_standard_money_concepts(self):

        for system, code in (
            (
                HL7_ADJUDICATION,
                "submitted",
            ),
            (
                CARIN_ADJUDICATION,
                "paidtoprovider",
            ),
            (
                CMS_ADJUDICATION,
                "CLM_LINE_ALOWD_CHRG_AMT",
            ),
        ):

            result = resolve_financial_code(
                system,
                code,
            )

            self.assertIsNotNone(result)

            self.assertEqual(
                result["semantic_role"],
                "MONETARY_AMOUNT",
            )

            self.assertEqual(
                result["kpi_status"],
                "NOT_APPROVED",
            )


    def test_checkpoint_7n_b2_cms_extension(self):

        expected = {
            "CLM_HIPPS_READMSN_RDCTN_AMT":
                "Readmission Reduction Amount",
            "CLM_HIPPS_VBP_AMT":
                "HIPPS Value Based Purchasing Amount",
            "CLM_INSTNL_LOW_VOL_PMT_AMT":
                "Low Volume Payment Amount",
            "CLM_INSTNL_PRFNL_AMT":
                "Professional Component Charge Amount",
            "CLM_MDCR_IP_1ST_YR_RATE_AMT":
                "First Year Rate Amount",
            "CLM_MDCR_IP_SCND_YR_RATE_AMT":
                "Second Year Rate Amount",
            "CLM_PPS_MD_WVR_STDZD_VAL_AMT":
                "Maryland Waiver Standardized Amount",
        }

        for code, display in expected.items():

            with self.subTest(code=code):

                result = resolve_financial_code(
                    CMS_ADJUDICATION,
                    code,
                )

                self.assertIsNotNone(result)

                self.assertEqual(
                    result["authoritative_display"],
                    display,
                )

                self.assertEqual(
                    result["semantic_role"],
                    "MONETARY_AMOUNT",
                )

                self.assertEqual(
                    result["aggregation_rule"],
                    "SAME_SYSTEM_CODE_CURRENCY_AND_GRAIN_ONLY",
                )

                self.assertEqual(
                    result["authority"],
                    "CMS Blue Button API",
                )

                self.assertEqual(
                    result["authority_version"],
                    "Blue Button v3",
                )

                self.assertEqual(
                    result["resolution_status"],
                    "AUTHORITATIVELY_RESOLVED",
                )

                self.assertEqual(
                    result["kpi_status"],
                    "NOT_APPROVED",
                )


    def test_non_monetary_cms_values_are_not_money(self):

        for code in (
            "CLM_INSTNL_CVRD_DAY_CNT",
            "CLM_MDCR_IP_LRD_USE_CNT",
            "CLM_MDCR_IP_PPS_DRG_WT_NUM",
        ):

            result = resolve_financial_code(
                CMS_ADJUDICATION,
                code,
            )

            self.assertEqual(
                result["semantic_role"],
                "NON_MONETARY_VALUE",
            )

    def test_benefit_payment_status_is_not_amount(self):

        result = resolve_financial_code(
            CARIN_DISCRIMINATOR,
            "benefitpaymentstatus",
        )

        self.assertEqual(
            result["semantic_role"],
            "STATUS_DISCRIMINATOR",
        )

        self.assertEqual(
            result["aggregation_rule"],
            "NOT_SUMMABLE",
        )


if __name__ == "__main__":
    unittest.main()
