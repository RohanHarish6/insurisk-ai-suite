# InsuRisk-AI: Enterprise Underwriting Intake & Claim Fraud Analytics Suite

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0%2B-orange.svg)](https://networkx.org/)
[![Pytest](https://img.shields.io/badge/pytest-passing-success.svg)](https://pytest.org/)

An enterprise-grade, high-performance insurance technology platform featuring an automated **Commercial Underwriting Copilot** and a graph-based **SIU Claim Fraud Analytics Engine** powered by FastAPI, Pydantic, and NetworkX.

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    subgraph InsuRisk-AI Suite
        A[Loss-Run Reports & Financials] --> B(Commercial Underwriting Copilot)
        B --> C[Composite Risk Score & Pydantic Brief]
        
        D[Claim Intakes & Entities] --> E(SIU Fraud Analytics Engine)
        E --> F[NetworkX Bipartite Graph & Anomaly Scoring]
        F --> G[Collusion Rings & SIU Referrals]
        
        H[FastAPI REST API & UI] --> B
        H --> E
    end
```

---

## 🚀 Quickstart

1. **Clone & Navigate**:
   ```bash
   cd insurisk-ai-suite
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Test Suite**:
   ```bash
   python -m pytest -v
   ```

4. **Start the API Server**:
   ```bash
   uvicorn insurisk.api.app:app --reload --port 8000
   ```
   * Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger documentation.

---

## 📡 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Service overview & status dashboard |
| `/api/v1/underwrite/analyze` | `POST` | Commercial underwriting risk evaluation & pricing multiplier |
| `/api/v1/fraud/inspect-network` | `POST` | Graph-based collusion ring detection & multi-factor anomaly scoring |

---

## 💼 Resume & Portfolio Bullet Points

- **Engineered InsuRisk-AI**: Architected a commercial underwriting copilot and SIU fraud analytics suite in Python and FastAPI, processing multi-year loss runs and performing graph-based anomaly detection.
- **Advanced Graph Analytics**: Implemented multi-relational bipartite graph analysis using NetworkX to detect syndicated insurance fraud rings connecting claimants, medical providers, VINs, and addresses.
- **Enterprise-Grade Reliability**: Built robust Pydantic data validation pipelines with automated unit and API integration tests (`pytest`).
