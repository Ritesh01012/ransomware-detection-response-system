"""
Quick test to verify database initialization and basic operations.
Run this to check if Phase 2 is working correctly.
"""

from app.database.models import initialize_database, get_connection
from app.database.operations import (
    save_event, get_events,
    save_process, get_processes,
    save_alert, get_alerts,
    save_incident, get_incidents,
    count_events, count_processes, count_alerts, count_incidents
)


def test_database():
    print("=" * 50)
    print("RDRS Database Test")
    print("=" * 50)
    
    # Initialize database
    print("\n1. Initializing database...")
    initialize_database()
    
    # Test event operations
    print("\n2. Testing event operations...")
    save_event("MODIFY", "sandbox/test.txt", 5.5)
    save_event("CREATE", "sandbox/new.txt", 0.0)
    events = get_events(limit=5)
    print(f"   Saved and retrieved {len(events)} events")
    
    # Test process operations
    print("\n3. Testing process operations...")
    save_process(1234, "test.exe", 2.5, 128.0, "C:\\test.exe")
    processes = get_processes(limit=5)
    print(f"   Saved and retrieved {len(processes)} process records")
    
    # Test alert operations
    print("\n4. Testing alert operations...")
    alert_id = save_alert(65, "HIGH", "Test alert for verification")
    alerts = get_alerts(limit=5)
    print(f"   Saved and retrieved {len(alerts)} alerts")
    print(f"   Alert ID: {alert_id}")
    
    # Test incident operations
    print("\n5. Testing incident operations...")
    incident_id = save_incident(alert_id, "OPEN")
    incidents = get_incidents(limit=5)
    print(f"   Saved and retrieved {len(incidents)} incidents")
    print(f"   Incident ID: {incident_id}")
    
    # Test count operations
    print("\n6. Testing count operations...")
    print(f"   Total events: {count_events()}")
    print(f"   Total processes: {count_processes()}")
    print(f"   Total alerts: {count_alerts()}")
    print(f"   Total incidents: {count_incidents()}")
    
    print("\n" + "=" * 50)
    print("Database test completed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    test_database()
