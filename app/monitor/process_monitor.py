"""
Process monitoring using psutil.
Collects process metadata for analysis.
"""

import psutil
import sys
import os

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from database.operations import save_process


def collect_processes():
    """
    Collect process information from the system.
    
    Returns:
        List of process dictionaries with metadata
    """
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'exe']):
        try:
            info = proc.info
            
            # Extract memory info
            memory = info.get('memory_info')
            memory_mb = 0.0
            if memory:
                memory_mb = round(memory.rss / (1024 * 1024), 2)
            
            # Extract CPU percent
            cpu_percent = info.get('cpu_percent')
            if cpu_percent is None:
                cpu_percent = 0.0
            
            process_data = {
                'pid': info['pid'],
                'name': info['name'],
                'cpu_percent': cpu_percent,
                'memory_mb': memory_mb,
                'executable': info.get('exe')
            }
            
            processes.append(process_data)
            
            # Save to database
            save_process(
                process_data['pid'],
                process_data['name'],
                process_data['cpu_percent'],
                process_data['memory_mb'],
                process_data['executable']
            )
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes that disappeared or are inaccessible
            continue
    
    return processes


def print_process_summary(processes, limit=10):
    """
    Print a summary of collected processes.
    
    Args:
        processes: List of process dictionaries
        limit: Number of processes to display
    """
    print("=" * 50)
    print("RDRS PROCESS MONITOR")
    print("=" * 50)
    print(f"Total processes collected: {len(processes)}")
    print()
    print(f"Top {limit} processes:")
    print()
    
    for proc in processes[:limit]:
        print(f"PID: {proc['pid']}")
        print(f"  Name: {proc['name']}")
        print(f"  CPU: {proc['cpu_percent']}%")
        print(f"  Memory: {proc['memory_mb']} MB")
        print(f"  Executable: {proc['executable']}")
        print()


if __name__ == "__main__":
    processes = collect_processes()
    print_process_summary(processes)
