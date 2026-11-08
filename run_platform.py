"""
Launch THE GILDED ACE Casino Decision Intelligence Platform.
Starts the FastAPI analytical backend and launches the multi-page platform in your browser.
"""
import sys
import os
import webbrowser
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "127.0.0.1")
    url = f"http://{host}:{port}/dashboard/index.html"
    
    print("=" * 70)
    print("♠ THE GILDED ACE · CASINO DECISION INTELLIGENCE PLATFORM")
    print("=" * 70)
    print(f"Backend API:   http://{host}:{port}/docs")
    print(f"Dashboard UI:  {url}")
    print("\n8 Structured Pages Available:")
    print("  1. Floor Overview       -> /dashboard/floor_overview.html")
    print("  2. Machine Intelligence -> /dashboard/machine_intelligence.html")
    print("  3. Demand Analytics     -> /dashboard/demand_analytics.html")
    print("  4. Operations           -> /dashboard/operations.html")
    print("  5. Guest Intelligence   -> /dashboard/guest_intelligence.html")
    print("  6. Budget Optimizer     -> /dashboard/budget_optimizer.html")
    print("  7. Gemini Copilot       -> /dashboard/gemini_copilot.html")
    print("  8. Evidence Explorer    -> /dashboard/evidence_explorer.html")
    print("=" * 70)
    print("Opening browser...")
    webbrowser.open(url)
    
    try:
        uvicorn.run("backend.main:app", host=host, port=port, log_level="info", reload=False)
    except KeyboardInterrupt:
        print("\nShutting down platform.")

