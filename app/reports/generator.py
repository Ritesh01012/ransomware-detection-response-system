"""
Report generation for RDRS.
Generates JSON and CSV reports from database data.
"""

import json
import csv
import os
import sys
from datetime import datetime

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from database.operations import (
    get_events,
    get_processes,
    get_alerts,
    get_incidents,
    get_quarantine_records
)

# Configuration
REPORTS_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "reports_output")


def generate_report_filename(base_name, format_type):
    """
    Generate a unique filename for reports.
    Format: base_name_YYYYMMDD_HHMMSS_microseconds.ext
    
    Args:
        base_name: Base name for the report
        format_type: 'json' or 'csv'
    
    Returns:
        str: Unique filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    ext = "json" if format_type == "json" else "csv"
    return f"{base_name}_{timestamp}.{ext}"


def generate_json_report(data, report_type):
    """
    Generate a JSON report.
    
    Args:
        data: List of dictionaries to include in report
        report_type: Type of report (events, processes, alerts, incidents, quarantine)
    
    Returns:
        dict: Report with metadata and data
    """
    report = {
        "report_type": report_type,
        "generated_at": datetime.now().isoformat(),
        "record_count": len(data),
        "data": data
    }
    return report


def generate_csv_report(data, fieldnames):
    """
    Generate CSV data from list of dictionaries.
    
    Args:
        data: List of dictionaries
        fieldnames: List of field names for CSV header
    
    Returns:
        str: CSV formatted string
    """
    import io
    buffer = io.StringIO()
    csv_writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    csv_writer.writeheader()
    csv_writer.writerows(data)
    
    return buffer.getvalue()


def save_report(content, filename):
    """
    Save report to file.
    
    Args:
        content: Report content (string for JSON or CSV)
        filename: Filename to save
    
    Returns:
        str: Full path to saved file
    
    Raises:
        IOError: If file cannot be written
    """
    # Ensure output directory exists
    os.makedirs(REPORTS_OUTPUT_PATH, exist_ok=True)
    
    filepath = os.path.join(REPORTS_OUTPUT_PATH, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath


def generate_events_report(format_type="json"):
    """
    Generate events report.
    
    Args:
        format_type: 'json' or 'csv'
    
    Returns:
        dict: Report info with filepath and metadata
    """
    records = get_events()
    
    data = [
        {
            "id": row[0],
            "event_type": row[1],
            "file_path": row[2],
            "entropy": row[3],
            "timestamp": row[4]
        }
        for row in records
    ]
    
    if format_type == "json":
        report = generate_json_report(data, "events")
        content = json.dumps(report, indent=2)
    else:
        fieldnames = ["id", "event_type", "file_path", "entropy", "timestamp"]
        content = generate_csv_report(data, fieldnames)
    
    filename = generate_report_filename("events", format_type)
    filepath = save_report(content, filename)
    
    return {
        "report_type": "events",
        "format": format_type,
        "filepath": filepath,
        "record_count": len(data),
        "generated_at": datetime.now().isoformat()
    }


def generate_processes_report(format_type="json"):
    """
    Generate processes report.
    
    Args:
        format_type: 'json' or 'csv'
    
    Returns:
        dict: Report info with filepath and metadata
    """
    records = get_processes()
    
    data = [
        {
            "id": row[0],
            "pid": row[1],
            "name": row[2],
            "cpu_percent": row[3],
            "memory_mb": row[4],
            "executable": row[5],
            "timestamp": row[6]
        }
        for row in records
    ]
    
    if format_type == "json":
        report = generate_json_report(data, "processes")
        content = json.dumps(report, indent=2)
    else:
        fieldnames = ["id", "pid", "name", "cpu_percent", "memory_mb", "executable", "timestamp"]
        content = generate_csv_report(data, fieldnames)
    
    filename = generate_report_filename("processes", format_type)
    filepath = save_report(content, filename)
    
    return {
        "report_type": "processes",
        "format": format_type,
        "filepath": filepath,
        "record_count": len(data),
        "generated_at": datetime.now().isoformat()
    }


def generate_alerts_report(format_type="json"):
    """
    Generate alerts report.
    
    Args:
        format_type: 'json' or 'csv'
    
    Returns:
        dict: Report info with filepath and metadata
    """
    records = get_alerts()
    
    data = [
        {
            "id": row[0],
            "threat_score": row[1],
            "threat_level": row[2],
            "reason": row[3],
            "timestamp": row[4]
        }
        for row in records
    ]
    
    if format_type == "json":
        report = generate_json_report(data, "alerts")
        content = json.dumps(report, indent=2)
    else:
        fieldnames = ["id", "threat_score", "threat_level", "reason", "timestamp"]
        content = generate_csv_report(data, fieldnames)
    
    filename = generate_report_filename("alerts", format_type)
    filepath = save_report(content, filename)
    
    return {
        "report_type": "alerts",
        "format": format_type,
        "filepath": filepath,
        "record_count": len(data),
        "generated_at": datetime.now().isoformat()
    }


def generate_incidents_report(format_type="json"):
    """
    Generate incidents report.
    
    Args:
        format_type: 'json' or 'csv'
    
    Returns:
        dict: Report info with filepath and metadata
    """
    records = get_incidents()
    
    data = [
        {
            "id": row[0],
            "alert_id": row[1],
            "status": row[2],
            "timestamp": row[3]
        }
        for row in records
    ]
    
    if format_type == "json":
        report = generate_json_report(data, "incidents")
        content = json.dumps(report, indent=2)
    else:
        fieldnames = ["id", "alert_id", "status", "timestamp"]
        content = generate_csv_report(data, fieldnames)
    
    filename = generate_report_filename("incidents", format_type)
    filepath = save_report(content, filename)
    
    return {
        "report_type": "incidents",
        "format": format_type,
        "filepath": filepath,
        "record_count": len(data),
        "generated_at": datetime.now().isoformat()
    }


def generate_quarantine_report(format_type="json"):
    """
    Generate quarantine report.
    
    Args:
        format_type: 'json' or 'csv'
    
    Returns:
        dict: Report info with filepath and metadata
    """
    records = get_quarantine_records()
    
    data = [
        {
            "id": row[0],
            "original_path": row[1],
            "evidence_path": row[2],
            "action_result": row[3],
            "timestamp": row[4]
        }
        for row in records
    ]
    
    if format_type == "json":
        report = generate_json_report(data, "quarantine")
        content = json.dumps(report, indent=2)
    else:
        fieldnames = ["id", "original_path", "evidence_path", "action_result", "timestamp"]
        content = generate_csv_report(data, fieldnames)
    
    filename = generate_report_filename("quarantine", format_type)
    filepath = save_report(content, filename)
    
    return {
        "report_type": "quarantine",
        "format": format_type,
        "filepath": filepath,
        "record_count": len(data),
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    print("=" * 50)
    print("Report Generation Test")
    print("=" * 50)
    
    # Test JSON reports
    print("\n1. Testing JSON reports...")
    events_json = generate_events_report("json")
    print(f"   Events JSON: {events_json['filepath']}")
    print(f"   Records: {events_json['record_count']}")
    
    alerts_json = generate_alerts_report("json")
    print(f"   Alerts JSON: {alerts_json['filepath']}")
    print(f"   Records: {alerts_json['record_count']}")
    
    # Test CSV reports
    print("\n2. Testing CSV reports...")
    events_csv = generate_events_report("csv")
    print(f"   Events CSV: {events_csv['filepath']}")
    print(f"   Records: {events_csv['record_count']}")
    
    alerts_csv = generate_alerts_report("csv")
    print(f"   Alerts CSV: {alerts_csv['filepath']}")
    print(f"   Records: {alerts_csv['record_count']}")
    
    print("\n" + "=" * 50)
    print("Report Generation Test Complete")
    print("=" * 50)
