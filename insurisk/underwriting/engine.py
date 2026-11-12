from typing import List
from .schemas import UnderwritingRequest, UnderwritingBrief, RiskFactor

class UnderwritingEngine:
    @staticmethod
    def analyze_risk(request: UnderwritingRequest) -> UnderwritingBrief:
        total_loss = 0.0
        total_events = 0
        at_fault_count = 0
        years = max(1, len(request.loss_run_reports))
        
        for report in request.loss_run_reports:
            for ev in report.loss_events:
                total_loss += ev.amount
                total_events += 1
                if ev.at_fault:
                    at_fault_count += 1

        frequency = total_events / years
        severity = (total_loss / total_events) if total_events > 0 else 0.0
        
        # Loss ratio proxy relative to revenue
        loss_ratio = (total_loss / request.annual_revenue) if request.annual_revenue > 0 else 0.1
        
        # Calculate risk factors
        factors: List[RiskFactor] = []
        
        freq_score = min(100.0, frequency * 25.0)
        factors.append(RiskFactor(
            factor_name="Loss Frequency",
            score=freq_score,
            description=f"Averaging {frequency:.1f} losses per policy year."
        ))
        
        sev_score = min(100.0, (severity / 50000.0) * 100.0)
        factors.append(RiskFactor(
            factor_name="Loss Severity",
            score=sev_score,
            description=f"Average loss amount of \${severity:,.2f} per incident."
        ))
        
        lr_score = min(100.0, loss_ratio * 500.0)
        factors.append(RiskFactor(
            factor_name="Loss-to-Revenue Ratio",
            score=lr_score,
            description=f"Losses represent {loss_ratio*100:.2f}% of annual revenue."
        ))
        
        fault_ratio = (at_fault_count / total_events) if total_events > 0 else 0.0
        fault_score = fault_ratio * 100.0
        factors.append(RiskFactor(
            factor_name="At-Fault Incident Ratio",
            score=fault_score,
            description=f"{at_fault_count} out of {total_events} incidents were at-fault."
        ))
        
        # Composite score calculation (weighted)
        composite = (freq_score * 0.3) + (sev_score * 0.3) + (lr_score * 0.3) + (fault_score * 0.1)
        composite = round(min(100.0, max(0.0, composite)), 2)
        
        # Determine recommendation & pricing multiplier
        if composite < 30.0:
            recommendation = "APPROVE"
            multiplier = 0.95
        elif composite < 70.0:
            recommendation = "REFER"
            multiplier = 1.15
        else:
            recommendation = "DECLINE"
            multiplier = 1.45
            
        narrative = (
            f"Underwriting evaluation for {request.insured_name} yielded a composite risk score of {composite}/100. "
            f"Total historical losses stand at \${total_loss:,.2f} across {total_events} events. "
            f"Based on loss frequency ({frequency:.1f}/yr) and severity (\${severity:,.2f}), the recommended "
            f"action is {recommendation} with a pricing adjustment multiplier of {multiplier}x."
        )
        
        return UnderwritingBrief(
            policy_id=request.policy_id,
            insured_name=request.insured_name,
            composite_risk_score=composite,
            recommendation=recommendation,
            risk_factors=factors,
            total_loss_amount=total_loss,
            frequency_per_year=frequency,
            pricing_multiplier=multiplier,
            summary_narrative=narrative
        )
