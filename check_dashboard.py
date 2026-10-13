"""
Check dashboard is accessible.
"""

import urllib.request

try:
    with urllib.request.urlopen("http://127.0.0.1:5000/dashboard", timeout=2) as response:
        content = response.read().decode()
        
    print("=" * 50)
    print("Dashboard Check")
    print("=" * 50)
    print(f"Status Code: {response.status}")
    
    if "RDRS Security" in content:
        print("✓ Dashboard loaded successfully")
        print("✓ Contains RDRS Security title")
    else:
        print("✗ Dashboard content unexpected")
    
    print("=" * 50)
    
except Exception as e:
    print(f"Error: {e}")
