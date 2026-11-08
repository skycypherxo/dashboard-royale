"""
Generate floor_overview.html & floor.html for Akshaya (Floor & ML Lead)
TAMU Datathon 2026 - THE GILDED ACE Casino Decision Intelligence Platform
Aligned with TEAM.md Multi-Page Decision Platform specifications.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_decision_platform import build_floor_overview

if __name__ == "__main__":
    print("♠ Generating unified Floor Overview for THE GILDED ACE (Akshaya - Floor & ML Lead)...")
    build_floor_overview()
    print("PASS: Successfully generated dashboard/floor_overview.html and dashboard/floor.html with full 7-zone matrix and 51-bank drill-down!")
