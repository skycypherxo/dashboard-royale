"""
MongoDB Atlas Client & Investigation Store for THE GILDED ACE.
Persists analyst investigations, machine override audits,
$100K budget simulation portfolios, and AI copilot dialogues.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

ROOT = Path(__file__).resolve().parents[2]
LOCAL_STORE = ROOT / "data" / "mongo_atlas_store.json"

class MongoAtlasClient:
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        self.uri = os.environ.get("MONGODB_URI")
        self.db_name = os.environ.get("MONGODB_DB", "gilded_ace_intelligence")
        self.is_connected = False
        self.client = None
        self.db = None
        
        if self.uri:
            try:
                from pymongo import MongoClient
                import certifi
                self.client = MongoClient(
                    self.uri,
                    tlsCAFile=certifi.where(),
                    tlsAllowInvalidCertificates=True,
                    serverSelectionTimeoutMS=2000
                )
                self.client.server_info()
                self.db = self.client[self.db_name]
                self.is_connected = True
                print("[MongoDB Atlas] Successfully connected to remote cluster.")
            except Exception as e:
                print(f"[MongoDB Atlas] Remote connection note: {e}")
                
        if not self.is_connected:
            self._init_local_store()

    def _init_local_store(self):
        if not LOCAL_STORE.exists():
            initial_data = {
                "audit_cases": [
                    {
                        "case_id": "AUDIT-M1158-001",
                        "machine_id": "M-1158",
                        "analyst": "Vaishnavi (Guests & BI Lead)",
                        "status": "EXONERATED_RETAIN",
                        "verdict": "Luck deficit of -$36,165 verified as binomial variance (Z=-20.21). Recommend A-INSPECT ($1,200).",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                ],
                "simulation_scenarios": [
                    {
                        "scenario_id": "SCEN-REC-JULY",
                        "name": "Recommended Balanced Portfolio",
                        "total_spend": 29000,
                        "retained_cash": 71000,
                        "net_annual_impact": 153400,
                        "actions": ["A-COMP-PILOT (1)", "A-PREVENTIVE (1)", "A-INSPECT (5)", "A-HOLD (1)"],
                        "timestamp": datetime.utcnow().isoformat()
                    }
                ],
                "chat_sessions": []
            }
            with open(LOCAL_STORE, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, indent=2)

    def _read_local(self) -> Dict[str, Any]:
        with open(LOCAL_STORE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_local(self, data: Dict[str, Any]):
        with open(LOCAL_STORE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def save_audit_case(self, case: Dict[str, Any]) -> str:
        case["timestamp"] = datetime.utcnow().isoformat()
        if self.is_connected and self.db is not None:
            res = self.db.audit_cases.insert_one(case)
            return str(res.inserted_id)
        else:
            store = self._read_local()
            case_id = f"AUDIT-{case.get('machine_id', 'GEN')}-{len(store['audit_cases'])+1:03d}"
            case["case_id"] = case_id
            store["audit_cases"].append(case)
            self._write_local(store)
            return case_id

    def get_audit_cases(self, machine_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if self.is_connected and self.db is not None:
            query = {"machine_id": machine_id} if machine_id else {}
            return list(self.db.audit_cases.find(query, {"_id": 0}))
        else:
            store = self._read_local()
            cases = store.get("audit_cases", [])
            if machine_id:
                cases = [c for c in cases if c.get("machine_id") == machine_id]
            return cases

    def save_simulation(self, scenario: Dict[str, Any]) -> str:
        scenario["timestamp"] = datetime.utcnow().isoformat()
        if self.is_connected and self.db is not None:
            res = self.db.simulation_scenarios.insert_one(scenario)
            return str(res.inserted_id)
        else:
            store = self._read_local()
            scen_id = f"SCEN-{len(store['simulation_scenarios'])+1:03d}"
            scenario["scenario_id"] = scen_id
            store["simulation_scenarios"].append(scenario)
            self._write_local(store)
            return scen_id

    def get_simulations(self) -> List[Dict[str, Any]]:
        if self.is_connected and self.db is not None:
            return list(self.db.simulation_scenarios.find({}, {"_id": 0}))
        else:
            return self._read_local().get("simulation_scenarios", [])

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": "ONLINE (Connected Atlas)" if self.is_connected else "ONLINE (Local Document Store)",
            "cluster": "cluster0.gilded-ace.mongodb.net",
            "database": self.db_name,
            "collections": ["audit_cases", "simulation_scenarios", "chat_sessions"],
            "total_audit_records": len(self.get_audit_cases())
        }

mongo_client = MongoAtlasClient()

