"""
Flask REST API for RDRS.
Provides endpoints for status, events, processes, alerts, incidents.
"""

from flask import Flask, jsonify, render_template, request, send_file
import sys
import os

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from database.operations import (
    get_events,
    get_processes,
    get_alerts,
    get_incidents,
    count_events,
    count_processes,
    count_alerts,
    count_incidents,
    count_open_incidents
)
from response.alert_manager import (
    update_incident,
    validate_status
)
from reports.generator import (
    generate_events_report,
    generate_processes_report,
    generate_alerts_report,
    generate_incidents_report,
    generate_quarantine_report
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """API information endpoint."""
    return jsonify({
        "project": "Ransomware Detection and Response System",
        "status": "running",
        "version": "1.0.0",
        "endpoints": [
            "/api/status",
            "/api/events",
            "/api/processes",
            "/api/alerts",
            "/api/incidents",
            "/api/reports/<report_type>/<format>",
            "/dashboard"
        ]
    })


@app.route("/api/status", methods=["GET"])
def status():
    """Get system status and counts."""
    return jsonify({
        "events": count_events(),
        "process_records": count_processes(),
        "alerts": count_alerts(),
        "incidents": count_incidents(),
        "open_incidents": count_open_incidents()
    })


@app.route("/api/events", methods=["GET"])
def events():
    """Get recent file events."""
    records = get_events(limit=50)
    
    return jsonify([
        {
            "id": row[0],
            "event_type": row[1],
            "file_path": row[2],
            "entropy": row[3],
            "timestamp": row[4]
        }
        for row in records
    ])


@app.route("/api/processes", methods=["GET"])
def processes():
    """Get recent process records."""
    records = get_processes(limit=50)
    
    return jsonify([
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
    ])


@app.route("/api/alerts", methods=["GET"])
def alerts():
    """Get recent alerts."""
    records = get_alerts(limit=50)
    
    return jsonify([
        {
            "id": row[0],
            "threat_score": row[1],
            "threat_level": row[2],
            "reason": row[3],
            "timestamp": row[4]
        }
        for row in records
    ])


@app.route("/api/incidents", methods=["GET"])
def incidents():
    """Get recent incidents."""
    records = get_incidents(limit=50)
    
    return jsonify([
        {
            "id": row[0],
            "alert_id": row[1],
            "status": row[2],
            "timestamp": row[3]
        }
        for row in records
    ])


@app.route("/api/incidents/<int:incident_id>", methods=["PATCH"])
def update_incident_status(incident_id):
    """
    Update incident status.
    
    Request body (JSON):
    {
        "status": "OPEN" | "INVESTIGATING" | "RESOLVED" | "CLOSED"
    }
    """
    try:
        data = request.get_json()
        
        if not data or "status" not in data:
            return jsonify({
                "error": "Missing 'status' field in request body"
            }), 400
        
        new_status = data["status"]
        
        # Validate status
        try:
            validate_status(new_status)
        except ValueError as e:
            return jsonify({
                "error": str(e)
            }), 400
        
        # Update incident
        update_incident(incident_id, new_status)
        
        return jsonify({
            "success": True,
            "incident_id": incident_id,
            "status": new_status
        }), 200
        
    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 404
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Serve the web dashboard."""
    return render_template("dashboard.html")


@app.route("/api/reports/<report_type>/<format>", methods=["GET"])
def generate_report(report_type, format):
    """
    Generate and download a report.
    
    Args:
        report_type: events, processes, alerts, incidents, quarantine
        format: json or csv
    
    Returns:
        File download or error response
    """
    # Validate format
    if format not in ["json", "csv"]:
        return jsonify({
            "error": "Invalid format. Use 'json' or 'csv'"
        }), 400
    
    # Validate report type
    valid_types = ["events", "processes", "alerts", "incidents", "quarantine"]
    if report_type not in valid_types:
        return jsonify({
            "error": f"Invalid report type. Valid types: {', '.join(valid_types)}"
        }), 400
    
    try:
        # Generate report
        if report_type == "events":
            report_info = generate_events_report(format)
        elif report_type == "processes":
            report_info = generate_processes_report(format)
        elif report_type == "alerts":
            report_info = generate_alerts_report(format)
        elif report_type == "incidents":
            report_info = generate_incidents_report(format)
        elif report_type == "quarantine":
            report_info = generate_quarantine_report(format)
        
        # Send file
        return send_file(
            report_info["filepath"],
            as_attachment=True,
            download_name=os.path.basename(report_info["filepath"])
        )
        
    except Exception as e:
        return jsonify({
            "error": f"Report generation failed: {str(e)}"
        }), 500


if __name__ == "__main__":
    print("=" * 50)
    print("RDRS REST API")
    print("=" * 50)
    print("Starting Flask server...")
    print(f"Dashboard: http://127.0.0.1:5000/dashboard")
    print("Press CTRL+C to stop.")
    print("=" * 50)
    
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
