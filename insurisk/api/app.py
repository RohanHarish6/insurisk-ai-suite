from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import Dict, Any

from insurisk.underwriting.schemas import UnderwritingRequest, UnderwritingBrief
from insurisk.underwriting.engine import UnderwritingEngine
from insurisk.fraud.schemas import FraudNetworkRequest, FraudInspectionResponse
from insurisk.fraud.engine import FraudEngine

app = FastAPI(
    title="InsuRisk-AI: Enterprise Underwriting Intake & Claim Fraud Analytics Suite",
    version="1.0.0",
    description="Advanced Commercial Underwriting Copilot & Graph-based SIU Claim Fraud Analytics Engine."
)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>InsuRisk-AI Suite</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #060911; color: #f8fafc; padding: 40px; }
                .card { background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 30px; max-width: 800px; margin: auto; }
                h1 { color: #38bdf8; margin-top: 0; }
                .badge { background: #10b981; color: #060911; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-size: 0.85rem; }
                ul { line-height: 1.8; }
                a { color: #38bdf8; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>InsuRisk-AI Suite <span class="badge">Active</span></h1>
                <p>Enterprise Underwriting Intake & Claim Fraud Analytics REST Service.</p>
                <h3>Available Endpoints</h3>
                <ul>
                    <li><code>POST /api/v1/underwrite/analyze</code> - Commercial Underwriting Copilot risk assessment.</li>
                    <li><code>POST /api/v1/fraud/inspect-network</code> - SIU Claim Fraud graph collusion ring detection.</li>
                    <li><a href="/docs" target="_blank">Interactive Swagger Documentation (/docs)</a></li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.post("/api/v1/underwrite/analyze", response_model=UnderwritingBrief)
def analyze_underwriting(request: UnderwritingRequest) -> UnderwritingBrief:
    try:
        return UnderwritingEngine.analyze_risk(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/fraud/inspect-network", response_model=FraudInspectionResponse)
def inspect_fraud_network(request: FraudNetworkRequest) -> FraudInspectionResponse:
    try:
        return FraudEngine.inspect_network(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
