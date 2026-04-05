#!/usr/bin/env python3
"""
Mobile Dashboard Server for Golf Analytics
Access from Android phone at: http://[YOUR_PC_IP]:8000

Usage:
  python3 mobile_server.py

Then on Android phone:
  Open browser → http://192.168.x.x:8000/
  (Replace 192.168.x.x with your PC's local IP)
"""

import os
import json
import http.server
import socketserver
import webbrowser
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8000

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve dashboard
        if self.path == '/' or self.path == '/dashboard':
            self.path = '/dashboard.html'

        # API endpoints
        elif self.path == '/api/signals':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            signals = {
                "transfer_rate": 43.1,
                "signals": [
                    {
                        "rank": 1,
                        "name": "Calm x Mixed x Yellow x Earth",
                        "edge": 15.5,
                        "sample": 44,
                        "ratio": 2.81,
                        "confidence": "HIGH",
                        "bet": "LARGE"
                    },
                    {
                        "rank": 2,
                        "name": "Calm x REMOVE x Purple x Water",
                        "edge": 13.4,
                        "sample": 30,
                        "ratio": 1.46,
                        "confidence": "HIGH",
                        "bet": "LARGE"
                    },
                    {
                        "rank": 3,
                        "name": "Calm x Positioning x Green x Metal",
                        "edge": 11.3,
                        "sample": 58,
                        "ratio": 1.98,
                        "confidence": "MEDIUM-HIGH",
                        "bet": "MEDIUM"
                    },
                    {
                        "rank": 4,
                        "name": "Calm x Closing x Blue x Fire",
                        "edge": 8.1,
                        "sample": 102,
                        "ratio": 1.14,
                        "confidence": "MEDIUM",
                        "bet": "SMALL"
                    }
                ]
            }

            self.wfile.write(json.dumps(signals, indent=2).encode())
            return

        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            status = {
                "model": "4D Element",
                "transfer_rate": 43.1,
                "signals_validated": 4,
                "last_updated": "2026-03-28",
                "status": "Ready for betting implementation"
            }

            self.wfile.write(json.dumps(status, indent=2).encode())
            return

        # Default: serve static files
        try:
            super().do_GET()
        except Exception as e:
            self.send_error(404)

def main():
    os.chdir(BASE_DIR)

    print("\n" + "="*70)
    print("GOLF ANALYTICS - MOBILE DASHBOARD SERVER")
    print("="*70)
    print(f"\nStarting server on port {PORT}...")
    print(f"\nAccess from Android phone:")
    print(f"  1. Find your PC's local IP (run 'ipconfig' on Windows)")
    print(f"  2. Open browser on phone: http://YOUR_PC_IP:{PORT}")
    print(f"\nExample: http://192.168.1.100:{PORT}")
    print(f"\nAPI Endpoints:")
    print(f"  /api/signals  - Get all 4 signals")
    print(f"  /api/status   - Get model status")
    print(f"\nPress Ctrl+C to stop server")
    print("="*70 + "\n")

    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            print(f"✓ Server running at http://localhost:{PORT}/")
            print(f"✓ Open http://localhost:{PORT}/ in browser")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except OSError as e:
        print(f"\nError: Port {PORT} is already in use.")
        print(f"Try a different port or close other applications.")

if __name__ == "__main__":
    main()
