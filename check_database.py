"""
Check database records are preserved.
"""

from app.database.operations import (
    count_events,
    count_processes,
    count_alerts,
    count_incidents,
    count_open_incidents,
    get_quarantine_records
)

print("=" * 50)
print("Database Records Check")
print("=" * 50)

print(f"\nEvents: {count_events()}")
print(f"Process Records: {count_processes()}")
print(f"Alerts: {count_alerts()}")
print(f"Incidents: {count_incidents()}")
print(f"Open Incidents: {count_open_incidents()}")

quarantine_records = get_quarantine_records(limit=5)
print(f"\nQuarantine Records (last 5): {len(quarantine_records)}")

for record in quarantine_records:
    print(f"  ID: {record[0]}")
    print(f"  Original: {record[1]}")
    print(f"  Evidence: {record[2]}")
    print(f"  Result: {record[3][:50]}...")
    print()

print("=" * 50)
