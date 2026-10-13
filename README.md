# Ransomware Detection and Response System (RDRS)

A defensive educational security system for detecting suspicious file activity, analyzing threats, and simulating incident response. RDRS monitors file system events, calculates entropy, generates alerts, manages incidents, and produces security reports.

## ⚠️ Disclaimer

**This is a defensive educational project for learning purposes only. It does not guarantee detection of all ransomware or malicious software. Never use real malware for testing. Always test with harmless files in the designated sandbox directory.**

---

## Project Overview

RDRS is a Python-based security monitoring system designed to detect potential ransomware behavior through:

- **File System Monitoring**: Real-time monitoring of file creation, modification, deletion, and rename events
- **Entropy Analysis**: Shannon entropy calculation to detect encrypted or high-entropy files
- **Threat Scoring**: Sliding time window analysis to calculate threat scores based on suspicious activity patterns
- **Alert Management**: Structured alert creation with threat levels (LOW, MEDIUM, HIGH, CRITICAL)
- **Incident Tracking**: Incident lifecycle management with status tracking (OPEN, INVESTIGATING, RESOLVED, CLOSED)
- **Safe Quarantine**: Simulation-only evidence copying with SHA-256 hash verification
- **Report Generation**: JSON and CSV security reports for events, processes, alerts, incidents, and quarantine records
- **Web Dashboard**: Real-time security dashboard for monitoring system status

---

## System Architecture

```
RDRS_Project/
├── app/
│   ├── api/              # Flask REST API and web dashboard
│   ├── config/           # Configuration management
│   ├── database/         # SQLite database models and operations
│   ├── detection/        # Entropy calculation and threat detection engine
│   ├── monitor/          # File and process monitoring
│   ├── reports/          # Report generation (JSON/CSV)
│   └── response/         # Alert manager and quarantine simulation
├── sandbox/              # Monitored directory for safe testing
├── quarantine/           # Evidence storage directory
├── reports_output/       # Generated security reports
├── tests/                # Pytest test suite
├── config.yaml           # System configuration
├── requirements.txt      # Python dependencies
└── rdrs.db              # SQLite database (created on first run)
```

---

## Data Flow

```
File Activity (Sandbox)
    ↓
File Monitor (Watchdog)
    ↓
Entropy Calculation
    ↓
Database (Events Table)
    ↓
Detection Engine (Sliding Window)
    ↓
Threat Score Calculation
    ↓
Alert Generation (Alerts Table)
    ↓
Incident Creation (Incidents Table)
    ↓
Quarantine Simulation (Evidence Copy + Hash Verification)
    ↓
Report Generation (JSON/CSV)
```

---

## Technologies and Dependencies

- **Python**: 3.12+
- **Flask**: 3.1.3 - REST API and web dashboard
- **Watchdog**: 6.0.0 - File system monitoring
- **psutil**: 7.2.2 - Process monitoring
- **PyYAML**: 6.0.3 - Configuration management
- **pytest**: 9.1.1 - Testing framework
- **SQLite**: Embedded database (Python standard library)

---

## Windows Setup Instructions

### Prerequisites

- Windows 10/11
- Python 3.12 or higher
- PowerShell or Command Prompt

### Step 1: Clone or Extract Project

Navigate to the project directory:

```cmd
cd C:\Users\Lenovo\Desktop\RDRS_Project
```

### Step 2: Create Virtual Environment

**Using PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Using Command Prompt:**

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Step 3: Install Dependencies

```cmd
pip install -r requirements.txt
```

### Step 4: Verify Installation

```cmd
python -m pytest --version
```

Expected output: `pytest 9.1.1`

---

## Running the System

### Start Flask REST API and Dashboard

```cmd
python app\api\routes.py
```

The API will start at `http://127.0.0.1:5000`

**Dashboard URL:** `http://127.0.0.1:5000/dashboard`

### Start File Monitor

Open a new terminal (keep the API running):

```cmd
python app\monitor\file_monitor.py
```

The file monitor will watch the `sandbox/` directory for file activity.

### Start Process Monitor

Open another terminal:

```cmd
python app\monitor\process_monitor.py
```

The process monitor will collect system process information every 30 seconds.

---

## API Endpoints

### System Status

- `GET /api/status` - Returns counts of events, processes, alerts, incidents, and open incidents

### Data Retrieval

- `GET /api/events` - Retrieve recent file events (limit 50)
- `GET /api/processes` - Retrieve recent process records (limit 50)
- `GET /api/alerts` - Retrieve recent alerts (limit 50)
- `GET /api/incidents` - Retrieve recent incidents (limit 50)

### Incident Management

- `PATCH /api/incidents/<incident_id>` - Update incident status

**Request Body (JSON):**
```json
{
  "status": "OPEN" | "INVESTIGATING" | "RESOLVED" | "CLOSED"
}
```

### Report Generation

- `GET /api/reports/<report_type>/<format>` - Generate and download report

**Valid report types:** `events`, `processes`, `alerts`, `incidents`, `quarantine`

**Valid formats:** `json`, `csv`

**Example:**
```
GET /api/reports/alerts/json
GET /api/reports/events/csv
```

---

## Safe Testing Instructions

### Create Test Files in Sandbox

**Using PowerShell:**

```powershell
# Create a test file
echo "This is a test file" > sandbox\test.txt

# Create a high-entropy file (simulating encrypted content)
$random = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 1000 | % {[char]$_})
$random > sandbox\high_entropy.txt
```

**Using Command Prompt:**

```cmd
echo This is a test file > sandbox\test.txt
```

