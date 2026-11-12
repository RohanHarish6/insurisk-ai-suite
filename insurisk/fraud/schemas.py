from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class ClaimEntity(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    claim_id: str
    claimant_id: str
    provider_id: str
    vehicle_vin: Optional[str] = None
    address: str
    claim_amount: float = Field(ge=0)
    is_suspicious_flag: bool = False

class FraudNetworkRequest(BaseModel):
    claims: List[ClaimEntity] = Field(min_length=1)

class FraudClusterResult(BaseModel):
    cluster_id: int
    members: List[str]
    shared_attributes: List[str]
    risk_score: float = Field(ge=0, le=100)
    recommendation: str
    evidence: List[str] = Field(default_factory=list)

class FraudInspectionResponse(BaseModel):
    total_claims_analyzed: int
    clusters_detected: int
    high_risk_rings: List[FraudClusterResult]
    network_density: float = Field(ge=0, le=1)
