import unittest
from insurisk.fraud.schemas import FraudNetworkRequest, ClaimEntity
from insurisk.fraud.engine import FraudEngine

class TestFraudEngine(unittest.TestCase):
    def test_fraud_network_detection(self):
        claims = [
            ClaimEntity(
                claim_id="CLM-001",
                claimant_id="CLMT-100",
                provider_id="PROV-999",
                vehicle_vin="VIN123456789",
                address="123 Main St, Miami FL",
                claim_amount=45000.0,
                is_suspicious_flag=True
            ),
            ClaimEntity(
                claim_id="CLM-002",
                claimant_id="CLMT-101",
                provider_id="PROV-999",
                vehicle_vin="VIN123456789", # Shared VIN / staged accident indicator
                address="123 Main St, Miami FL", # Shared Address
                claim_amount=52000.0,
                is_suspicious_flag=True
            ),
            ClaimEntity(
                claim_id="CLM-003",
                claimant_id="CLMT-102",
                provider_id="PROV-999",
                vehicle_vin="VIN999999999",
                address="123 Main St, Miami FL",
                claim_amount=48000.0,
                is_suspicious_flag=True
            )
        ]
        
        req = FraudNetworkRequest(claims=claims)
        res = FraudEngine.inspect_network(req)
        
        self.assertEqual(res.total_claims_analyzed, 3)
        self.assertGreaterEqual(res.clusters_detected, 1)
        self.assertTrue(any("REFER TO SIU" in ring.recommendation for ring in res.high_risk_rings))
        self.assertTrue(all(ring.evidence for ring in res.high_risk_rings))

if __name__ == "__main__":
    unittest.main()
