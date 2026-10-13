"""
Check API status endpoint response.
"""

import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/status", timeout=5) as response:
        data = json.loads(response.read().decode())
    
    print("Status Response:")
    print(json.dumps(data, indent=2))
    print(f"\nKeys: {list(data.keys())}")
    
except Exception as e:
    print(f"Error: {e}")
