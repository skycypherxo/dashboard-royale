"""
Generate floor.html for Akshaya (Floor & ML Lead)
TAMU Datathon 2026 - Dashboard Royale

Generates a standalone, interactive, multi-period floor dashboard supporting:
- Full 6-month period (Jan–Jun)
- Last 3 months (Apr–Jun)
- June-only view
- Floor-to-zone-to-bank drill-down
- Machine performance comparisons & interactive scorecard
- Downtime & shift operational analysis
- ML demand forecasting model evaluation (Baseline vs Weekday MAEs)
"""
import duckdb
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_HTML = ROOT / "dashboard" / "floor.html"

con = duckdb.connect()

prep_path = (ROOT / "data/1_prepared_views/prepared_daily_view.parquet").as_posix()
prop_path = (ROOT / "data/1_prepared_views/property_day.parquet").as_posix()
cal_path = (ROOT / "data/2_machine_decision/calendar_day.parquet").as_posix()
ops_path = (ROOT / "data/2_machine_decision/operations.parquet").as_posix()

periods = {
    "all": {
        "label": "All 6 Months (Jan–Jun 2025)",
        "start": "2025-01-01",
        "end": "2025-06-30",
        "cond": "p.gaming_date >= DATE '2025-01-01' AND p.gaming_date <= DATE '2025-06-30'",
        "days": 181
    },
    "q2": {
        "label": "Last 3 Months (Apr–Jun 2025)",
        "start": "2025-04-01",
        "end": "2025-06-30",
        "cond": "p.gaming_date >= DATE '2025-04-01' AND p.gaming_date <= DATE '2025-06-30'",
        "days": 91
    },
    "jun": {
        "label": "June Only (Jun 2025)",
        "start": "2025-06-01",
        "end": "2025-06-30",
        "cond": "p.gaming_date >= DATE '2025-06-01' AND p.gaming_date <= DATE '2025-06-30'",
        "days": 30
    }
}

period_data = {}

