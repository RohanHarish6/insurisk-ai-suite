import unittest
from fastapi.testclient import TestClient
from insurisk.api.app import app

class TestFastAPIApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("InsuRisk-AI Suite", response.text)

    def test_underwrite_api(self):
        payload = {
            "policy_id": "POL-9999",
            "insured_name": "Test Freight Corp",
            "loss_run_reports": [
                {
                    "policy_id": "POL-9999",
                    "insured_name": "Test Freight Corp",
                    "policy_year": 2022,
                    "loss_events": [
                        {
                            "loss_id": "LE-1",
                            "date": "2022-07-10",
                            "amount": 12000.0,
                            "description": "Dock collision",
                            "loss_type": "Liability",
                            "at_fault": True
                        }
                    ]
                }
            ],
            "annual_revenue": 10000000.0,
            "employee_count": 80,
            "industry_code": "484121",
            "requested_limit": 2000000.0
        }
        response = self.client.post("/api/v1/underwrite/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["policy_id"], "POL-9999")
        self.assertIn("recommendation", data)

    def test_fraud_api(self):
        payload = {
            "claims": [
                {
                    "claim_id": "C-1",
                    "claimant_id": "CLM-1",
                    "provider_id": "PRV-1",
                    "vehicle_vin": "ABC123XYZ",
                    "address": "456 Oak Rd",
                    "claim_amount": 30000.0
                },
                {
                    "claim_id": "C-2",
                    "claimant_id": "CLM-2",
                    "provider_id": "PRV-1",
                    "vehicle_vin": "ABC123XYZ",
                    "address": "456 Oak Rd",
                    "claim_amount": 35000.0
                }
            ]
        }
        response = self.client.post("/api/v1/fraud/inspect-network", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total_claims_analyzed"], 2)
        self.assertIn("clusters_detected", data)

if __name__ == "__main__":
    unittest.main()
