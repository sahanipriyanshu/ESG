# ESG Data Ingestion Prototype

An enterprise-grade, full-stack platform designed to securely ingest, normalize, and audit Environmental, Social, and Governance (ESG) data across multiple corporate sources.

## 🚀 Key Features

*   **Multi-Source Ingestion**: Automated pipelines for SAP ERP (Scope 1 fuels), Utility smart meters (Scope 2 electricity), and Travel APIs (Scope 3 business travel).
*   **Immutable Audit Logging**: Every state change, approval, or rejection is immutably logged using polymorphic relationships, proving data lineage to auditors.
*   **Analyst Review Workflow**: A dedicated review pipeline separating raw incoming telemetry from canonical, approved "Ledger" data.
*   **Anomaly Detection**: Automated flagging of suspicious records (e.g., negative fuel quantities, overlapping billing cycles, excessive hotel stays).

## 🛠️ Technology Stack

*   **Backend**: Django, Django REST Framework (DRF), PostgreSQL (via `dj-database-url`), Pandas (Data processing).
*   **Frontend**: React, Vite, Tailwind CSS (v3).
*   **Deployment Ready**: Configured for Railway (`railway.json`, `Procfile`) and Vercel (`vercel.json`).

## 📚 Documentation

For deep-dive technical details on how the system was designed, see the `docs/` folder:
*   [MODEL.md](./docs/MODEL.md) - Entity Relationship Diagram & Schema overview.
*   [DECISIONS.md](./docs/DECISIONS.md) - Architectural Decision Records (ADRs).
*   [TRADEOFFS.md](./docs/TRADEOFFS.md) - Conscious simplifications and their production paths.
*   [SOURCES.md](./docs/SOURCES.md) - Ingestion formats and payload schemas.

## 💻 Local Development Setup

To run this platform locally, you will need Node.js and Python 3 installed.

### 1. Start the Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the Django server
python manage.py runserver
```

### 2. Start the Frontend

In a new terminal window:

```bash
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

Navigate to `http://localhost:5174` in your browser. You can use the mock CSV files located in the `scratch/` directory to test the ingestion pipelines!
