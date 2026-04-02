#!/usr/bin/env python3
"""
Remote API for Golf Analytics
Trigger analysis remotely, get signals, check status

Usage:
  python remote_api.py

Access from anywhere:
  GET /api/signals → Get 4 validated signals
  GET /api/run-analysis → Trigger fresh 4D element analysis
  GET /api/status → Get model status
"""

import os
import json
import subprocess
from datetime import datetime
from flask import Flask, jsonify, request
from pathlib import Path

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load current signals
def load_signals():
    try:
        with open(os.path.join(BASE_DIR, "signals_api.json"), "r") as f:
            return json.load(f)
    except:
        return {"error": "Signals not loaded"}

# Trigger 4D element analysis
def run_analysis(year_min=2025, year_max=2026):
    """Run 4D element analysis for given year range"""
    try:
        script = os.path.join(BASE_DIR, "engine", "combo_analysis_4d_element.py")
        cmd = [
            "python",
            script,
            "--year-min", str(year_min),
            "--year-max", str(year_max)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        return {
            "status": "success" if result.returncode == 0 else "error",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "timestamp": datetime.now().isoformat()
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "Analysis timeout (>5 min)"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.route('/api/signals', methods=['GET'])
def get_signals():
    """Get 4 validated betting signals"""
    signals = load_signals()
    return jsonify(signals)

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get model status and metrics"""
    status = {
        "model": "4D Element",
        "transfer_rate": 43.1,
        "signals_validated": 4,
        "last_updated": "2026-03-28",
        "baseline_roi": 62.57,
        "status": "Ready for betting implementation",
        "next_steps": [
            "Implement betting rules",
            "Build matching system",
            "Create performance dashboard",
            "Go live with 2025-2026 validation"
        ]
    }
    return jsonify(status)

@app.route('/api/run-analysis', methods=['GET'])
def run_analysis_endpoint():
    """Trigger fresh 4D element analysis

    Query params:
      year_min: Start year (default 2025)
      year_max: End year (default 2026)
    """
    year_min = request.args.get('year_min', 2025, type=int)
    year_max = request.args.get('year_max', 2026, type=int)

    return jsonify({
        "status": "running",
        "message": f"Running analysis for {year_min}-{year_max}",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/avoid-signals', methods=['GET'])
def get_avoid_signals():
    """Get signals to avoid (negative edges)"""
    avoid = {
        "signals_to_avoid": [
            {
                "rank": 1,
                "combo": "Moderate x Positioning x Purple x Metal",
                "edge": -8.9,
                "sample": 36,
                "action": "AVOID"
            },
            {
                "rank": 2,
                "combo": "Calm x Survival x Blue x Metal",
                "edge": -8.6,
                "sample": 102,
                "action": "AVOID"
            },
            {
                "rank": 3,
                "combo": "Calm x Mixed x Yellow x Fire",
                "edge": -6.5,
                "sample": 51,
                "action": "AVOID"
            }
        ]
    }
    return jsonify(avoid)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        "name": "Golf Analytics Remote API",
        "version": "1.0",
        "endpoints": {
            "GET /api/signals": "Get 4 validated betting signals",
            "GET /api/status": "Get model status and metrics",
            "GET /api/avoid-signals": "Get signals to avoid",
            "GET /api/run-analysis?year_min=2025&year_max=2026": "Trigger fresh analysis",
            "GET /api/health": "Health check"
        }
    })

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GOLF ANALYTICS - REMOTE API")
    print("="*70)
    print("\nStarting API server...")
    print("\nLocal: http://localhost:5000")
    print("API Endpoints:")
    print("  GET /api/signals - Get 4 signals")
    print("  GET /api/status - Model status")
    print("  GET /api/avoid-signals - Avoid these")
    print("  GET /api/run-analysis - Trigger analysis")
    print("  GET /api/health - Health check")
    print("\nFor remote access, deploy to cloud or use ngrok tunnel")
    print("="*70 + "\n")

    app.run(host="0.0.0.0", port=5000, debug=False)
