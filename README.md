# FoodWise AI – Smart Food Waste Reduction and Sustainable Redistribution Ecosystem

**Problem Statement ID:** 26234  
**Organization:** Ministry of Food Processing Industries (MoFPI)  
**Category:** Software  
**Theme:** Agriculture, FoodTech & Rural Development

---

## 1. Executive Summary

**FoodWise AI** is a modern, intelligent, end-to-end software ecosystem designed to eradicate food waste across institutional kitchens (college cafeterias, hotels, catering centers), food processing units, and NGOs/food banks. 

The platform delivers:
- **AI-Driven Demand Forecasting:** Random Forest Regression predicting daily consumption to eliminate overpreparation buffer bloat.
- **Smart Food Quality Triage & Expiry Tracker:** Computer vision image screening for surface deterioration paired with real-time cold storage IoT telemetry.
- **Surplus Food Marketplace & NGO Matching:** Automated detection of surplus food, feasibility scoring, and 1-click redistribution listings.
- **AI Route Optimization:** 2-Opt & deadline-prioritizing A* multi-stop route planner rendered on interactive OpenStreetMap.
- **Industrial Processing Unit Monitoring:** Raw material yield tracking, machine downtime telemetry (OEE), and specific energy consumption (kWh/kg).
- **Operational Inefficiency & Anomaly Detection:** IsolationForest algorithms detecting abnormal plate waste spikes and machinery thermal stress.
- **Verifiable ESG Sustainability Analytics:** Carbon emissions avoided (2.5 kg CO2e / kg food), virtual water conserved (290 L / kg), and energy saved (3.2 kWh / kg) with downloadable PDF and CSV reports.
- **Smart Production Planning:** Holistic multi-variable optimization integrating forecasts, expiring pantry inventory, and past waste rates with Explainable AI reasoning.

---

## 2. Technology Stack

### Frontend
- **Framework:** React.js (Vite build engine)
- **Styling:** Tailwind CSS (Emerald & Slate modern SaaS design)
- **Visualizations:** Recharts (Area charts, Bar charts, Responsive containers)
- **Icons:** Lucide React
- **Geographic Mapping:** Leaflet & React-Leaflet with OpenStreetMap tiles

### Backend
- **Framework:** Python FastAPI (Asynchronous REST API)
- **Authentication:** JWT tokens (HS256) & Bcrypt password hashing
- **Authorization:** Role-Based Access Control (RBAC) across 4 roles
- **Reporting Engine:** ReportLab for audit-grade PDF generation & Python CSV streamer

### Database
- **ORM:** SQLAlchemy 2.0 with normalized schema (22 tables)
- **Database Engine:** Compatible with PostgreSQL & SQLite (configured via `DATABASE_URL`)
- **Schema DDL:** Full relational PostgreSQL script in `backend/database_schema.sql`

### Artificial Intelligence & Machine Learning
- **Libraries:** Scikit-Learn, Pandas, NumPy, Pillow, Joblib
- **Demand Forecasting:** Random Forest Regressor (`demand_rf_model.joblib`) with $R^2 \approx 0.996$
- **Computer Vision:** Image degradation analysis (browning index, color uniformity, surface defect scoring)
- **Anomaly Detection:** Scikit-Learn `IsolationForest` & statistical Z-scores for waste spikes and machine inefficiencies
- **Route Optimizer:** Multi-stop Traveling Salesperson heuristic (Greedy Nearest Neighbor + 2-Opt with safe-use deadline weighting)

---

## 3. User Roles & Seeded Credentials

FoodWise AI supports 4 distinct user roles with dedicated interfaces and instant 1-click switching from the top navigation bar:

| Role | Name | Email | Password | Scope & Permissions |
|---|---|---|---|---|
| **Administrator** | Dr. Rajesh Sharma | `admin@foodwise.gov.in` | `Password123!` | National MoFPI oversight, verified institutions, NGO approvals, policy ESG audits |
| **Kitchen Manager** | Ananya Desai | `kitchen@delhitechnical.edu` | `Password123!` | Attendance logging, ML demand forecasting, image quality triage, cold storage IoT, surplus donation |
| **Processing Lead** | Vikram Malhotra | `processing@agrofresh.in` | `Password123!` | Raw material yields, machine downtime & OEE, energy intensity (kWh/kg), anomaly alerts |
| **NGO / Food Bank** | Meera Sen | `contact@aahaarngo.org` | `Password123!` | Nearby surplus food discovery, acceptance, cold-chain van dispatch, delivery confirmation |

---

## 4. Complete 10-Step Operational Workflow

FoodWise AI implements the full end-to-end workflow specified in Problem Statement 26234:

1. **Consumption Logging:** Kitchen manager enters dining hall attendance (e.g., 520 diners) and meal service details.
2. **AI Demand Prediction:** Random Forest model predicts exact portion demand (520 portions) and tight 4% safety buffer.
3. **Optimized Production Guidance:** System recommends preparing 545 portions, preventing 55 portions of overproduction waste compared to traditional 600 portions.
4. **Production & Service Recording:** Actual diner turnout and meal distribution are recorded.
5. **Surplus Auto-Identification:** The delta between prepared portions and diners served is automatically flagged as edible surplus.
6. **1-Click Redistribution Listing:** Surplus item is listed with preparation timestamp, storage spec, pickup GPS, and 4-hour safe-use deadline.
7. **Nearby NGO Acceptance:** Matching algorithm ranks local food banks; Aahaar Foundation reviews feasibility and accepts the donation.
8. **AI Route Logistics:** Interactive OpenStreetMap displays the multi-stop pickup and drop circuit with estimated travel time (38 mins).
9. **Cold-Chain Delivery Tracking:** Status advances through: `AVAILABLE` → `ACCEPTED` → `PICKUP_SCHEDULED` → `COLLECTED` → `DELIVERED` → `COMPLETED`.
10. **Sustainability & ESG Audit:** Platform updates carbon avoided (2.5 kg CO2e / kg), water conserved (290 L / kg), and enables instant PDF/CSV audit export.

---

## 5. Project Structure

```
foodwise-ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── auth.py              # JWT authentication & role-based endpoints
│   │   │   ├── admin.py             # Administrator platform metrics & directory
│   │   │   ├── kitchen.py           # Demand forecasting & kitchen inventory
│   │   │   ├── quality.py           # Computer vision image quality triage
│   │   │   ├── iot.py               # Cold storage sensory telemetry & simulation
│   │   │   ├── redistribution.py    # Surplus donation marketplace & acceptance
│   │   │   ├── routing.py           # Multi-stop logistics route planner
│   │   │   ├── processing.py        # Industrial unit yield & machine monitoring
│   │   │   └── analytics.py         # ESG metrics, PDF & CSV export, Module 8 planner
│   │   ├── core/
│   │   │   ├── config.py            # Environment settings
│   │   │   ├── database.py          # SQLAlchemy session & engine
│   │   │   └── security.py          # Bcrypt hashing & JWT token verification
│   │   ├── ml/
│   │   │   ├── demand_forecasting.py# Random Forest demand prediction model
│   │   │   ├── quality_classifier.py# Computer vision freshness analysis
│   │   │   ├── anomaly_detector.py  # IsolationForest waste & downtime detector
│   │   │   ├── route_optimizer.py   # Multi-stop TSP route planner
│   │   │   ├── train_demand_model.py# Standalone ML training script
│   │   │   └── trained_models/      # Persisted .joblib model artifacts
│   │   ├── models/                  # 22 Normalized SQLAlchemy database models
│   │   ├── schemas/                 # Pydantic validation schemas
│   │   └── main.py                  # FastAPI application entry point
│   ├── database_schema.sql          # Relational PostgreSQL DDL script
│   ├── seed_data.py                 # Initial realistic database seeding
│   ├── requirements.txt             # Python package dependencies
│   ├── .env.example                 # Environment configuration template
│   └── .env                         # Active configuration
├── frontend/
│   ├── src/
│   │   ├── components/common/       # Navbar, Sidebar, StatCard
│   │   ├── context/AuthContext.jsx  # User session & 1-click role switcher
│   │   ├── pages/
│   │   │   ├── Overview.jsx         # Architecture & 10-step lifecycle
│   │   │   ├── AdminDashboard.jsx   # MoFPI Administrator Command Center
│   │   │   ├── KitchenDashboard.jsx # Kitchen demand AI, inventory & surplus
│   │   │   ├── QualityAndIotPage.jsx# Vision screening & IoT cold storage
│   │   │   ├── ProcessingUnitDashboard.jsx # Industrial processing & machinery
│   │   │   ├── NgoDashboard.jsx     # NGO donation marketplace & dispatch
│   │   │   ├── RouteOptimizationPage.jsx # OpenStreetMap route logistics
│   │   │   ├── SustainabilityDashboard.jsx # ESG analytics, charts & reports
│   │   │   └── ProductionPlannerPage.jsx # Module 8 holistic planner
│   │   ├── services/api.js          # REST API client connecting to FastAPI
│   │   ├── App.jsx                  # Root layout & page switcher
│   │   └── index.css                # Tailwind directives & Leaflet styling
│   ├── tailwind.config.js           # Theme and color extensions
│   ├── vite.config.js               # Vite bundler configuration
│   └── package.json                 # Node.js dependencies
├── start.bat                        # Windows 1-click startup batch script
├── start.ps1                        # PowerShell 1-click startup script
└── README.md                        # Documentation
```