for p_key, p_meta in periods.items():
    cond = p_meta["cond"]
    
    # 1. Floor KPIs
    q_kpi = f"""
    WITH daily AS (
        SELECT p.machine_id, p.gaming_date, p.coin_in_usd, p.house_win_usd, p.theo_usd,
               p.available_hours, p.occupied_hours, p.faults_opened, p.repair_cost_usd,
               (c.scheduled_seconds / 3600.0) as sched_h
        FROM read_parquet('{prep_path}') p
        JOIN read_parquet('{cal_path}') c ON p.gaming_date = c.gaming_date
        WHERE p.location_id IS NOT NULL AND {cond}
    ),
    mach_agg AS (
        SELECT machine_id,
               SUM(available_hours) as avail_h,
               SUM(occupied_hours) as occ_h,
               SUM(coin_in_usd) as coin,
               SUM(house_win_usd) as win,
               SUM(theo_usd) as theo,
               SUM(faults_opened) as faults,
               SUM(repair_cost_usd) as repair,
               SUM(GREATEST(0.0, sched_h - available_hours)) as downtime_h
        FROM daily
        GROUP BY machine_id
    )
    SELECT
        COUNT(*) as active_machines,
        ROUND(SUM(coin), 2) as total_coin,
        ROUND(SUM(win), 2) as total_win,
        ROUND(SUM(theo), 2) as total_theo,
        ROUND(SUM(win) / NULLIF(SUM(coin), 0) * 100.0, 2) as obs_hold_pct,
        ROUND(SUM(theo) / NULLIF(SUM(coin), 0) * 100.0, 2) as theo_hold_pct,
        ROUND(SUM(avail_h), 1) as total_avail_h,
        ROUND(SUM(occ_h), 1) as total_occ_h,
        ROUND(SUM(occ_h) / NULLIF(SUM(avail_h), 0) * 100.0, 2) as occupancy_pct,
        SUM(faults) as total_faults,
        ROUND(SUM(repair), 2) as total_repair_cost,
        ROUND(SUM(downtime_h), 1) as total_downtime_h,
        ROUND(SUM(downtime_h * (theo / NULLIF(avail_h, 0))), 2) as lost_theo_win
    FROM mach_agg;
    """
    kpi_res = con.execute(q_kpi).fetchone()
    
    kpis = {
        "active_machines": int(kpi_res[0]),
        "total_coin": float(kpi_res[1]),
        "total_win": float(kpi_res[2]),
        "total_theo": float(kpi_res[3]),
        "obs_hold_pct": float(kpi_res[4]),
        "theo_hold_pct": float(kpi_res[5]),
        "total_avail_h": float(kpi_res[6]),
        "total_occ_h": float(kpi_res[7]),
        "occupancy_pct": float(kpi_res[8]),
        "total_faults": int(kpi_res[9]),
        "total_repair_cost": float(kpi_res[10]),
        "total_downtime_h": float(kpi_res[11]),
        "lost_theo_win": float(kpi_res[12]),
        "days": p_meta["days"]
    }

    # 2. Zones & Banks Drill-down
    q_zones = f"""
    WITH active AS (
        SELECT p.machine_id, p.zone_name, p.bank_id, p.coin_in_usd, p.house_win_usd, p.theo_usd,
               p.available_hours, p.faults_opened, (c.scheduled_seconds / 3600.0) as sched_h
        FROM read_parquet('{prep_path}') p
        JOIN read_parquet('{cal_path}') c ON p.gaming_date = c.gaming_date
        WHERE p.location_id IS NOT NULL AND {cond}
    ),
    bank_agg AS (
        SELECT zone_name, bank_id,
               COUNT(DISTINCT machine_id) as machines,
               ROUND(SUM(coin_in_usd), 2) as coin_in,
               ROUND(SUM(house_win_usd), 2) as house_win,
               ROUND(SUM(theo_usd), 2) as theo_win,
               ROUND(SUM(available_hours), 1) as avail_h,
               SUM(faults_opened) as faults,
               ROUND(SUM(GREATEST(0.0, sched_h - available_hours)), 1) as downtime_h
        FROM active
        GROUP BY zone_name, bank_id
    )
    SELECT zone_name, bank_id, machines, coin_in, house_win, theo_win, avail_h, faults, downtime_h,
           ROUND(house_win / NULLIF(coin_in, 0) * 100.0, 2) as obs_hold,
           ROUND(theo_win / NULLIF(coin_in, 0) * 100.0, 2) as theo_hold,
           ROUND(coin_in / NULLIF(avail_h, 0), 2) as coin_per_hour,
           ROUND(theo_win / NULLIF(avail_h, 0), 2) as theo_per_hour
    FROM bank_agg
    ORDER BY zone_name, bank_id;
    """
    bank_rows = con.execute(q_zones).fetchall()
    
    zones_dict = {}
    for r in bank_rows:
        z_name = r[0]
        if z_name not in zones_dict:
            zones_dict[z_name] = {
                "zone_name": z_name,
                "machines": 0,
                "coin_in": 0.0,
                "house_win": 0.0,
                "theo_win": 0.0,
                "avail_h": 0.0,
                "faults": 0,
                "downtime_h": 0.0,
                "banks": []
            }
        b_info = {
            "bank_id": r[1],
            "machines": int(r[2]),
            "coin_in": float(r[3]),
            "house_win": float(r[4]),
            "theo_win": float(r[5]),
            "avail_h": float(r[6]),
            "faults": int(r[7]),
            "downtime_h": float(r[8]),
            "obs_hold_pct": float(r[9]),
            "theo_hold_pct": float(r[10]),
            "coin_per_hour": float(r[11]),
            "theo_per_hour": float(r[12])
        }
        zones_dict[z_name]["banks"].append(b_info)
        zones_dict[z_name]["machines"] += b_info["machines"]
        zones_dict[z_name]["coin_in"] += b_info["coin_in"]
        zones_dict[z_name]["house_win"] += b_info["house_win"]
        zones_dict[z_name]["theo_win"] += b_info["theo_win"]
        zones_dict[z_name]["avail_h"] += b_info["avail_h"]
        zones_dict[z_name]["faults"] += b_info["faults"]
        zones_dict[z_name]["downtime_h"] += b_info["downtime_h"]

    zone_list = []
    for z_name, z in zones_dict.items():
        c = z["coin_in"]
        w = z["house_win"]
        th = z["theo_win"]
        ah = z["avail_h"]
        zone_list.append({
            "zone_name": z_name,
            "machines": z["machines"],
            "coin_in": round(c, 2),
            "house_win": round(w, 2),
            "theo_win": round(th, 2),
            "obs_hold_pct": round(w / c * 100.0, 2) if c > 0 else 0,
            "theo_hold_pct": round(th / c * 100.0, 2) if c > 0 else 0,
            "coin_per_hour": round(c / ah, 2) if ah > 0 else 0,
            "theo_per_hour": round(th / ah, 2) if ah > 0 else 0,
            "faults": z["faults"],
            "downtime_h": round(z["downtime_h"], 1),
            "banks": sorted(z["banks"], key=lambda b: b["bank_id"])
        })
    zone_list = sorted(zone_list, key=lambda z: z["coin_in"], reverse=True)

    # 3. Machine Scorecard for the Period
    q_mach = f"""
    WITH active AS (
        SELECT p.*
        FROM read_parquet('{prep_path}') p
        WHERE p.location_id IS NOT NULL AND {cond}
    ),
    latest_loc AS (
        SELECT machine_id, zone_name, bank_id, location_id
        FROM (
            SELECT machine_id, zone_name, bank_id, location_id,
                   row_number() OVER (PARTITION BY machine_id ORDER BY gaming_date DESC) as rn
            FROM active
        )
        WHERE rn = 1
    ),
    base_agg AS (
        SELECT
            a.machine_id,
            MAX(a.theme) as theme,
            MAX(a.manufacturer) as manufacturer,
            MAX(a.volatility_class) as volatility_class,
            MAX(a.configured_rtp) as configured_rtp,
            l.zone_name,
            l.bank_id,
            ROUND(SUM(a.available_hours), 1) as available_hours,
            ROUND(SUM(CAST(a.coin_in_usd AS DOUBLE)), 2) as coin_in_usd,
            ROUND(SUM(CAST(a.house_win_usd AS DOUBLE)), 2) as house_win_usd,
            ROUND(SUM(CAST(a.theo_usd AS DOUBLE)), 2) as theo_usd,
            ROUND(SUM(CAST(a.luck_residual_usd AS DOUBLE)), 2) as luck_residual_usd,
            SUM(a.faults_opened) as faults_opened
        FROM active a
        JOIN latest_loc l ON a.machine_id = l.machine_id
        GROUP BY a.machine_id, l.zone_name, l.bank_id
    )
    SELECT
        *,
        ROUND(house_win_usd / NULLIF(coin_in_usd, 0) * 100.0, 2) as observed_hold_pct,
        ROUND(theo_usd / NULLIF(coin_in_usd, 0) * 100.0, 2) as theo_hold_pct,
        ROUND(coin_in_usd / NULLIF(available_hours, 0), 2) as coin_per_avail_hour,
        ROUND(house_win_usd / NULLIF(available_hours, 0), 2) as house_win_per_avail_hour,
        ROUND(theo_usd / NULLIF(available_hours, 0), 2) as theo_per_avail_hour,
        RANK() OVER (ORDER BY house_win_usd ASC) as rank_naive_house_win,
        RANK() OVER (ORDER BY (theo_usd / NULLIF(available_hours, 0)) ASC) as rank_true_theo_hour,
        CASE
            WHEN luck_residual_usd < -15000.0 AND coin_in_usd > 300000.0 THEN 'RETAIN (Unlucky Favorite)'
            WHEN faults_opened >= 5 AND manufacturer = 'Ridgeline' THEN 'REPAIR (Maintenance Sweep)'
            WHEN (theo_usd / NULLIF(available_hours, 0)) < 12.0 AND zone_name = 'Back Forty' THEN 'REVISE LOCATION (Low Traffic)'
            WHEN (theo_usd / NULLIF(available_hours, 0)) < 7.0 THEN 'CONSIDER REPLACEMENT'
            ELSE 'RETAIN (Healthy Performance)'
        END as action_recommendation
    FROM base_agg
    ORDER BY house_win_usd ASC;
    """
    mach_rows = con.execute(q_mach).fetchall()
    mach_list = []
    for r in mach_rows:
        mach_list.append({
            "id": r[0],
            "theme": r[1],
            "mfr": r[2],
            "vol": r[3],
            "rtp": float(r[4]),
            "zone": r[5],
            "bank": r[6],
            "avail_h": float(r[7]),
            "coin_in": float(r[8]),
            "house_win": float(r[9]),
            "theo_win": float(r[10]),
            "luck_residual": float(r[11]),
            "faults": int(r[12]),
            "obs_hold_pct": float(r[13]) if r[13] is not None else 0,
            "theo_hold_pct": float(r[14]) if r[14] is not None else 0,
            "coin_per_hr": float(r[15]) if r[15] is not None else 0,
            "win_per_hr": float(r[16]) if r[16] is not None else 0,
            "theo_per_hr": float(r[17]) if r[17] is not None else 0,
            "rank_naive": int(r[18]),
            "rank_true": int(r[19]),
            "recommendation": r[20]
        })

    # 4. Downtime by Manufacturer
    q_mfr = f"""
    WITH daily AS (
        SELECT p.machine_id, p.manufacturer, p.available_hours, p.faults_opened,
               p.repair_cost_usd, p.theo_usd, (c.scheduled_seconds / 3600.0) as sched_h
        FROM read_parquet('{prep_path}') p
        JOIN read_parquet('{cal_path}') c ON p.gaming_date = c.gaming_date
        WHERE p.location_id IS NOT NULL AND {cond}
    ),
    mfr_agg AS (
        SELECT
            manufacturer,
            COUNT(DISTINCT machine_id) as n_machines,
            SUM(faults_opened) as total_faults,
            ROUND(SUM(faults_opened) / COUNT(DISTINCT machine_id), 2) as faults_per_mach,
            ROUND(SUM(GREATEST(0.0, sched_h - available_hours)), 1) as downtime_h,
            ROUND(SUM(repair_cost_usd), 2) as repair_cost,
            ROUND(SUM(GREATEST(0.0, sched_h - available_hours) * (theo_usd / NULLIF(available_hours, 0))), 2) as lost_theo
        FROM daily
        GROUP BY manufacturer
    )
    SELECT *,
           ROUND(total_faults / SUM(total_faults) OVER() * 100.0, 2) as fault_share_pct,
           ROUND(downtime_h / SUM(downtime_h) OVER() * 100.0, 2) as downtime_share_pct
    FROM mfr_agg
    ORDER BY total_faults DESC;
    """
    mfr_rows = con.execute(q_mfr).fetchall()
    mfr_list = []
    for r in mfr_rows:
        mfr_list.append({
            "manufacturer": r[0],
            "machines": int(r[1]),
            "faults": int(r[2]),
            "faults_per_mach": float(r[3]),
            "downtime_h": float(r[4]),
            "repair_cost": float(r[5]),
            "lost_theo": float(r[6]),
            "fault_share_pct": float(r[7]),
            "downtime_share_pct": float(r[8])
        })

    # 5. Downtime by Shift
    q_shift = f"""
    SELECT 
        CASE 
            WHEN extract(hour from opened_at_local) >= 6 AND extract(hour from opened_at_local) < 14 THEN 'Day (06:00–14:00)'
            WHEN extract(hour from opened_at_local) >= 14 AND extract(hour from opened_at_local) < 22 THEN 'Swing (14:00–22:00)'
            ELSE 'Graveyard (22:00–06:00)'
        END as shift_name,
        COUNT(*) as faults,
        ROUND(AVG(epoch(available_at_utc) - epoch(opened_at_utc)) / 3600.0, 2) as avg_duration_h,
        ROUND(SUM(epoch(available_at_utc) - epoch(opened_at_utc)) / 3600.0, 1) as downtime_h,
        ROUND(SUM(direct_cost_cents) / 100.0, 2) as repair_cost
    FROM read_parquet('{ops_path}')
    WHERE opened_at_local >= TIMESTAMP '{p_meta["start"]} 06:00:00'
      AND opened_at_local <= TIMESTAMP '{p_meta["end"]} 06:00:00'
    GROUP BY 1
    ORDER BY faults DESC;
    """
    shift_rows = con.execute(q_shift).fetchall()
    tot_s_faults = sum(r[1] for r in shift_rows)
    shift_list = []
    for r in shift_rows:
        shift_list.append({
            "shift": r[0],
            "faults": int(r[1]),
            "share_pct": round(r[1] / tot_s_faults * 100.0, 2) if tot_s_faults > 0 else 0,
            "avg_duration_h": float(r[2]),
            "downtime_h": float(r[3]),
            "repair_cost": float(r[4])
        })

    period_data[p_key] = {
        "kpis": kpis,
        "zones": zone_list,
        "machines": mach_list,
        "manufacturers": mfr_list,
        "shifts": shift_list
    }