### Monitor Detection

1. Ensure the file monitor is running
2. Create or modify files in the `sandbox/` directory
3. Check the dashboard at `http://127.0.0.1:5000/dashboard`
4. View alerts and incidents via API endpoints

### Test Quarantine

```cmd
python app\response\quarantine.py
```

This will create a test file in sandbox, quarantine it with hash verification, and verify the original file is preserved.

---

## Running Tests

### Run All Tests

```cmd
venv\Scripts\python.exe -m pytest -v
```

### Run Specific Test Suite

```cmd
venv\Scripts\python.exe -m pytest tests\test_alerts.py -v
venv\Scripts\python.exe -m pytest tests\test_quarantine.py -v
venv\Scripts\python.exe -m pytest tests\test_reports.py -v
```

### Run with Detailed Output

```cmd
venv\Scripts\python.exe -m pytest -vv --tb=long
```

### Interpreting Results

- **PASSED**: Test executed successfully
- **FAILED**: Test assertion failed (investigate the error)
- **ERROR**: Test encountered an exception (check traceback)

---

## Report Generation Examples

### Generate JSON Report

**Via API:**
```
GET http://127.0.0.1:5000/api/reports/events/json
```

**Via Python:**
```python
from app.reports.generator import generate_events_report

report = generate_events_report("json")
print(f"Report saved to: {report['filepath']}")
print(f"Records: {report['record_count']}")
```

### Generate CSV Report

**Via API:**
```
GET http://127.0.0.1:5000/api/reports/alerts/csv
```

**Via Python:**
```python
from app.reports.generator import generate_alerts_report

report = generate_alerts_report("csv")
print(f"Report saved to: {report['filepath']}")
```

### Report Location

All reports are saved to: `reports_output/`

Report filename format: `<type>_YYYYMMDD_HHMMSS_microseconds.<ext>`

---

## Configuration

Edit `config.yaml` to customize system behavior:

```yaml
monitor:
  paths:
    - "./sandbox"              # Directory to monitor
  process_interval_seconds: 30  # Process collection interval

detection:
  entropy_threshold: 7.0        # High entropy threshold
  time_window_seconds: 60       # Detection time window
  modification_threshold: 20    # Alert threshold for modifications
  deletion_threshold: 10        # Alert threshold for deletions
  rename_threshold: 10          # Alert threshold for renames
  alert_threshold: 40           # Overall threat score threshold

response:
  simulation_mode: true         # Enable simulation mode
  quarantine_path: "./quarantine"  # Evidence storage directory

reports:
  output_path: "./reports_output"  # Report output directory

database:
  path: "./rdrs.db"             # SQLite database file

api:
  host: "127.0.0.1"             # API host
  port: 5000                    # API port
  debug: false                  # Debug mode
```

---

## Limitations

- **Simulation Only**: Quarantine is simulation-only; original files are never modified or deleted
- **Sandbox-Restricted**: Only files in the configured sandbox directory can be quarantined
- **No Real-Time Protection**: This is a monitoring and detection system, not a real-time antivirus
- **Educational Purpose**: Not suitable for production security environments
- **Windows Only**: Currently tested on Windows 10/11
- **Single-User**: Not designed for multi-user environments
- **No Network Monitoring**: Does not monitor network traffic or remote file systems

---

## Troubleshooting

### Port Already in Use

If you see `Address already in use`, change the port in `config.yaml`:

```yaml
api:
  port: 5001
```

### Database Locked

If you encounter database lock errors, ensure no other processes are accessing `rdrs.db`. Close all terminals and restart.

### Import Errors

Ensure you are in the virtual environment:

```cmd
.\venv\Scripts\activate
```

### File Monitor Not Detecting Events

- Verify the file monitor is running
- Check that files are being created in the `sandbox/` directory
- Ensure the path in `config.yaml` matches your actual sandbox location

### High CPU Usage

The process monitor runs every 30 seconds by default. Increase the interval in `config.yaml`:

```yaml
monitor:
  process_interval_seconds: 60
```

---

## Test Coverage

The project includes comprehensive tests for:

- **Database Operations** (1 test)
- **Alert Management** (6 tests)
  - Status validation
  - Threat score validation
  - Threat level validation
  - Alert creation
  - Incident creation
  - Incident status updates
- **Quarantine Simulation** (7 tests)
  - Successful quarantine
  - Hash verification
  - Missing file handling
  - Outside-sandbox path rejection
  - Path traversal protection
  - Collision-safe filename generation
  - Directory rejection
- **Report Generation** (8 tests)
  - JSON report generation
  - CSV report generation
  - All report types
  - Unique filenames
  - Report directory
  - JSON structure
  - CSV structure
  - Empty data handling

**Total: 22 tests**

---

## Security Considerations

- **No Privilege Escalation**: The system runs with standard user permissions
- **No Network Exposure**: API binds to localhost only (127.0.0.1)
- **Parameterized Queries**: All database queries use parameterized statements to prevent SQL injection
- **Path Validation**: Quarantine enforces sandbox-only access with path traversal protection
- **Hash Verification**: Evidence copies are verified with SHA-256 hashes
- **Simulation Mode**: Original files are never modified or deleted

---

## License

This project is for educational purposes. Use responsibly and ethically.

---

## Contributing

This is an educational project. Contributions should focus on:
- Improving detection accuracy
- Adding educational documentation
- Enhancing test coverage
- Fixing bugs

---

## Version

**Current Version:** 1.0.0

---

## Contact

For questions or issues related to this educational project, please refer to the documentation or create an issue in the project repository.
