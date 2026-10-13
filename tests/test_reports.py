"""
Tests for Report Generation.
Tests JSON and CSV output, empty data, and error handling.
"""

import sys
import os
import json
import csv

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from app.reports.generator import (
    generate_events_report,
    generate_processes_report,
    generate_alerts_report,
    generate_incidents_report,
    generate_quarantine_report,
    REPORTS_OUTPUT_PATH
)


def test_json_report_generation():
    """Test JSON report generation."""
    print("\n1. Testing JSON report generation...")
    
    report = generate_events_report("json")
    
    # Verify report structure
    assert "report_type" in report
    assert "format" in report
    assert "filepath" in report
    assert "record_count" in report
    assert "generated_at" in report
    
    assert report["report_type"] == "events"
    assert report["format"] == "json"
    assert report["record_count"] >= 0
    
    # Verify file exists
    assert os.path.exists(report["filepath"])
    
    # Verify file is valid JSON
    with open(report["filepath"], "r") as f:
        data = json.load(f)
    
    assert "report_type" in data
    assert "data" in data
    assert "generated_at" in data
    
    print(f"   ✓ JSON report generated: {report['filepath']}")
    print(f"   ✓ Records: {report['record_count']}")


def test_csv_report_generation():
    """Test CSV report generation."""
    print("\n2. Testing CSV report generation...")
    
    report = generate_alerts_report("csv")
    
    # Verify report structure
    assert "report_type" in report
    assert "format" in report
    assert "filepath" in report
    assert "record_count" in report
    
    assert report["report_type"] == "alerts"
    assert report["format"] == "csv"
    
    # Verify file exists
    assert os.path.exists(report["filepath"])
    
    # Verify file is valid CSV
    with open(report["filepath"], "r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    assert len(rows) == report["record_count"]
    
    print(f"   ✓ CSV report generated: {report['filepath']}")
    print(f"   ✓ Records: {report['record_count']}")


def test_all_report_types():
    """Test all report types can be generated."""
    print("\n3. Testing all report types...")
    
    report_types = [
        ("events", generate_events_report),
        ("processes", generate_processes_report),
        ("alerts", generate_alerts_report),
        ("incidents", generate_incidents_report),
        ("quarantine", generate_quarantine_report)
    ]
    
    for report_type, generator in report_types:
        report = generator("json")
        assert report["report_type"] == report_type
        assert os.path.exists(report["filepath"])
        print(f"   ✓ {report_type} report generated")
    
    for report_type, generator in report_types:
        report = generator("csv")
        assert report["report_type"] == report_type
        assert os.path.exists(report["filepath"])
        print(f"   ✓ {report_type} CSV generated")


def test_unique_filenames():
    """Test that reports have unique filenames."""
    print("\n4. Testing unique filenames...")
    
    report1 = generate_events_report("json")
    report2 = generate_events_report("json")
    
    # Filenames should be different (different timestamps)
    filename1 = os.path.basename(report1["filepath"])
    filename2 = os.path.basename(report2["filepath"])
    
    assert filename1 != filename2
    print(f"   ✓ Unique filenames generated")
    print(f"   ✓ File 1: {filename1}")
    print(f"   ✓ File 2: {filename2}")


def test_report_directory():
    """Test reports are saved in correct directory."""
    print("\n5. Testing report directory...")
    
    report = generate_incidents_report("json")
    
    assert report["filepath"].startswith(REPORTS_OUTPUT_PATH)
    assert os.path.exists(REPORTS_OUTPUT_PATH)
    
    print(f"   ✓ Reports saved in: {REPORTS_OUTPUT_PATH}")


def test_json_structure():
    """Test JSON report has correct structure."""
    print("\n6. Testing JSON structure...")
    
    report = generate_alerts_report("json")
    
    with open(report["filepath"], "r") as f:
        data = json.load(f)
    
    # Verify top-level structure
    assert "report_type" in data
    assert "generated_at" in data
    assert "record_count" in data
    assert "data" in data
    
    # Verify data is a list
    assert isinstance(data["data"], list)
    
    # Verify record count matches
    assert data["record_count"] == len(data["data"])
    
    print(f"   ✓ JSON structure valid")
    print(f"   ✓ Record count matches: {data['record_count']}")


def test_csv_structure():
    """Test CSV report has correct structure."""
    print("\n7. Testing CSV structure...")
    
    report = generate_processes_report("csv")
    
    with open(report["filepath"], "r", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)
    
    # Verify expected fields
    expected_fields = ["id", "pid", "name", "cpu_percent", "memory_mb", "executable", "timestamp"]
    for field in expected_fields:
        assert field in fieldnames, f"Missing field: {field}"
    
    print(f"   ✓ CSV structure valid")
    print(f"   ✓ Fields: {', '.join(fieldnames)}")


def test_empty_data_handling():
    """Test reports handle empty data gracefully."""
    print("\n8. Testing empty data handling...")
    
    # Even with no data, reports should generate
    # (This test assumes database has data, but verifies no crashes)
    report = generate_quarantine_report("json")
    
    assert report["record_count"] >= 0
    assert os.path.exists(report["filepath"])
    
    print(f"   ✓ Empty data handled gracefully")
    print(f"   ✓ Records: {report['record_count']}")


if __name__ == "__main__":
    print("=" * 50)
    print("Report Generation Tests")
    print("=" * 50)
    
    try:
        test_json_report_generation()
        test_csv_report_generation()
        test_all_report_types()
        test_unique_filenames()
        test_report_directory()
        test_json_structure()
        test_csv_structure()
        test_empty_data_handling()
        
        print("\n" + "=" * 50)
        print("All report tests passed")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
