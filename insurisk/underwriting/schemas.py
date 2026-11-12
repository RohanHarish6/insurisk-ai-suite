from typing import List
from pydantic import BaseModel, Field, ConfigDict

class LossEvent(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    loss_id: str
    date: str
    amount: float = Field(ge=0)
    description: str
    loss_type: str  # e.g., "Property", "Liability", "Auto"
    at_fault: bool

class LossRunReport(BaseModel):
    policy_id: str
    insured_name: str
    policy_year: int
    loss_events: List[LossEvent] = Field(default_factory=list)

class UnderwritingRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    policy_id: str
    insured_name: str
    loss_run_reports: List[LossRunReport] = Field(min_length=1)
    annual_revenue: float = Field(gt=0)
    employee_count: int = Field(ge=0)
    industry_code: str
    requested_limit: float = Field(gt=0)

class RiskFactor(BaseModel):
    factor_name: str
    score: float = Field(ge=0, le=100)
    description: str

class UnderwritingBrief(BaseModel):
    policy_id: str
    insured_name: str
    composite_risk_score: float = Field(ge=0, le=100)
    recommendation: str  # "APPROVE", "REFER", "DECLINE"
    risk_factors: List[RiskFactor]
    total_loss_amount: float
    frequency_per_year: float
    pricing_multiplier: float = Field(gt=0)
    summary_narrative: str
