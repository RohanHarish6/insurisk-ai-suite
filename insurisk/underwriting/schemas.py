from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LossEvent(BaseModel):
    loss_id: str
    date: str
    amount: float
    description: str
    loss_type: str  # e.g., "Property", "Liability", "Auto"
    at_fault: bool

class LossRunReport(BaseModel):
    policy_id: str
    insured_name: str
    policy_year: int
    loss_events: List[LossEvent] = Field(default_factory=list)

class UnderwritingRequest(BaseModel):
    policy_id: str
    insured_name: str
    loss_run_reports: List[LossRunReport]
    annual_revenue: float
    employee_count: int
    industry_code: str
    requested_limit: float

class RiskFactor(BaseModel):
    factor_name: str
    score: float  # 0 to 100, where higher is riskier
    description: str

class UnderwritingBrief(BaseModel):
    policy_id: str
    insured_name: str
    composite_risk_score: float  # 0 to 100
    recommendation: str  # "APPROVE", "REFER", "DECLINE"
    risk_factors: List[RiskFactor]
    total_loss_amount: float
    frequency_per_year: float
    pricing_multiplier: float
    summary_narrative: str
