"""
Detection engine for threat analysis.
Uses sliding time window and threat scoring.
"""

import sys
import os

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from database.operations import (
    get_recent_events,
    save_alert,
    save_incident,
    get_alerts
)
from detection.entropy import is_high_entropy


# Configuration (will be loaded from config.yaml in future)
TIME_WINDOW_SECONDS = 60
ALERT_THRESHOLD = 40
ENTROPY_THRESHOLD = 7.0


def calculate_threat_score(modified_count, renamed_count, deleted_count, high_entropy_count):
    """
    Calculate threat score based on event counts.
    
    Args:
        modified_count: Number of file modification events
        renamed_count: Number of file rename events
        deleted_count: Number of file deletion events
        high_entropy_count: Number of high-entropy events
    
    Returns:
        score: Threat score (0-100)
    """
    score = 0
    
    # Modified events
    if modified_count >= 5:
        score += 25
    elif modified_count >= 3:
        score += 15
    
    # Renamed events
    if renamed_count >= 3:
        score += 20
    elif renamed_count >= 1:
        score += 10
    
    # Deleted events
    if deleted_count >= 3:
        score += 20
    elif deleted_count >= 1:
        score += 10
    
    # High entropy events (strong indicator)
    if high_entropy_count >= 5:
        score += 35
    elif high_entropy_count >= 2:
        score += 20
    elif high_entropy_count >= 1:
        score += 10
    
    return min(score, 100)


def get_threat_level(score):
    """
    Convert threat score to threat level.
    
    Args:
        score: Threat score (0-100)
    
    Returns:
        level: LOW, MEDIUM, HIGH, or CRITICAL
    """
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"


def analyze_events():
    """
    Analyze recent events and generate alerts if suspicious.
    """
    events = get_recent_events(seconds=TIME_WINDOW_SECONDS)
    
    # Count event types
    modified_count = 0
    renamed_count = 0
    deleted_count = 0
    high_entropy_count = 0
    
    for event in events:
        event_type = event[0]
        entropy = event[1]
        
        if event_type == "MODIFY":
            modified_count += 1
        elif event_type == "RENAME":
            renamed_count += 1
        elif event_type == "DELETE":
            deleted_count += 1
        
        # Check for high entropy
        if entropy is not None and is_high_entropy(entropy, ENTROPY_THRESHOLD):
            high_entropy_count += 1
    
    # Calculate threat score
    score = calculate_threat_score(
        modified_count,
        renamed_count,
        deleted_count,
        high_entropy_count
    )
    
    level = get_threat_level(score)
    
    # Print analysis
    print("=" * 50)
    print("RDRS DETECTION ENGINE")
    print("=" * 50)
    print(f"Time Window: {TIME_WINDOW_SECONDS} seconds")
    print(f"Modified: {modified_count}")
    print(f"Renamed: {renamed_count}")
    print(f"Deleted: {deleted_count}")
    print(f"High Entropy: {high_entropy_count}")
    print()
    print(f"Threat Score: {score} / 100")
    print(f"Threat Level: {level}")
    print()
    
    # Generate alert if threshold crossed
    if score >= ALERT_THRESHOLD:
        reason = (
            f"Suspicious activity detected: "
            f"modified={modified_count}, "
            f"renamed={renamed_count}, "
            f"deleted={deleted_count}, "
            f"high_entropy={high_entropy_count}"
        )
        
        # Check for duplicate recent alert
        alerts = get_alerts(limit=10)
        duplicate_found = False
        
        for alert in alerts:
            if alert[3] == reason:  # alert[3] is reason
                duplicate_found = True
                break
        
        if not duplicate_found:
            alert_id = save_alert(score, level, reason)
            incident_id = save_incident(alert_id, "OPEN")
            
            print("ALERT GENERATED!")
            print(f"Alert ID: {alert_id}")
            print(f"Incident ID: {incident_id}")
            print(f"Reason: {reason}")
        else:
            print("Recent matching alert already exists. Skipping duplicate.")
    else:
        print("No alert generated. Score below threshold.")
    
    print("=" * 50)
    
    return score, level


if __name__ == "__main__":
    analyze_events()
