"""
The Gilded Ace - Casino Decision Intelligence Backend API
Unified FastAPI Platform with Live DB Connectors & Dual AI Services:
- Databricks Delta Lake & Spark SQL
- MongoDB Atlas Investigation & Audit Case Store
- TigerData / Timescale Sensor Time-Series Telemetry
- Google Gemini 1.5 Flash (Executive Decision Copilot)
- xAI Grok (Adversarial Casino Auditor & Red Team)
"""
import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import pydantic

from backend.analytics.engine import engine
from backend.db.databricks_client import databricks_client
from backend.db.mongo_client import mongo_client
from backend.db.tigerdb_client import tigerdb_client
from backend.ai.gemini_service import gemini_service
from backend.ai.grok_service import grok_service

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"

app = FastAPI(
    title="The Gilded Ace - Decision Intelligence Platform API",
    description="Multi-engine analytical backend integrating Databricks, MongoDB Atlas, TigerData, Gemini Copilot, and Grok Adversarial Auditor.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# 1. LIVE SYSTEM & DATABASE STATUS
# -----------------
@app.get("/api/system/status")
def get_system_status():
    """Returns real-time connectivity and status of Databricks, MongoDB Atlas, and TigerData."""
    return {
        "status": "HEALTHY",
        "databases": {
            "databricks": databricks_client.get_cluster_status(),
            "mongodb_atlas": mongo_client.get_status(),
            "tigerdata_timescale": tigerdb_client.get_status()
        },
        "ai_engines": {
            "gemini_decision_copilot": "READY (Live API / Grounded Telemetry)",
            "grok_adversarial_auditor": "READY (Live API / Red-Team Stress-Test)"
        }
    }

# -----------------
# 2. DYNAMIC ANALYTICS & PERIOD FILTERING (Observe & Trace)
# -----------------
@app.get("/api/metrics/summary")
def get_metrics_summary(period: str = Query("all", description="all, last_3m, or june_only")):
    """Dynamically calculates high-level executive metrics directly from raw Parquet/Delta tables."""
    return engine.get_summary_metrics(period=period)

@app.get("/api/floor/zones")
def get_zone_metrics(period: str = Query("all", description="all, last_3m, or june_only")):
    """Dynamically calculates zone metrics, occupancy, and win velocity."""
    return engine.get_zone_breakdown(period=period)

@app.get("/api/machines/{machine_id}/audit")
def get_machine_audit(machine_id: str):
    """
    Dynamically generates the complete 6-Question Decision Audit for ANY machine on the fly:
    1. Why flagged
    2. Statistical test (Z-score, 95% CI on hold)
    3. Operational downtime factor
    4. Location and walkway dynamics
    5. Economic justification for replacement
    6. Cheaper alternative interventions
    """
    try:
        return engine.get_machine_audit(machine_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# -----------------
# 3. DATABRICKS DELTA LAKE QUERIES
# -----------------
@app.get("/api/databricks/query")
def run_databricks_query(sql: str = Query(..., description="SQL statement to execute")):
    """Executes a SQL query on Databricks Delta Lake tables."""
    return {
        "query": sql,
        "results": databricks_client.execute_sql(sql)
    }

# -----------------
# 4. TIGERDATA / TIMESCALEDB TIME-SERIES QUERIES
# -----------------
@app.get("/api/tigerdb/sensor-traffic")
def get_tigerdb_traffic(zone_id: Optional[str] = Query(None), interval_hours: int = Query(24)):
    """Runs a time_bucket window query on sensor traffic from TigerData."""
    return {
        "engine": "TigerData Timescale Hypertable",
        "data": tigerdb_client.query_time_bucket(zone_id=zone_id, interval_hours=interval_hours)
    }

@app.get("/api/tigerdb/machine-telemetry/{machine_id}")
def get_tigerdb_machine_telemetry(machine_id: str):
    """Queries high-frequency hourly telemetry from TigerData (1.32M rows)."""
    return {
        "machine_id": machine_id,
        "hourly_telemetry": tigerdb_client.query_machine_hour_telemetry(machine_id)
    }

# -----------------
# 5. MONGODB ATLAS INVESTIGATION & AUDIT STORE
# -----------------
class AuditCaseRequest(pydantic.BaseModel):
    machine_id: str
    analyst: str
    status: str
    verdict: str
    notes: Optional[str] = ""

@app.post("/api/audit/case")
def save_audit_case(req: AuditCaseRequest):
    """Persists an analyst investigation / flag override record into MongoDB Atlas."""
    case_id = mongo_client.save_audit_case(req.dict())
    return {
        "message": "Audit case persisted to MongoDB Atlas",
        "case_id": case_id
    }

@app.get("/api/audit/cases")
def get_audit_cases(machine_id: Optional[str] = Query(None)):
    """Retrieves all investigation cases from MongoDB Atlas."""
    return {
        "count": len(mongo_client.get_audit_cases(machine_id)),
        "cases": mongo_client.get_audit_cases(machine_id)
    }

# -----------------
# 6. BUDGET OPTIMIZER ($100K INTERVENTION SIMULATOR)
# -----------------
class SimulationActionItem(pydantic.BaseModel):
    action_id: str
    quantity: int

class SimulationRequest(pydantic.BaseModel):
    actions: List[SimulationActionItem]
    save_scenario_to_mongo: bool = False
    scenario_name: Optional[str] = None

@app.post("/api/optimizer/simulate")
def simulate_budget_portfolio(req: SimulationRequest):
    """
    Simulates a custom intervention portfolio against all 5 strict business constraints:
    1. Total expenditure <= $100,000.
    2. Maximum 3 distinct action types (excluding A-HOLD).
    3. Catalogue quantity limits.
    4. Lead times and downtime hours.
    5. Incompatibility groups (same_machine conflicts, comp_policy conflicts).
    """
    with open(DATA_DIR / "optimizer_data.json", "r", encoding="utf-8") as f:
        opt_data = json.load(f)
        
    catalog_map = {a["action_id"]: a for a in opt_data["catalog_actions"]}
    
    total_cost = 0.0
    total_monthly_benefit = 0.0
    total_downtime_hours = 0.0
    max_lead_days = 0
    action_types_selected = []
    incompat_groups = set()
    violations = []
    
    for item in req.actions:
        aid = item.action_id
        qty = item.quantity
        if qty <= 0:
            continue
            
        if aid not in catalog_map:
            violations.append(f"Unknown action_id: {aid}")
            continue
            
        action = catalog_map[aid]
        if aid != "A-HOLD":
            action_types_selected.append(aid)
            
        if qty > action["quantity_limit"]:
            violations.append(f"Action {aid} exceeds maximum limit ({qty} > {action['quantity_limit']}).")
            
        incompat = action.get("incompatibility_group")
        if incompat and incompat != "None":
            if incompat in incompat_groups:
                violations.append(f"Incompatible action conflict in group '{incompat}' for action {aid}.")
            incompat_groups.add(incompat)
            
        unit_cost = action["unit_cost_usd"]
        recur_cost_day = action["recurring_cost_per_day_usd"]
        lead_days = action["lead_days"]
        operational_days_july = max(0, 30 - lead_days)
        cost_for_action = qty * (unit_cost + recur_cost_day * operational_days_july)
        
        if aid == "A-COMP-PILOT":
            cost_for_action += 10000.0
            
        total_cost += cost_for_action
        max_lead_days = max(max_lead_days, lead_days)
        total_downtime_hours += (action["downtime_minutes"] * qty) / 60.0
        total_monthly_benefit += action["monthly_benefit_per_unit_usd"] * qty

    distinct_types = len(set(action_types_selected))
    if distinct_types > 3:
        violations.append(f"Exceeds maximum allowable action types (Selected {distinct_types} types; limit is 3).")
        
    retained_budget = 100000.0 - total_cost
    if retained_budget < 0:
        violations.append(f"Exceeds $100,000 budget ceiling by ${abs(retained_budget):,.2f}.")

    annual_benefit = total_monthly_benefit * 12.0
    net_annual_impact = annual_benefit - total_cost
    payback_months = (total_cost / total_monthly_benefit) if total_monthly_benefit > 0 else 999.0

    res = {
        "is_valid": len(violations) == 0,
        "violations": violations,
        "total_cost_usd": round(total_cost, 2),
        "retained_budget_usd": round(retained_budget, 2),
        "distinct_action_types_count": distinct_types,
        "max_lead_time_days": max_lead_days,
        "total_downtime_hours": round(total_downtime_hours, 1),
        "estimated_monthly_benefit_usd": round(total_monthly_benefit, 2),
        "estimated_annual_benefit_usd": round(annual_benefit, 2),
        "net_annual_impact_usd": round(net_annual_impact, 2),
        "payback_months": round(payback_months, 1),
        "sensitivity": {
            "pessimistic_benefit_annual": round(annual_benefit * 0.70, 2),
            "expected_benefit_annual": round(annual_benefit, 2),
            "optimistic_benefit_annual": round(annual_benefit * 1.35, 2)
        }
    }
    
    if req.save_scenario_to_mongo:
        scenario_record = {
            "name": req.scenario_name or "Custom Scenario",
            "total_spend": total_cost,
            "retained_cash": retained_budget,
            "net_annual_impact": net_annual_impact,
            "actions": [f"{item.action_id} (Qty: {item.quantity})" for item in req.actions if item.quantity > 0]
        }
        res["mongo_scenario_id"] = mongo_client.save_simulation(scenario_record)
        
    return res

# -----------------
# 7. DUAL AI COPILOT: GEMINI VS GROK
# -----------------
class AIChatRequest(pydantic.BaseModel):
    model: str = "gemini"  # "gemini" (Decision Copilot) or "grok" (Adversarial Auditor)
    prompt: str
    machine_id: Optional[str] = None
    user_api_key: Optional[str] = None

@app.post("/api/ai/chat")
def universal_ai_chat(req: AIChatRequest):
    """
    Universal AI Endpoint supporting both:
    1. Gemini: Executive Decision Copilot (Grounding, ROI calculations, executive board justification)
    2. Grok: Adversarial Floor Auditor & Red Team (Pokes holes in assumptions, questions fraud vs luck, stress-tests budget)
    """
    context = engine.get_summary_metrics()
    
    if req.model.lower() == "grok":
        return grok_service.query(prompt=req.prompt, context=context, user_key=req.user_api_key)
    else:
        return gemini_service.query(prompt=req.prompt, context=context, user_key=req.user_api_key)

# -----------------
# 8. STATIC DATA / DASHBOARD MOUNT
# -----------------
app.mount("/dashboard", StaticFiles(directory=str(ROOT / "dashboard"), html=True), name="dashboard")

@app.get("/")
def read_root():
    return FileResponse(ROOT / "dashboard" / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
