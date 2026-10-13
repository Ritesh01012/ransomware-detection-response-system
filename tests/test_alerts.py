"""
Tests for Alert and Incident Manager.
Tests validation, creation, and status updates.
"""

import sys
import os

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from app.response.alert_manager import (
    validate_status,
    validate_threat_score,
    validate_threat_level,
    create_alert,
    create_incident,
    update_incident,
    get_incident_by_id
)
from app.database.operations import get_incidents


def test_status_validation():
    """Test valid and invalid status values."""
    print("\n1. Testing status validation...")
    
    # Valid statuses
    valid_statuses = ["OPEN", "INVESTIGATING", "RESOLVED", "CLOSED"]
    for status in valid_statuses:
        try:
            validate_status(status)
            print(f"   ✓ Valid status '{status}' accepted")
        except ValueError:
            print(f"   ✗ Valid status '{status}' rejected (FAIL)")
            assert False, f"Valid status '{status}' was rejected"
    
    # Invalid status
    try:
        validate_status("INVALID_STATUS")
        print("   ✗ Invalid status accepted (FAIL)")
        assert False, "Invalid status was accepted"
    except ValueError as e:
        print(f"   ✓ Invalid status rejected: {e}")
        assert "Invalid status" in str(e)


def test_threat_score_validation():
    """Test threat score validation."""
    print("\n2. Testing threat score validation...")
    
    # Valid scores
    valid_scores = [0, 50, 100, 75.5]
    for score in valid_scores:
        try:
            validate_threat_score(score)
            print(f"   ✓ Valid score {score} accepted")
        except ValueError:
            print(f"   ✗ Valid score {score} rejected (FAIL)")
            assert False, f"Valid score {score} was rejected"
    
    # Invalid scores
    invalid_scores = [-1, 101, 150, "invalid"]
    for score in invalid_scores:
        try:
            validate_threat_score(score)
            print(f"   ✗ Invalid score {score} accepted (FAIL)")
            assert False, f"Invalid score {score} was accepted"
        except ValueError as e:
            print(f"   ✓ Invalid score {score} rejected")
            assert "Threat score" in str(e)


def test_threat_level_validation():
    """Test threat level validation."""
    print("\n3. Testing threat level validation...")
    
    # Valid levels
    valid_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    for level in valid_levels:
        try:
            validate_threat_level(level)
            print(f"   ✓ Valid level '{level}' accepted")
        except ValueError:
            print(f"   ✗ Valid level '{level}' rejected (FAIL)")
            assert False, f"Valid level '{level}' was rejected"
    
    # Invalid level
    try:
        validate_threat_level("INVALID")
        print("   ✗ Invalid level accepted (FAIL)")
        assert False, "Invalid level was accepted"
    except ValueError as e:
        print(f"   ✓ Invalid level rejected: {e}")
        assert "Invalid threat level" in str(e)


def test_alert_creation():
    """Test alert creation with validation."""
    print("\n4. Testing alert creation...")
    
    alert_id = create_alert(65, "HIGH", "Test alert for validation")
    print(f"   ✓ Alert created with ID: {alert_id}")
    assert alert_id is not None
    assert isinstance(alert_id, int)
    assert alert_id > 0


def test_incident_creation():
    """Test incident creation with validation."""
    print("\n5. Testing incident creation...")
    
    # Create a test alert first
    alert_id = create_alert(50, "MEDIUM", "Test alert for incident creation")
    assert alert_id is not None
    
    # Create incident
    incident_id = create_incident(alert_id, "OPEN")
    print(f"   ✓ Incident created with ID: {incident_id}")
    assert incident_id is not None
    assert isinstance(incident_id, int)
    assert incident_id > 0
    
    # Verify incident exists
    incident = get_incident_by_id(incident_id)
    assert incident is not None
    assert incident[1] == alert_id  # alert_id matches
    assert incident[2] == "OPEN"  # status matches


def test_incident_update():
    """Test incident status update with validation."""
    print("\n6. Testing incident status update...")
    
    # Create test alert and incident
    alert_id = create_alert(75, "HIGH", "Test alert for incident update")
    incident_id = create_incident(alert_id, "OPEN")
    
    # Valid update
    update_incident(incident_id, "INVESTIGATING")
    print(f"   ✓ Incident {incident_id} updated to INVESTIGATING")
    
    # Verify update
    incident = get_incident_by_id(incident_id)
    assert incident is not None
    assert incident[2] == "INVESTIGATING"
    print(f"   ✓ Update verified: status is {incident[2]}")
    
    # Invalid status
    try:
        update_incident(incident_id, "INVALID_STATUS")
        print("   ✗ Invalid status accepted (FAIL)")
        assert False, "Invalid status was accepted"
    except ValueError as e:
        print(f"   ✓ Invalid status rejected: {e}")
        assert "Invalid status" in str(e)
    
    # Missing incident ID
    try:
        update_incident(99999, "RESOLVED")
        print("   ✗ Missing incident ID accepted (FAIL)")
        assert False, "Missing incident ID was accepted"
    except ValueError as e:
        print(f"   ✓ Missing incident ID rejected: {e}")
        assert "does not exist" in str(e)


def run_all_tests():
    """Run all alert manager tests."""
    print("=" * 50)
    print("Alert Manager Tests")
    print("=" * 50)
    
    results = []
    
    # Run tests
    results.append(("Status Validation", test_status_validation()))
    results.append(("Threat Score Validation", test_threat_score_validation()))
    results.append(("Threat Level Validation", test_threat_level_validation()))
    
    alert_id = test_alert_creation()
    incident_id = test_incident_creation(alert_id)
    
    results.append(("Alert Creation", alert_id is not None))
    results.append(("Incident Creation", incident_id is not None))
    results.append(("Incident Update", test_incident_update(incident_id)))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 50)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
