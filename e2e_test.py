"""
End-to-End Acceptance Test for RDRS.
Tests the complete workflow from API to dashboard to reports.
"""

import urllib.request
import json
import os
import sys
import time

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), ".")
sys.path.insert(0, app_dir)

from app.reports.generator import (
    generate_events_report,
    generate_alerts_report
)
from app.response.quarantine import quarantine_file
from app.response.alert_manager import create_alert, create_incident, update_incident

print("=" * 70)
print("RDRS End-to-End Acceptance Test")
print("=" * 70)

# Test 1: Dashboard Load
print("\n[TEST 1] Dashboard Load")
try:
    with urllib.request.urlopen("http://127.0.0.1:5000/dashboard", timeout=5) as response:
        content = response.read().decode()
    if "RDRS Security" in content:
        print("✅ PASS: Dashboard loads successfully")
    else:
        print("❌ FAIL: Dashboard content unexpected")
except Exception as e:
    print(f"❌ FAIL: Dashboard load error: {e}")

# Test 2: API Status Endpoint
print("\n[TEST 2] API Status Endpoint")
try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/status", timeout=5) as response:
        data = json.loads(response.read().decode())
    required_fields = ["events", "process_records", "alerts", "incidents", "open_incidents"]
    if all(field in data for field in required_fields):
        print(f"✅ PASS: API status endpoint working")
        print(f"   Events: {data['events']}, Alerts: {data['alerts']}, Incidents: {data['incidents']}")
    else:
        print(f"❌ FAIL: Missing fields in status response")
except Exception as e:
    print(f"❌ FAIL: API status error: {e}")

# Test 3: API Events Endpoint
print("\n[TEST 3] API Events Endpoint")
try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/events", timeout=5) as response:
        data = json.loads(response.read().decode())
    if isinstance(data, list):
        print(f"✅ PASS: API events endpoint working")
        print(f"   Retrieved {len(data)} events")
    else:
        print(f"❌ FAIL: Events response not a list")
except Exception as e:
    print(f"❌ FAIL: API events error: {e}")

# Test 4: API Processes Endpoint
print("\n[TEST 4] API Processes Endpoint")
try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/processes", timeout=5) as response:
        data = json.loads(response.read().decode())
    if isinstance(data, list):
        print(f"✅ PASS: API processes endpoint working")
        print(f"   Retrieved {len(data)} process records")
    else:
        print(f"❌ FAIL: Processes response not a list")
except Exception as e:
    print(f"❌ FAIL: API processes error: {e}")

# Test 5: API Alerts Endpoint
print("\n[TEST 5] API Alerts Endpoint")
try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/alerts", timeout=5) as response:
        data = json.loads(response.read().decode())
    if isinstance(data, list):
        print(f"✅ PASS: API alerts endpoint working")
        print(f"   Retrieved {len(data)} alerts")
    else:
        print(f"❌ FAIL: Alerts response not a list")
except Exception as e:
    print(f"❌ FAIL: API alerts error: {e}")

# Test 6: API Incidents Endpoint
print("\n[TEST 6] API Incidents Endpoint")
try:
    with urllib.request.urlopen("http://127.0.0.1:5000/api/incidents", timeout=5) as response:
        data = json.loads(response.read().decode())
    if isinstance(data, list):
        print(f"✅ PASS: API incidents endpoint working")
        print(f"   Retrieved {len(data)} incidents")
    else:
        print(f"❌ FAIL: Incidents response not a list")
except Exception as e:
    print(f"❌ FAIL: API incidents error: {e}")

# Test 7: Generate Test Events in Sandbox
print("\n[TEST 7] Generate Test Events in Sandbox")
sandbox_path = os.path.join(os.path.dirname(__file__), "sandbox")
test_file = os.path.join(sandbox_path, "e2e_test.txt")
try:
    with open(test_file, "w") as f:
        f.write("End-to-end test file content")
    print(f"✅ PASS: Test file created in sandbox: {test_file}")
    time.sleep(1)  # Allow monitor to detect
except Exception as e:
    print(f"❌ FAIL: Could not create test file: {e}")

# Test 8: Alert Creation
print("\n[TEST 8] Alert Creation")
try:
    alert_id = create_alert(50, "MEDIUM", "E2E test alert")
    print(f"✅ PASS: Alert created with ID: {alert_id}")
except Exception as e:
    print(f"❌ FAIL: Alert creation failed: {e}")

# Test 9: Incident Creation
print("\n[TEST 9] Incident Creation")
try:
    incident_id = create_incident(alert_id, "OPEN")
    print(f"✅ PASS: Incident created with ID: {incident_id}")
except Exception as e:
    print(f"❌ FAIL: Incident creation failed: {e}")

# Test 10: Incident Status Update
print("\n[TEST 10] Incident Status Update")
try:
    update_incident(incident_id, "INVESTIGATING")
    print(f"✅ PASS: Incident status updated to INVESTIGATING")
except Exception as e:
    print(f"❌ FAIL: Incident status update failed: {e}")

# Test 11: Quarantine Simulation
print("\n[TEST 11] Quarantine Simulation")
try:
    result = quarantine_file(test_file)
    print(f"✅ PASS: File quarantined successfully")
    print(f"   Evidence: {os.path.basename(result['evidence_path'])}")
    print(f"   Hash verified: {result['hash_verified']}")
    
    # Verify original file preserved
    if os.path.exists(test_file):
        print(f"✅ PASS: Original file preserved")
    else:
        print(f"❌ FAIL: Original file was modified/deleted")
except Exception as e:
    print(f"❌ FAIL: Quarantine failed: {e}")

# Test 12: JSON Report Generation
print("\n[TEST 12] JSON Report Generation")
try:
    report = generate_events_report("json")
    if os.path.exists(report["filepath"]):
        print(f"✅ PASS: JSON report generated")
        print(f"   File: {os.path.basename(report['filepath'])}")
        print(f"   Records: {report['record_count']}")
    else:
        print(f"❌ FAIL: Report file not created")
except Exception as e:
    print(f"❌ FAIL: JSON report generation failed: {e}")

# Test 13: CSV Report Generation
print("\n[TEST 13] CSV Report Generation")
try:
    report = generate_alerts_report("csv")
    if os.path.exists(report["filepath"]):
        print(f"✅ PASS: CSV report generated")
        print(f"   File: {os.path.basename(report['filepath'])}")
        print(f"   Records: {report['record_count']}")
    else:
        print(f"❌ FAIL: Report file not created")
except Exception as e:
    print(f"❌ FAIL: CSV report generation failed: {e}")

# Test 14: Unique Filenames
print("\n[TEST 14] Unique Report Filenames")
try:
    report1 = generate_events_report("json")
    report2 = generate_events_report("json")
    filename1 = os.path.basename(report1["filepath"])
    filename2 = os.path.basename(report2["filepath"])
    if filename1 != filename2:
        print(f"✅ PASS: Unique filenames generated")
        print(f"   File 1: {filename1}")
        print(f"   File 2: {filename2}")
    else:
        print(f"❌ FAIL: Filenames are identical")
except Exception as e:
    print(f"❌ FAIL: Unique filename test failed: {e}")

# Cleanup
print("\n[CLEANUP]")
try:
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✅ Test file cleaned up")
except Exception as e:
    print(f"⚠️  Cleanup warning: {e}")

print("\n" + "=" * 70)
print("End-to-End Acceptance Test Complete")
print("=" * 70)
