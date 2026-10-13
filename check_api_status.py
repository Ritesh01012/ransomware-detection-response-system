"""
Check if API is accessible.
"""

import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/status", timeout=2) as response:
        data = json.loads(response.read().decode())
    print("API Status: RUNNING")
    print(f"Events: {data['events']}")
    print(f"Alerts: {data['alerts']}")
    print(f"Incidents: {data['incidents']}")
except Exception as e:
    print(f"API Status: NOT RUNNING - {e}")
