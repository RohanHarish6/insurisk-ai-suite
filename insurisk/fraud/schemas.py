from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ClaimEntity(BaseModel):
    claim_id: str
    claimant_id: str
    provider_id: str
    vehicle_vin: Optional[str] = None
    address: str
    claim_amount: float
    is_suspicious_flag: bool = False

class FraudNetworkRequest(BaseModel):
    claims: List[ClaimEntity]

class FraudClusterResult(BaseModel):
    cluster_id: int
    members: List[str]
    shared_attributes: List[str]
    risk_score: float
    recommendation: str

class FraudInspectionResponse(BaseModel):
    total_claims_analyzed: int
    clusters_detected: int
    high_risk_rings: List[FraudClusterResult]
    network_density: float
