"""
Alert and Incident Manager for RDRS.
Provides structured alert creation, incident management, and status validation.
"""

import sys
import os

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from database.operations import (
    save_alert,
    save_incident,
    update_incident_status,
    get_incidents
)


# Valid status values
VALID_STATUSES = ["OPEN", "INVESTIGATING", "RESOLVED", "CLOSED"]


def validate_status(status):
    """
    Validate that status is a valid value.
    
    Args:
        status: Status string to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    Raises:
        ValueError: If status is not valid
    """
    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid status '{status}'. "
            f"Valid statuses: {', '.join(VALID_STATUSES)}"
        )
    return True


def validate_threat_score(score):
    """
    Validate that threat score is within valid range.
    
    Args:
        score: Threat score (0-100)
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If score is out of range
    """
    if not isinstance(score, (int, float)):
        raise ValueError(f"Threat score must be a number, got {type(score)}")
    
    if score < 0 or score > 100:
        raise ValueError(f"Threat score must be between 0 and 100, got {score}")
    
    return True


def validate_threat_level(level):
    """
    Validate that threat level is a valid value.
    
    Args:
        level: Threat level string
    
    Returns:
        bool: True if valid
    
    Raises:
        ValueError: If level is not valid
    """
    valid_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    if level not in valid_levels:
        raise ValueError(
            f"Invalid threat level '{level}'. "
            f"Valid levels: {', '.join(valid_levels)}"
        )
    return True


def create_alert(threat_score, threat_level, reason):
    """
    Create a new alert with validation.
    
    Args:
        threat_score: Threat score (0-100)
        threat_level: LOW, MEDIUM, HIGH, CRITICAL
        reason: Human-readable reason for the alert
    
    Returns:
        alert_id: The ID of the created alert
    
    Raises:
        ValueError: If validation fails
    """
    validate_threat_score(threat_score)
    validate_threat_level(threat_level)
    
    if not reason or not isinstance(reason, str):
        raise ValueError("Reason must be a non-empty string")
    
    alert_id = save_alert(threat_score, threat_level, reason)
    return alert_id


def create_incident(alert_id, status="OPEN"):
    """
    Create a new incident with validation.
    
    Args:
        alert_id: Foreign key to alerts table
        status: OPEN, INVESTIGATING, RESOLVED, CLOSED
    
    Returns:
        incident_id: The ID of the created incident
    
    Raises:
        ValueError: If validation fails
    """
    validate_status(status)
    
    if not isinstance(alert_id, int) or alert_id <= 0:
        raise ValueError(f"Alert ID must be a positive integer, got {alert_id}")
    
    incident_id = save_incident(alert_id, status)
    return incident_id


def update_incident(incident_id, new_status):
    """
    Update incident status with validation.
    
    Args:
        incident_id: ID of the incident to update
        new_status: New status (OPEN, INVESTIGATING, RESOLVED, CLOSED)
    
    Returns:
        bool: True if update successful
    
    Raises:
        ValueError: If validation fails
    """
    validate_status(new_status)
    
    if not isinstance(incident_id, int) or incident_id <= 0:
        raise ValueError(f"Incident ID must be a positive integer, got {incident_id}")
    
    # Check if incident exists
    incidents = get_incidents()
    incident_exists = any(inc[0] == incident_id for inc in incidents)
    
    if not incident_exists:
        raise ValueError(f"Incident with ID {incident_id} does not exist")
    
    update_incident_status(incident_id, new_status)
    return True


def get_incident_by_id(incident_id):
    """
    Get a specific incident by ID.
    
    Args:
        incident_id: ID of the incident to retrieve
    
    Returns:
        tuple: Incident data (id, alert_id, status, timestamp) or None if not found
    """
    incidents = get_incidents()
    
    for incident in incidents:
        if incident[0] == incident_id:
            return incident
    
    return None


if __name__ == "__main__":
    # Test alert manager
    print("=" * 50)
    print("Alert Manager Test")
    print("=" * 50)
    
    try:
        # Test validation
        print("\n1. Testing status validation:")
        validate_status("OPEN")
        print("   Valid status 'OPEN': PASS")
        
        try:
            validate_status("INVALID")
        except ValueError as e:
            print(f"   Invalid status error: {e}")
        
        # Test alert creation
        print("\n2. Testing alert creation:")
        alert_id = create_alert(65, "HIGH", "Test alert from alert manager")
        print(f"   Alert created with ID: {alert_id}")
        
        # Test incident creation
        print("\n3. Testing incident creation:")
        incident_id = create_incident(alert_id, "OPEN")
        print(f"   Incident created with ID: {incident_id}")
        
        # Test incident update
        print("\n4. Testing incident update:")
        update_incident(incident_id, "INVESTIGATING")
        print(f"   Incident {incident_id} updated to INVESTIGATING")
        
        # Verify update
        incident = get_incident_by_id(incident_id)
        print(f"   Current status: {incident[2]}")
        
        print("\n" + "=" * 50)
        print("Alert Manager Test Complete")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error: {e}")
