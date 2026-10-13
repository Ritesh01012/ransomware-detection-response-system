"""
Verify database records.
"""

from app.database.operations import (
    count_events,
    count_processes,
    count_alerts,
    count_incidents,
    count_open_incidents,
    get_quarantine_records
)

print("=" * 70)
print("Database Verification")
print("=" * 70)
print(f"Events: {count_events()}")
print(f"Process Records: {count_processes()}")
print(f"Alerts: {count_alerts()}")
print(f"Incidents: {count_incidents()}")
print(f"Open Incidents: {count_open_incidents()}")
print(f"Quarantine Records: {len(get_quarantine_records())}")
print("=" * 70)
