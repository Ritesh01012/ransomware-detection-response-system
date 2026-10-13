"""
Database CRUD operations for RDRS.
All queries use parameterized statements to prevent SQL injection.
"""

from .models import get_connection


# ==================== EVENT OPERATIONS ====================

def save_event(event_type, file_path, entropy=None):
    """
    Save a file event to the database.
    
    Args:
        event_type: CREATE, MODIFY, DELETE, RENAME
        file_path: Full path to the file
        entropy: Shannon entropy value (optional)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO events (event_type, file_path, entropy)
        VALUES (?, ?, ?)
    """, (event_type, file_path, entropy))
    
    conn.commit()
    conn.close()


def get_events(limit=None):
    """
    Retrieve file events from the database.
    
    Args:
        limit: Maximum number of records to return (None = all)
    
    Returns:
        List of tuples (id, event_type, file_path, entropy, timestamp)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("""
            SELECT id, event_type, file_path, entropy, timestamp
            FROM events
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT id, event_type, file_path, entropy, timestamp
            FROM events
            ORDER BY id DESC
        """)
    
    events = cursor.fetchall()
    conn.close()
    
    return events


def get_recent_events(seconds=60):
    """
    Retrieve events from the last N seconds.
    
    Args:
        seconds: Time window in seconds
    
    Returns:
        List of tuples (event_type, entropy, timestamp)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT event_type, entropy, timestamp
        FROM events
        WHERE timestamp >= datetime('now', '-' || ? || ' seconds')
        ORDER BY timestamp DESC
    """, (seconds,))
    
    events = cursor.fetchall()
    conn.close()
    
    return events


# ==================== PROCESS OPERATIONS ====================

def save_process(pid, name, cpu_percent, memory_mb, executable):
    """
    Save process metadata to the database.
    
    Args:
        pid: Process ID
        name: Process name
        cpu_percent: CPU usage percentage
        memory_mb: Memory usage in MB
        executable: Executable path
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO processes (pid, name, cpu_percent, memory_mb, executable)
        VALUES (?, ?, ?, ?, ?)
    """, (pid, name, cpu_percent, memory_mb, executable))
    
    conn.commit()
    conn.close()


def get_processes(limit=None):
    """
    Retrieve process records from the database.
    
    Args:
        limit: Maximum number of records to return (None = all)
    
    Returns:
        List of tuples (id, pid, name, cpu_percent, memory_mb, executable, timestamp)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("""
            SELECT id, pid, name, cpu_percent, memory_mb, executable, timestamp
            FROM processes
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT id, pid, name, cpu_percent, memory_mb, executable, timestamp
            FROM processes
            ORDER BY id DESC
        """)
    
    processes = cursor.fetchall()
    conn.close()
    
    return processes


# ==================== ALERT OPERATIONS ====================

def save_alert(threat_score, threat_level, reason):
    """
    Save an alert to the database.
    
    Args:
        threat_score: Threat score (0-100)
        threat_level: LOW, MEDIUM, HIGH, CRITICAL
        reason: Human-readable reason for the alert
    
    Returns:
        alert_id: The ID of the created alert
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO alerts (threat_score, threat_level, reason)
        VALUES (?, ?, ?)
    """, (threat_score, threat_level, reason))
    
    alert_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return alert_id


def get_alerts(limit=None):
    """
    Retrieve alerts from the database.
    
    Args:
        limit: Maximum number of records to return (None = all)
    
    Returns:
        List of tuples (id, threat_score, threat_level, reason, timestamp)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("""
            SELECT id, threat_score, threat_level, reason, timestamp
            FROM alerts
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT id, threat_score, threat_level, reason, timestamp
            FROM alerts
            ORDER BY id DESC
        """)
    
    alerts = cursor.fetchall()
    conn.close()
    
    return alerts


# ==================== INCIDENT OPERATIONS ====================

def save_incident(alert_id, status="OPEN"):
    """
    Save an incident to the database.
    
    Args:
        alert_id: Foreign key to alerts table
        status: OPEN, INVESTIGATING, RESOLVED
    
    Returns:
        incident_id: The ID of the created incident
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO incidents (alert_id, status)
        VALUES (?, ?)
    """, (alert_id, status))
    
    incident_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return incident_id


def get_incidents(limit=None):
    """
    Retrieve incidents from the database.
    
    Args:
        limit: Maximum number of records to return (None = all)
    
    Returns:
        List of tuples (id, alert_id, status, timestamp)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("""
            SELECT id, alert_id, status, timestamp
            FROM incidents
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT id, alert_id, status, timestamp
            FROM incidents
            ORDER BY id DESC
        """)
    
    incidents = cursor.fetchall()
    conn.close()
    
    return incidents


def update_incident_status(incident_id, status):
    """
    Update the status of an incident.
    
    Args:
        incident_id: ID of the incident to update
        status: New status (OPEN, INVESTIGATING, RESOLVED)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE incidents
        SET status = ?
        WHERE id = ?
    """, (status, incident_id))
    
    conn.commit()
    conn.close()


# ==================== QUARANTINE OPERATIONS ====================

def save_quarantine_record(original_path, evidence_path, action_result):
    """
    Save a quarantine record to the database.
    
    Args:
        original_path: Original file path
        evidence_path: Path to quarantined copy
        action_result: Result of quarantine action
    
    Returns:
        record_id: The ID of the created record
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO quarantine (original_path, evidence_path, action_result)
        VALUES (?, ?, ?)
    """, (original_path, evidence_path, action_result))
    
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return record_id


def get_quarantine_records(limit=None):
    """
    Retrieve quarantine records from the database.
    
    Args:
        limit: Maximum number of records to return (None = all)
    
    Returns:
        List of tuples (id, original_path, evidence_path, action_result, timestamp)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("""
            SELECT id, original_path, evidence_path, action_result, timestamp
            FROM quarantine
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    else:
        cursor.execute("""
            SELECT id, original_path, evidence_path, action_result, timestamp
            FROM quarantine
            ORDER BY id DESC
        """)
    
    records = cursor.fetchall()
    conn.close()
    
    return records


# ==================== COUNT OPERATIONS ====================

def count_events():
    """Return total number of events."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def count_processes():
    """Return total number of process records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM processes")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def count_alerts():
    """Return total number of alerts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM alerts")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def count_incidents():
    """Return total number of incidents."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def count_open_incidents():
    """Return number of incidents with OPEN status."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE status = 'OPEN'")
    count = cursor.fetchone()[0]
    conn.close()
    return count