---

## 6. Installation & Execution Guide

### Prerequisites
- Python 3.10+ (installed on system)
- Node.js v18+ & npm (installed on system)

### Quick Start (Automated)
Run the startup script from the root project folder:
```powershell
.\start.ps1
```
Or double-click `start.bat`.

### Manual Step-by-Step Launch

#### 1. Backend Setup:
```bash
cd backend
python -m pip install -r requirements.txt
python seed_data.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API is live at: `http://localhost:8000`
- Interactive Swagger documentation: `http://localhost:8000/docs`

#### 2. Frontend Setup:
In a separate terminal:
```bash
cd frontend
npm install
npm run dev
```
- Web Application is live at: `http://localhost:5173`

---

## 7. ESG Conversion Factor Standards

All sustainability metrics computed on the platform adhere to documented international standards:

1. **Carbon Emissions Avoidance:**  
   $$\text{Emissions Avoided (kg CO}_2\text{e)} = \text{Food Waste Prevented (kg)} \times 2.5$$  
   *Source: EPA Waste Reduction Model (WARM) & FAO Food Wastage Footprint standard.*
2. **Virtual Water Conserved:**  
   $$\text{Water Saved (Liters)} = \text{Food Waste Prevented (kg)} \times 290.0$$  
   *Source: Water Footprint Network baseline for composite agricultural and cooked diets.*
3. **Embodied Energy Conserved:**  
   $$\text{Energy Saved (kWh)} = \text{Food Waste Prevented (kg)} \times 3.2$$  
   *Source: Agricultural primary energy and cold-chain storage baseline.*

---

## 8. Alignment with Problem Statement 26234

- ✅ **No static UI prototypes:** Fully dynamic, database-driven React application backed by active FastAPI REST endpoints.
- ✅ **Random Forest Demand Model:** Trained, saved, and performing low-latency inference on demand.
- ✅ **Image-Based Quality Screening:** Real image upload and visual attribute defect analysis with explicit food safety caveats.
- ✅ **IoT Cold Storage:** Live simulated telemetry stream with safety threshold breach alerts.
- ✅ **Route Optimization:** Multi-drop algorithm considering food expiry urgency and OpenStreetMap map visualization.
- ✅ **Industrial Monitoring:** Material loss, machine downtime, and energy intensity tracking for food processing units.
- ✅ **Audit Reports:** One-click download of audit-grade PDF and raw CSV reports.
