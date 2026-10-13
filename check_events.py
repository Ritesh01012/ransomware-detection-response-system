"""
Quick check to verify file events were saved to database.
"""

from app.database.operations import get_events, count_events

print("=" * 50)
print("Database Event Check")
print("=" * 50)

events = get_events(limit=10)
total = count_events()

print(f"\nTotal events in database: {total}")
print(f"\nRecent events (last 10):")

for event in events:
    print(f"  ID: {event[0]} | Type: {event[1]} | File: {event[2]} | Entropy: {event[3]} | Time: {event[4]}")

print("\n" + "=" * 50)