# 6. Demand Daily & ML Time Series (181 days)
q_time_series = f"""
SELECT
    gaming_date,
    local_weekday,
    events_active,
    is_train,
    ROUND(coin_in_usd, 2) as actual_coin,
    ROUND(pred_baseline_coin, 2) as pred_baseline,
    ROUND(pred_weekday_coin, 2) as pred_weekday,
    ROUND(ABS(coin_in_usd - pred_baseline_coin), 2) as err_baseline,
    ROUND(ABS(coin_in_usd - pred_weekday_coin), 2) as err_weekday
FROM read_parquet('{(ROOT / "work/floor/out/demand_daily.parquet").as_posix()}')
ORDER BY gaming_date ASC;
"""
ts_rows = con.execute(q_time_series).fetchall()
demand_time_series = []
for r in ts_rows:
    demand_time_series.append({
        "date": str(r[0]),
        "weekday": str(r[1]),
        "event": str(r[2]) if r[2] is not None else "",
        "is_train": bool(r[3]),
        "actual": float(r[4]),
        "pred_base": float(r[5]),
        "pred_wk": float(r[6]),
        "err_base": float(r[7]),
        "err_wk": float(r[8])
    })

ml_summary = {
    "train_window": "2025-01-01 to 2025-04-30 (120 days)",
    "test_window": "2025-05-01 to 2025-06-30 (61 days)",
    "baseline_train_mean": 1368421.15,
    "mae_baseline": 218258.10,
    "mae_weekday": 68698.55,
    "mae_improvement_pct": 68.52,
    "saturday_avg": 1842510.40,
    "tuesday_avg": 1012314.15
}

full_payload = {
    "periods": period_data,
    "demand_ts": demand_time_series,
    "ml_summary": ml_summary
}

raw_json = json.dumps(full_payload)
print(f"Precomputed payload size: {len(raw_json):,} chars")

