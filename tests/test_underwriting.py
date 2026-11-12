import unittest
from insurisk.underwriting.schemas import UnderwritingRequest, LossRunReport, LossEvent
from insurisk.underwriting.engine import UnderwritingEngine

class TestUnderwritingEngine(unittest.TestCase):
    def test_risk_analysis_approval(self):
        req = UnderwritingRequest(
            policy_id="POL-1001",
            insured_name="Acme Logistics LLC",
            loss_run_reports=[
                LossRunReport(
                    policy_id="POL-1001",
                    insured_name="Acme Logistics LLC",
                    policy_year=2023,
                    loss_events=[
                        LossEvent(
                            loss_id="L-1",
                            date="2023-04-12",
                            amount=5000.0,
                            description="Minor bumper scratch",
                            loss_type="Auto",
                            at_fault=True
                        )
                    ]
                )
            ],
            annual_revenue=5000000.0,
            employee_count=45,
            industry_code="484110",
            requested_limit=1000000.0
        )
        brief = UnderwritingEngine.analyze_risk(req)
        self.assertEqual(brief.policy_id, "POL-1001")
        self.assertEqual(brief.recommendation, "APPROVE")
        self.assertLess(brief.composite_risk_score, 30.0)
        self.assertEqual(brief.pricing_multiplier, 0.95)

    def test_risk_analysis_decline(self):
        req = UnderwritingRequest(
            policy_id="POL-1002",
            insured_name="High Risk Transport Inc",
            loss_run_reports=[
                LossRunReport(
                    policy_id="POL-1002",
                    insured_name="High Risk Transport Inc",
                    policy_year=2023,
                    loss_events=[
                        LossEvent(loss_id="L-1", date="2023-01-10", amount=150000.0, description="Total loss collision", loss_type="Auto", at_fault=True),
                        LossEvent(loss_id="L-2", date="2023-05-20", amount=250000.0, description="Warehouse fire", loss_type="Property", at_fault=True),
                        LossEvent(loss_id="L-3", date="2023-09-15", amount=100000.0, description="Cargo spill", loss_type="Liability", at_fault=True)
                    ]
                )
            ],
            annual_revenue=2000000.0,
            employee_count=10,
            industry_code="484110",
            requested_limit=5000000.0
        )
        brief = UnderwritingEngine.analyze_risk(req)
        self.assertEqual(brief.recommendation, "DECLINE")
        self.assertGreaterEqual(brief.composite_risk_score, 70.0)

if __name__ == "__main__":
    unittest.main()
