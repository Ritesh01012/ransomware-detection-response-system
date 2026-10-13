"""
Quick check to verify Flask API is working.
"""

import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/status", timeout=2) as response:
        data = json.loads(response.read().decode())
    
    print("=" * 50)
    print("Flask API Status Check")
    print("=" * 50)
    print(f"Status Code: {response.status}")
    print(f"Response: {json.dumps(data, indent=2)}")
    print("=" * 50)
    
except Exception as e:
    print(f"Error: {e}")