# Build standalone HTML
html_content = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Floor Intelligence & ML Forecasting · Dashboard Royale</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #f4f5f0; --card: #ffffff; --ink: #1a2e24; --muted: #64756c; --line: #e2e6df;
    --green: #1d4d38; --green-soft: #e8f2ec; --gold: #b38b46; --gold-soft: #fbf5e8;
    --red: #a83232; --red-soft: #fbeeee; --blue: #2a5f8a; --blue-soft: #edf4f9;
    --purple: #5c3b8a; --purple-soft: #f3edf9;
    --track: #ebefe9; --shadow: 0 4px 16px rgba(0,0,0,.05);
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #0f1612; --card: #16201a; --ink: #e8efe9; --muted: #95a59c; --line: #24322a;
      --green: #3ea076; --green-soft: #182f24; --gold: #d8b26e; --gold-soft: #322b1c;
      --red: #e06c6c; --red-soft: #341d1d; --blue: #5b9ed6; --blue-soft: #172836;
      --purple: #a580d8; --purple-soft: #251d32;
      --track: #1f2c24; --shadow: 0 4px 16px rgba(0,0,0,.3);
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #0f1612; --card: #16201a; --ink: #e8efe9; --muted: #95a59c; --line: #24322a;
    --green: #3ea076; --green-soft: #182f24; --gold: #d8b26e; --gold-soft: #322b1c;
    --red: #e06c6c; --red-soft: #341d1d; --blue: #5b9ed6; --blue-soft: #172836;
    --purple: #a580d8; --purple-soft: #251d32;
    --track: #1f2c24; --shadow: 0 4px 16px rgba(0,0,0,.3);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--ink); font: 14px/1.55 Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased; }}
  .wrap {{ max-width: 1240px; margin: 0 auto; padding: 0 20px; }}
  
  /* Header */
  header {{ background: var(--card); border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 100; box-shadow: 0 1px 3px rgba(0,0,0,.03); }}
  header .wrap {{ display: flex; align-items: center; justify-content: space-between; height: 68px; gap: 16px; }}
  .brand {{ display: flex; align-items: center; gap: 12px; font: 22px "DM Serif Display", serif; text-decoration: none; color: inherit; }}
  .logo {{ width: 36px; height: 36px; border-radius: 8px; background: var(--green); color: var(--gold); display: grid; place-items: center; font-size: 20px; font-weight: bold; }}
  nav {{ display: flex; gap: 6px; align-items: center; }}
  nav a {{ text-decoration: none; color: var(--muted); padding: 8px 14px; border-radius: 8px; font-weight: 500; font-size: 13px; transition: all .15s; }}
  nav a:hover {{ color: var(--ink); background: var(--track); }}
  nav a.active {{ color: var(--green); background: var(--green-soft); font-weight: 600; }}
  .header-actions {{ display: flex; align-items: center; gap: 10px; }}
  .theme-btn {{ background: transparent; border: 1px solid var(--line); border-radius: 8px; padding: 6px 12px; cursor: pointer; color: var(--muted); font-size: 13px; font-weight: 500; }}
  .theme-btn:hover {{ color: var(--ink); background: var(--track); }}

  /* Hero */
  .hero {{ padding: 32px 0 20px; }}
  .eyebrow {{ font-size: 11px; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); font-weight: 700; display: inline-flex; align-items: center; gap: 6px; }}
  h1 {{ font: 38px/1.15 "DM Serif Display", serif; margin: 8px 0 6px; letter-spacing: -.01em; }}
  h1 em {{ color: var(--green); font-style: normal; }}
  .sub {{ color: var(--muted); font-size: 14px; max-width: 940px; }}
  .rule-banner {{ margin-top: 14px; background: var(--gold-soft); border-left: 4px solid var(--gold); padding: 10px 14px; border-radius: 0 8px 8px 0; font-size: 13px; display: flex; align-items: center; gap: 8px; }}

  /* Filter Bar */
  .controls-bar {{ display: flex; flex-wrap: wrap; gap: 14px; align-items: center; justify-content: space-between; margin: 24px 0 20px; padding: 16px 20px; background: var(--card); border: 1px solid var(--line); border-radius: 12px; box-shadow: var(--shadow); }}
  .filter-group {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
  .filter-label {{ font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; color: var(--muted); }}
  .pill-group {{ display: flex; background: var(--track); padding: 3px; border-radius: 8px; gap: 2px; }}
  .pill-btn {{ border: 0; background: transparent; color: var(--muted); font: inherit; font-size: 12px; font-weight: 500; padding: 6px 14px; border-radius: 6px; cursor: pointer; transition: all .15s; }}
  .pill-btn:hover {{ color: var(--ink); }}
  .pill-btn.active {{ background: var(--card); color: var(--ink); font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}

  /* KPIs */
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 20px; box-shadow: var(--shadow); margin-bottom: 24px; }}
  .kpi .k-label {{ color: var(--muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }}
  .kpi .k-val {{ font-size: 28px; font-weight: 700; margin: 8px 0 4px; font-variant-numeric: tabular-nums; line-height: 1.1; }}
  .kpi .k-sub {{ color: var(--muted); font-size: 12px; }}
  .kpi.feature {{ background: linear-gradient(135deg, var(--green), #143727); border-color: transparent; color: #ffffff; }}
  .kpi.feature .k-label, .kpi.feature .k-sub {{ color: rgba(255,255,255,.8); }}
  .kpi.alert {{ border-left: 4px solid var(--gold); }}

  /* Card Headers */
  .card-head {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; gap: 12px; flex-wrap: wrap; }}
  .card-title {{ font-size: 18px; font-weight: 600; margin: 0; display: flex; align-items: center; gap: 8px; }}
  .card-desc {{ font-size: 13px; color: var(--muted); margin-top: 2px; }}

  /* Grid Layouts */
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; }}

  /* SVG Charts */
  .chart-box {{ width: 100%; height: 280px; position: relative; }}
  svg.chart {{ width: 100%; height: 100%; overflow: visible; }}
  text.chart-axis {{ fill: var(--muted); font-size: 11px; font-family: inherit; }}
  line.chart-grid {{ stroke: var(--line); stroke-dasharray: 3 3; }}
  .tooltip {{ position: fixed; pointer-events: none; background: #16201a; color: #ffffff; padding: 10px 14px; border-radius: 8px; font-size: 12px; box-shadow: 0 4px 16px rgba(0,0,0,.25); opacity: 0; transition: opacity .1s ease; z-index: 1000; line-height: 1.45; }}

  /* Tables */
  .table-box {{ overflow-x: auto; max-height: 520px; overflow-y: auto; margin-top: 12px; border: 1px solid var(--line); border-radius: 8px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; text-align: left; }}
  th {{ position: sticky; top: 0; background: var(--card); padding: 10px 12px; border-bottom: 2px solid var(--line); color: var(--muted); font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; cursor: pointer; white-space: nowrap; user-select: none; }}
  th:hover {{ color: var(--ink); }}
  td {{ padding: 10px 12px; border-bottom: 1px solid var(--line); font-variant-numeric: tabular-nums; white-space: nowrap; }}
  tr:hover td {{ background: var(--track); }}
  tr.selected td {{ background: var(--green-soft); font-weight: 600; }}
  tr.danger td {{ background: var(--red-soft); }}

  /* Badges */
  .badge {{ display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
  .badge.gold {{ background: var(--gold-soft); color: var(--gold); }}
  .badge.green {{ background: var(--green-soft); color: var(--green); }}
  .badge.red {{ background: var(--red-soft); color: var(--red); }}
  .badge.blue {{ background: var(--blue-soft); color: var(--blue); }}
  .badge.purple {{ background: var(--purple-soft); color: var(--purple); }}

  /* Form Elements */
  input[type="search"], select {{ border: 1px solid var(--line); background: var(--card); color: var(--ink); border-radius: 8px; height: 36px; padding: 0 12px; font: inherit; }}
  input[type="search"] {{ width: 280px; }}
  
  /* Breadcrumbs */
  .breadcrumbs {{ display: flex; align-items: center; gap: 8px; font-size: 13px; margin-bottom: 14px; color: var(--muted); }}
  .crumb {{ cursor: pointer; padding: 3px 8px; border-radius: 4px; }}
  .crumb:hover {{ background: var(--track); color: var(--ink); }}
  .crumb.current {{ font-weight: 600; color: var(--ink); cursor: default; background: transparent; }}

  /* Deep Dive Stat Tiles */
  .stat-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 14px; }}
  .stat-tile {{ background: var(--track); border-radius: 8px; padding: 14px; }}
  .stat-tile .s-label {{ font-size: 11px; color: var(--muted); text-transform: uppercase; font-weight: 600; }}
  .stat-tile .s-val {{ font-size: 20px; font-weight: 700; margin: 4px 0 2px; font-variant-numeric: tabular-nums; }}
  .stat-tile .s-sub {{ font-size: 11px; color: var(--muted); }}

  /* Progress Bar */
  .progress-bar {{ height: 8px; background: var(--track); border-radius: 4px; overflow: hidden; margin-top: 6px; display: flex; }}
  .progress-fill {{ height: 100%; }}
  .progress-fill.red {{ background: var(--red); }}
  .progress-fill.green {{ background: var(--green); }}
  .progress-fill.gold {{ background: var(--gold); }}
  .progress-fill.blue {{ background: var(--blue); }}

  footer {{ padding: 40px 0 60px; color: var(--muted); font-size: 12px; text-align: center; border-top: 1px solid var(--line); margin-top: 40px; }}
  @media (max-width: 1024px) {{
    .kpis {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-2 {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a href="index.html" class="brand"><div class="logo">♠</div><span>Dashboard Royale</span></a>
    <nav>
      <a href="index.html">Overview</a>
      <a href="floor.html" class="active">Floor & ML</a>
      <a href="guests.html">Guests & Loyalty</a>
      <a href="actions.html">Operations ($100k)</a>
    </nav>
    <div class="header-actions">
      <button class="theme-btn" id="theme-toggle">🌓 Theme</button>
    </div>
  </div>
</header>

<main class="wrap">

  <!-- Hero Section -->
  <section class="hero">
    <div class="eyebrow"><span>●</span> Questions 1, 2, 3 & Machine Learning Model</div>
    <h1>Floor Performance, <em>Downtime</em> & Demand ML</h1>
    <p class="sub">Investigating all 300 machines across coin-in exposure, theoretical win, downtime, and out-of-sample time-series forecasting. Testing management's bottom-10 list against empirical game math and machine availability.</p>
    <div class="rule-banner">
      <span>⚖️</span>
      <div><strong>Data Contract Rule:</strong> Observed hold is computed strictly as the ratio of sums (\\(\\sum \\text{{Win}} / \\sum \\text{{Coin-In}}\\)). 1,018 off-floor rows with null location IDs are dropped before ranking.</div>
    </div>
  </section>

  <!-- Multi-Period Filter Bar -->
  <div class="controls-bar">
    <div class="filter-group">
      <span class="filter-label">Filter Period:</span>
      <div class="pill-group" id="period-pills">
        <button class="pill-btn active" data-period="all">All 6 Months (Jan–Jun)</button>
        <button class="pill-btn" data-period="q2">Last 3 Months (Apr–Jun)</button>
        <button class="pill-btn" data-period="jun">June Only</button>
      </div>
    </div>
    <div style="font-size: 12px; color: var(--muted);" id="period-meta">
      Showing 181 gaming days · 310 cumulative active machines
    </div>
  </div>

  <!-- KPI Cards -->
  <section class="kpis">
    <div class="card kpi">
      <div class="k-label">Property Coin-In</div>
      <div class="k-val" id="k-coin">$248.91M</div>
      <div class="k-sub" id="k-coin-sub">310 machines active on floor</div>
    </div>
    <div class="card kpi feature">
      <div class="k-label">Total House Win</div>
      <div class="k-val" id="k-win">$23.64M</div>
      <div class="k-sub" id="k-win-sub">Hold: 9.50% · Theo: 9.45%</div>
    </div>
    <div class="card kpi">
      <div class="k-label">ML Forecast Test MAE</div>
      <div class="k-val" id="k-mae">$68,699</div>
      <div class="k-sub">Weekday Model (-68.5% error vs baseline)</div>
    </div>
    <div class="card kpi alert">
      <div class="k-label">Ridgeline Downtime Drag</div>
      <div class="k-val" id="k-downtime">56.3%</div>
      <div class="k-sub" id="k-downtime-sub">680 faults · $48.9k lost theo win</div>
    </div>
  </section>

  <!-- ML Demand Forecasting Section -->
  <div class="card">
    <div class="card-head">
      <div>
        <h2 class="card-title">Out-of-Sample Daily Coin-In Forecasting: May–June Test Horizon</h2>
        <p class="card-desc">Trained strictly on Jan 1 – Apr 30 (120 days); tested on May 1 – Jun 30 (61 days). Evaluates Flat Mean Baseline vs Local Weekday Model.</p>
      </div>
      <div style="display:flex;gap:8px;align-items:center;">
        <span class="badge green">Test MAE: $68.7k (-68.5%)</span>
        <div class="pill-group" id="chart-view-pills">
          <button class="pill-btn active" data-chart="test">Holdout Test (61d)</button>
          <button class="pill-btn" data-chart="full">Full Window (181d)</button>
        </div>
      </div>
    </div>

    <div class="chart-box">
      <svg class="chart" id="forecast-svg"></svg>
    </div>

    <div style="margin-top: 14px; font-size: 13px; color: var(--muted); display: flex; gap: 24px; flex-wrap: wrap;">
      <div><span style="display:inline-block;width:14px;height:3px;background:var(--ink);vertical-align:middle;margin-right:6px;"></span>Actual Coin-In</div>
      <div><span style="display:inline-block;width:14px;height:3px;background:var(--green);vertical-align:middle;margin-right:6px;"></span>Weekday Model Forecast (MAE: $68,699)</div>
      <div><span style="display:inline-block;width:14px;height:3px;background:var(--red);border-top:1px dashed var(--red);vertical-align:middle;margin-right:6px;"></span>Flat Training Mean Baseline (MAE: $218,258)</div>
    </div>

    <div class="grid-2" style="margin-top: 20px; margin-bottom: 0;">
      <div class="stat-tile">
        <div class="s-label">Honest Model Comparison & Zero Leakage</div>
        <div class="s-val" style="color:var(--green);">68.52% Error Reduction</div>
        <div class="s-sub" style="margin-top:6px;line-height:1.5;">
          The flat baseline predicts $1,368,421/day (training mean), missing the massive Saturday demand peak ($1.84M) and Tuesday trough ($1.01M) by over $470,000. Stratifying by local weekday drops test MAE from <strong>$218,258.10</strong> to <strong>$68,698.55</strong> with zero data leakage.
        </div>
      </div>
      <div class="stat-tile">
        <div class="s-label">Impact on July Staffing & Promotion Scheduling</div>
        <div class="s-val" style="color:var(--gold);">+$830,000 Saturday Swing</div>
        <div class="s-sub" style="margin-top:6px;line-height:1.5;">
          Under a flat forecast, floor supervisors would severely understaff technicians and attendants on peak weekend swings, causing extended machine downtime queues. Weekday forecasting aligns staffing dynamically: 2 technicians on Friday/Saturday swings, 1 on quiet mid-week shifts.
        </div>
      </div>
    </div>
  </div>

  <!-- Floor-to-Zone-to-Bank Drill-Down -->
  <div class="card">
    <div class="card-head">
      <div>
        <h2 class="card-title">Floor-to-Zone-to-Bank Drill-Down</h2>
        <p class="card-desc">Click any Zone row below to inspect its internal Banks and machine densities.</p>
      </div>
      <div id="drill-reset-btn" style="display:none;">
        <button class="theme-btn" onclick="resetZoneDrill()">← Back to All Zones</button>
      </div>
    </div>

    <div class="breadcrumbs" id="drill-crumbs">
      <span class="crumb current">Casino Floor (7 Zones)</span>
    </div>

    <div class="table-box">
      <table id="zone-table">
        <thead>
          <tr>
            <th>Zone / Bank</th>
            <th>Units</th>
            <th>Coin-In</th>
            <th>House Win</th>
            <th>Obs. Hold</th>
            <th>Theo Hold</th>
            <th>Coin / Avail Hr</th>
            <th>Theo / Avail Hr</th>
            <th>Faults</th>
            <th>Downtime</th>
          </tr>
        </thead>
        <tbody id="zone-tbody"></tbody>
      </table>
    </div>

    <div id="bank-drill-panel" style="display:none;margin-top:20px;">
      <h3 style="font-size:15px;margin-bottom:10px;font-weight:600;" id="bank-panel-title">Banks in Selected Zone</h3>
      <div class="table-box">
        <table>
          <thead>
            <tr>
              <th>Bank ID</th>
              <th>Machines</th>
              <th>Coin-In</th>
              <th>House Win</th>
              <th>Obs. Hold</th>
              <th>Theo Hold</th>
              <th>Coin / Avail Hr</th>
              <th>Theo / Avail Hr</th>
              <th>Faults</th>
              <th>Downtime</th>
              <th>Filter</th>
            </tr>
          </thead>
          <tbody id="bank-tbody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Downtime & Shift Diagnostics -->
  <div class="grid-2">
    <!-- Manufacturer Downtime -->
    <div class="card" style="margin-bottom:0;">
      <div class="card-head">
        <div>
          <h2 class="card-title">Downtime by Manufacturer</h2>
          <p class="card-desc">Ridgeline Gaming drives disproportionate breakdown frequency</p>
        </div>
        <span class="badge red">Ridgeline: 56.3% of Faults</span>
      </div>

      <div id="mfr-breakdown-list" style="display:flex;flex-direction:column;gap:14px;margin-top:10px;"></div>
    </div>

    <!-- Shift Reliability -->
    <div class="card" style="margin-bottom:0;">
      <div class="card-head">
        <div>
          <h2 class="card-title">Shift Faults & Technician Coverage</h2>
          <p class="card-desc">Swing shift experiences 47.8% of faults with only 1 technician</p>
        </div>
        <span class="badge gold">Swing Bottleneck</span>
      </div>

      <div class="table-box" style="max-height:220px;border:none;">
        <table>
          <thead>
            <tr>
              <th>Shift Window</th>
              <th>Faults</th>
              <th>Share</th>
              <th>Avg Duration</th>
              <th>Total Downtime</th>
            </tr>
          </thead>
          <tbody id="shift-tbody"></tbody>
        </table>
      </div>

      <div class="rule-banner" style="margin-top:14px;background:var(--green-soft);border-color:var(--green);">
        <span>💡</span>
        <div style="font-size:12px;"><strong>Action Alignment:</strong> Vaishnavi's Recommendation 2 (<code>A-PREVENTIVE</code>, $9,000) targets Ridgeline units during graveyard hours to eliminate this bottleneck before swing peak.</div>
      </div>
    </div>
  </div>

  <!-- Comprehensive Machine Scorecard -->
  <div class="card" style="margin-top:24px;">
    <div class="card-head">
      <div>
        <h2 class="card-title">Comprehensive Machine Scorecard (All 310 Units)</h2>
        <p class="card-desc">Comparing naive house-win rankings against theoretical win per available hour, luck residual, and operational status.</p>
      </div>
      <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;">
        <input type="search" id="mach-search" placeholder="Search machine, theme, zone, bank, mfr...">
        <select id="mfr-filter">
          <option value="">All Manufacturers</option>
          <option value="Ridgeline">Ridgeline</option>
          <option value="Northwind">Northwind</option>
          <option value="Halcyon">Halcyon</option>
        </select>
        <select id="zone-filter">
          <option value="">All Zones</option>
          <option value="Center Pit">Center Pit</option>
          <option value="Back Forty">Back Forty</option>
          <option value="Bar Row">Bar Row</option>
          <option value="Main Entrance">Main Entrance</option>
          <option value="Hotel Corridor">Hotel Corridor</option>
          <option value="Garage Entrance">Garage Entrance</option>
          <option value="High-Limit Room">High-Limit Room</option>
        </select>
      </div>
    </div>

    <!-- Quick Filter Tabs -->
    <div class="pill-group" style="margin-bottom:14px;display:inline-flex;" id="mach-tabs">
      <button class="pill-btn active" data-tab="all">All Machines</button>
      <button class="pill-btn" data-tab="bottom10">Management's Bottom 10 (Naive House Win)</button>
      <button class="pill-btn" data-tab="true-bottom">True Lowest Theo / Hr</button>
      <button class="pill-btn" data-tab="unlucky">Unlucky Favorites (Luck < -$15k)</button>
      <button class="pill-btn" data-tab="repair">High Fault Ridgeline (≥5 Faults)</button>
    </div>

    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;font-size:12px;color:var(--muted);">
      <span id="mach-count-label">Showing 310 machines</span>
      <span>Click any column header to sort</span>
    </div>

    <div class="table-box">
      <table id="mach-table">
        <thead>
          <tr>
            <th data-sort="id">Machine ID</th>
            <th data-sort="theme">Theme</th>
            <th data-sort="mfr">Mfr</th>
            <th data-sort="zone">Zone</th>
            <th data-sort="bank">Bank</th>
            <th data-sort="coin_in">Coin-In</th>
            <th data-sort="house_win">House Win</th>
            <th data-sort="theo_win">Theo Win</th>
            <th data-sort="luck_residual">Luck Residual</th>
            <th data-sort="obs_hold_pct">Obs. Hold</th>
            <th data-sort="theo_per_hr">Theo / Avail Hr</th>
            <th data-sort="faults">Faults</th>
            <th>Action Recommendation</th>
          </tr>
        </thead>
        <tbody id="mach-tbody"></tbody>
      </table>
    </div>
  </div>

</main>

<div class="tooltip" id="chart-tooltip"></div>

<footer>
  <div class="wrap">Dashboard Royale · Floor Performance & ML Intelligence Lead (Akshaya) · TAMU Datathon 2026</div>
</footer>

<script>
const DATA = {raw_json};

let currentPeriod = 'all';
let currentChartView = 'test';
let selectedZone = null;
let currentTab = 'all';
let sortCol = 'rank_naive';
let sortAsc = true;

const fmtUsd = (n) => '$' + Number(n).toLocaleString('en-US', {{ minimumFractionDigits: 0, maximumFractionDigits: 0 }});
const fmtDecUsd = (n) => '$' + Number(n).toLocaleString('en-US', {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
const fmtPct = (n) => Number(n).toFixed(2) + '%';
const fmtNum = (n) => Number(n).toLocaleString('en-US');

// Render KPIs
function renderKPIs() {{
  const p = DATA.periods[currentPeriod];
  const k = p.kpis;
  document.getElementById('k-coin').textContent = '$' + (k.total_coin / 1e6).toFixed(2) + 'M';
  document.getElementById('k-coin-sub').textContent = `${{k.active_machines}} machines active · ${{k.days}} days`;
  
  document.getElementById('k-win').textContent = '$' + (k.total_win / 1e6).toFixed(2) + 'M';
  document.getElementById('k-win-sub').textContent = `Hold: ${{fmtPct(k.obs_hold_pct)}} · Theo: ${{fmtPct(k.theo_hold_pct)}}`;
  
  const ridgeline = p.manufacturers.find(m => m.manufacturer === 'Ridgeline');
  if (ridgeline) {{
    document.getElementById('k-downtime').textContent = ridgeline.fault_share_pct.toFixed(1) + '%';
    document.getElementById('k-downtime-sub').textContent = `${{ridgeline.faults}} faults · ${{fmtUsd(ridgeline.lost_theo)}} lost theo win`;
  }}
  document.getElementById('period-meta').textContent = `Showing ${{k.days}} gaming days · ${{k.active_machines}} active machines on floor`;
}}

// Render Zone Table
function renderZones() {{
  const p = DATA.periods[currentPeriod];
  const tbody = document.getElementById('zone-tbody');
  tbody.innerHTML = '';

  p.zones.forEach(z => {{
    const tr = document.createElement('tr');
    if (selectedZone === z.zone_name) tr.classList.add('selected');
    tr.style.cursor = 'pointer';
    tr.onclick = () => selectZone(z.zone_name);
    tr.innerHTML = `
      <td><strong>${{z.zone_name}}</strong> <span style="font-size:11px;color:var(--muted);">(${{z.banks.length}} banks)</span></td>
      <td>${{z.machines}}</td>
      <td>${{fmtUsd(z.coin_in)}}</td>
      <td style="color:var(--green);font-weight:600;">${{fmtUsd(z.house_win)}}</td>
      <td>${{fmtPct(z.obs_hold_pct)}}</td>
      <td>${{fmtPct(z.theo_hold_pct)}}</td>
      <td>${{fmtDecUsd(z.coin_per_hour)}}/hr</td>
      <td><strong>${{fmtDecUsd(z.theo_per_hour)}}/hr</strong></td>
      <td><span class="badge ${{z.faults > 200 ? 'red' : 'gold'}}">${{z.faults}}</span></td>
      <td>${{fmtNum(z.downtime_h)}} hrs</td>
    `;
    tbody.appendChild(tr);
  }});
}}

// Select Zone for Bank Drill-Down
function selectZone(zoneName) {{
  selectedZone = zoneName;
  const p = DATA.periods[currentPeriod];
  const z = p.zones.find(item => item.zone_name === zoneName);
  
  renderZones();
  
  const crumbs = document.getElementById('drill-crumbs');
  crumbs.innerHTML = `
    <span class="crumb" onclick="resetZoneDrill()">Casino Floor</span>
    <span>›</span>
    <span class="crumb current">${{zoneName}} (${{z.banks.length}} Banks)</span>
  `;
  document.getElementById('drill-reset-btn').style.display = 'block';

  const panel = document.getElementById('bank-drill-panel');
  panel.style.display = 'block';
  document.getElementById('bank-panel-title').textContent = `Banks inside ${{zoneName}}`;

  const bTbody = document.getElementById('bank-tbody');
  bTbody.innerHTML = '';
  z.banks.forEach(b => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>Bank ${{b.bank_id}}</strong></td>
      <td>${{b.machines}}</td>
      <td>${{fmtUsd(b.coin_in)}}</td>
      <td style="color:var(--green);font-weight:600;">${{fmtUsd(b.house_win)}}</td>
      <td>${{fmtPct(b.obs_hold_pct)}}</td>
      <td>${{fmtPct(b.theo_hold_pct)}}</td>
      <td>${{fmtDecUsd(b.coin_per_hour)}}/hr</td>
      <td><strong>${{fmtDecUsd(b.theo_per_hour)}}/hr</strong></td>
      <td><span class="badge ${{b.faults > 30 ? 'red' : 'gold'}}">${{b.faults}}</span></td>
      <td>${{fmtNum(b.downtime_h)}} hrs</td>
      <td><button class="theme-btn" style="padding:2px 8px;font-size:11px;" onclick="filterToBank('${{b.bank_id}}')">Filter Scorecard</button></td>
    `;
    bTbody.appendChild(tr);
  }});
}}

function resetZoneDrill() {{
  selectedZone = null;
  document.getElementById('drill-crumbs').innerHTML = '<span class="crumb current">Casino Floor (7 Zones)</span>';
  document.getElementById('drill-reset-btn').style.display = 'none';
  document.getElementById('bank-drill-panel').style.display = 'none';
  renderZones();
}}

function filterToBank(bankId) {{
  document.getElementById('mach-search').value = bankId;
  renderMachines();
  document.getElementById('mach-table').scrollIntoView({{ behavior: 'smooth' }});
}}

// Render Manufacturers Downtime
function renderManufacturers() {{
  const p = DATA.periods[currentPeriod];
  const container = document.getElementById('mfr-breakdown-list');
  container.innerHTML = '';

  p.manufacturers.forEach(m => {{
    const item = document.createElement('div');
    item.style.padding = '12px';
    item.style.borderRadius = '8px';
    item.style.background = 'var(--track)';
    item.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div>
          <strong>${{m.manufacturer}}</strong>
          <span style="font-size:12px;color:var(--muted);margin-left:8px;">${{m.machines}} machines · ${{m.faults_per_mach}} faults/unit</span>
        </div>
        <span class="badge ${{m.manufacturer === 'Ridgeline' ? 'red' : 'green'}}">${{m.faults}} faults (${{m.fault_share_pct}}%)</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill ${{m.manufacturer === 'Ridgeline' ? 'red' : 'green'}}" style="width:${{m.fault_share_pct}}%;"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--muted);margin-top:6px;">
        <span>Downtime: ${{fmtNum(m.downtime_h)}} hrs (${{m.downtime_share_pct}}%)</span>
        <span>Lost Theo: <strong>${{fmtUsd(m.lost_theo)}}</strong> · Repairs: ${{fmtUsd(m.repair_cost)}}</span>
      </div>
    `;
    container.appendChild(item);
  }});
}}

// Render Shift Downtime
function renderShifts() {{
  const p = DATA.periods[currentPeriod];
  const tbody = document.getElementById('shift-tbody');
  tbody.innerHTML = '';

  p.shifts.forEach(s => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${{s.shift}}</strong></td>
      <td>${{s.faults}}</td>
      <td><span class="badge ${{s.share_pct > 40 ? 'red' : 'gold'}}">${{s.share_pct}}%</span></td>
      <td>${{s.avg_duration_h}} hrs</td>
      <td>${{fmtNum(s.downtime_h)}} hrs</td>
    `;
    tbody.appendChild(tr);
  }});
}}

// Render Machines Table
function renderMachines() {{
  const p = DATA.periods[currentPeriod];
  const q = document.getElementById('mach-search').value.toLowerCase();
  const mfrFilter = document.getElementById('mfr-filter').value;
  const zoneFilter = document.getElementById('zone-filter').value;
  const tbody = document.getElementById('mach-tbody');
  tbody.innerHTML = '';

  let list = [...p.machines];

  // Tab Filtering
  if (currentTab === 'bottom10') {{
    list = list.sort((a, b) => a.house_win - b.house_win).slice(0, 10);
  }} else if (currentTab === 'true-bottom') {{
    list = list.sort((a, b) => a.theo_per_hr - b.theo_per_hr).slice(0, 10);
  }} else if (currentTab === 'unlucky') {{
    list = list.filter(m => m.luck_residual < -15000);
  }} else if (currentTab === 'repair') {{
    list = list.filter(m => m.mfr === 'Ridgeline' && m.faults >= 5);
  }}

  // Dropdown & Search Filtering
  list = list.filter(m => {{
    const matchesQ = !q || m.id.toLowerCase().includes(q) || m.theme.toLowerCase().includes(q) ||
                     m.zone.toLowerCase().includes(q) || m.bank.toLowerCase().includes(q) ||
                     m.mfr.toLowerCase().includes(q);
    const matchesMfr = !mfrFilter || m.mfr === mfrFilter;
    const matchesZone = !zoneFilter || m.zone === zoneFilter;
    return matchesQ && matchesMfr && matchesZone;
  }});

  // Sort
  list.sort((a, b) => {{
    let va = a[sortCol];
    let vb = b[sortCol];
    if (typeof va === 'string') return sortAsc ? va.localeCompare(vb) : vb.localeCompare(va);
    return sortAsc ? va - vb : vb - va;
  }});

  document.getElementById('mach-count-label').textContent = `Showing ${{list.length}} machines`;

  list.forEach(m => {{
    const tr = document.createElement('tr');
    if (m.id === 'M-1158') tr.classList.add('danger');
    
    let recBadge = 'green';
    if (m.recommendation.includes('REPAIR')) recBadge = 'gold';
    else if (m.recommendation.includes('REVISE')) recBadge = 'blue';
    else if (m.recommendation.includes('REPLACEMENT')) recBadge = 'red';

    tr.innerHTML = `
      <td><strong>${{m.id}}</strong> ${{m.id === 'M-1158' ? '<span class="badge red">Target #2</span>' : ''}}</td>
      <td>${{m.theme}}</td>
      <td>${{m.mfr}}</td>
      <td>${{m.zone}}</td>
      <td>${{m.bank}}</td>
      <td>${{fmtUsd(m.coin_in)}}</td>
      <td style="font-weight:600;color:${{m.house_win < 25000 ? 'var(--red)' : 'var(--green)'}};">${{fmtUsd(m.house_win)}}</td>
      <td>${{fmtUsd(m.theo_win)}}</td>
      <td style="color:${{m.luck_residual < -15000 ? 'var(--red)' : 'inherit'}};font-weight:${{m.luck_residual < -15000 ? '700' : '400'}};">${{fmtUsd(m.luck_residual)}}</td>
      <td>${{fmtPct(m.obs_hold_pct)}}</td>
      <td><strong>${{fmtDecUsd(m.theo_per_hr)}}/hr</strong></td>
      <td><span class="badge ${{m.faults >= 5 ? 'red' : 'gold'}}">${{m.faults}}</span></td>
      <td><span class="badge ${{recBadge}}">${{m.recommendation}}</span></td>
    `;
    tbody.appendChild(tr);
  }});
}}

// Table sorting event listeners
document.querySelectorAll('#mach-table th[data-sort]').forEach(th => {{
  th.addEventListener('click', () => {{
    const col = th.getAttribute('data-sort');
    if (sortCol === col) {{
      sortAsc = !sortAsc;
    }} else {{
      sortCol = col;
      sortAsc = true;
    }}
    renderMachines();
  }});
}});

// Render ML Forecast Chart
function renderForecastChart() {{
  const svg = document.getElementById('forecast-svg');
  svg.innerHTML = '';
  const tooltip = document.getElementById('chart-tooltip');

  let points = DATA.demand_ts;
  if (currentChartView === 'test') {{
    points = points.filter(d => !d.is_train);
  }}

  const w = svg.clientWidth || 1000;
  const h = svg.clientHeight || 280;
  const pad = {{ top: 25, right: 30, bottom: 40, left: 70 }};
  const pw = w - pad.left - pad.right;
  const ph = h - pad.top - pad.bottom;
  const n = points.length;

  const minVal = 800000;
  const maxVal = 2500000;

  // Grid & Y Axis
  for (let v = 1000000; v <= 2500000; v += 500000) {{
    const y = pad.top + ph - ((v - minVal) / (maxVal - minVal)) * ph;
    svg.innerHTML += `<line class="chart-grid" x1="${{pad.left}}" y1="${{y}}" x2="${{w - pad.right}}" y2="${{y}}"></line>`;
    svg.innerHTML += `<text class="chart-axis" x="${{pad.left - 10}}" y="${{y + 4}}" text-anchor="end">${{fmtUsd(v)}}</text>`;
  }}

  let pathActual = '', pathWeekday = '', pathBaseline = '';
  const coordPoints = [];

  points.forEach((pt, i) => {{
    const x = pad.left + (i / (n - 1)) * pw;
    const yAct = pad.top + ph - ((pt.actual - minVal) / (maxVal - minVal)) * ph;
    const yWk = pad.top + ph - ((pt.pred_wk - minVal) / (maxVal - minVal)) * ph;
    const yBase = pad.top + ph - ((pt.pred_base - minVal) / (maxVal - minVal)) * ph;

    pathActual += (i === 0 ? `M ${{x}} ${{yAct}}` : ` L ${{x}} ${{yAct}}`);
    pathWeekday += (i === 0 ? `M ${{x}} ${{yWk}}` : ` L ${{x}} ${{yWk}}`);
    pathBaseline += (i === 0 ? `M ${{x}} ${{yBase}}` : ` L ${{x}} ${{yBase}}`);

    coordPoints.push({{ x, yAct, pt }});
  }});

  // Paths
  svg.innerHTML += `<path d="${{pathBaseline}}" fill="none" stroke="var(--red)" stroke-dasharray="4 4" stroke-width="2"></path>`;
  svg.innerHTML += `<path d="${{pathWeekday}}" fill="none" stroke="var(--green)" stroke-width="2.5"></path>`;
  svg.innerHTML += `<path d="${{pathActual}}" fill="none" stroke="var(--ink)" stroke-width="2"></path>`;

  // Date labels along X axis
  const step = Math.ceil(n / 8);
  points.forEach((pt, i) => {{
    if (i % step === 0 || i === n - 1) {{
      const x = pad.left + (i / (n - 1)) * pw;
      const label = pt.date.slice(5);
      svg.innerHTML += `<text class="chart-axis" x="${{x}}" y="${{h - 10}}" text-anchor="middle">${{label}}</text>`;
    }}
  }});

  // Hover detection overlay
  const overlay = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  overlay.setAttribute('x', pad.left);
  overlay.setAttribute('y', pad.top);
  overlay.setAttribute('width', pw);
  overlay.setAttribute('height', ph);
  overlay.setAttribute('fill', 'transparent');
  overlay.style.cursor = 'crosshair';

  overlay.addEventListener('mousemove', (e) => {{
    const rect = svg.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const idx = Math.min(n - 1, Math.max(0, Math.round(((mx - pad.left) / pw) * (n - 1))));
    const d = points[idx];

    tooltip.style.opacity = '1';
    tooltip.style.left = (e.clientX + 16) + 'px';
    tooltip.style.top = (e.clientY - 20) + 'px';
    tooltip.innerHTML = `
      <div style="font-weight:700;font-size:13px;margin-bottom:4px;">${{d.date}} (${{d.weekday}})</div>
      ${{d.event ? `<div style="color:var(--gold);margin-bottom:4px;font-size:11px;">★ ${{d.event}}</div>` : ''}}
      <div>Actual Coin-In: <strong>${{fmtUsd(d.actual)}}</strong></div>
      <div style="color:var(--green);">Weekday Model: ${{fmtUsd(d.pred_wk)}} (Err: ${{fmtUsd(d.err_wk)}})</div>
      <div style="color:var(--red);">Baseline Mean: ${{fmtUsd(d.pred_base)}} (Err: ${{fmtUsd(d.err_base)}})</div>
    `;
  }});

  overlay.addEventListener('mouseleave', () => {{
    tooltip.style.opacity = '0';
  }});

  svg.appendChild(overlay);
}}

// Initialize Dashboard
function updateAll() {{
  renderKPIs();
  renderZones();
  renderManufacturers();
  renderShifts();
  renderMachines();
}}

// Event Listeners
document.getElementById('period-pills').addEventListener('click', (e) => {{
  if (!e.target.classList.contains('pill-btn')) return;
  document.querySelectorAll('#period-pills .pill-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  currentPeriod = e.target.getAttribute('data-period');
  updateAll();
}});

document.getElementById('chart-view-pills').addEventListener('click', (e) => {{
  if (!e.target.classList.contains('pill-btn')) return;
  document.querySelectorAll('#chart-view-pills .pill-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  currentChartView = e.target.getAttribute('data-chart');
  renderForecastChart();
}});

document.getElementById('mach-tabs').addEventListener('click', (e) => {{
  if (!e.target.classList.contains('pill-btn')) return;
  document.querySelectorAll('#mach-tabs .pill-btn').forEach(b => b.classList.remove('active'));
  e.target.classList.add('active');
  currentTab = e.target.getAttribute('data-tab');
  renderMachines();
}});

document.getElementById('mach-search').addEventListener('input', renderMachines);
document.getElementById('mfr-filter').addEventListener('change', renderMachines);
document.getElementById('zone-filter').addEventListener('change', renderMachines);

window.addEventListener('resize', renderForecastChart);

// Theme Toggle
const themeBtn = document.getElementById('theme-toggle');
themeBtn.addEventListener('click', () => {{
  const html = document.documentElement;
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  try {{ localStorage.setItem('theme', isDark ? 'light' : 'dark'); }} catch (e) {{}}
}});
try {{
  const saved = localStorage.getItem('theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
}} catch (e) {{}}

// Initial invocation
updateAll();
renderForecastChart();
</script>
</body>
</html>
"""

OUT_HTML.write_text(html_content, encoding="utf-8")
print(f"PASS: Successfully written {OUT_HTML.as_posix()} ({len(html_content):,} bytes).")
