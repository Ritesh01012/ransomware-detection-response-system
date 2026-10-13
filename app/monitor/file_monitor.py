"""
File monitoring using Watchdog.
Monitors the sandbox directory for file activity.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from detection.entropy import calculate_entropy
from database.operations import save_event


class RDRSEventHandler(FileSystemEventHandler):
    """
    Handles file system events in the monitored directory.
    """
    
    def on_created(self, event):
        """Called when a file or directory is created."""
        if not event.is_directory:
            print(f"[FILE CREATED] {event.src_path}")
            
            try:
                entropy = calculate_entropy(event.src_path)
                print(f"    Entropy: {entropy:.4f}")
                save_event("CREATE", event.src_path, entropy)
            except Exception as e:
                print(f"    Error calculating entropy: {e}")
                save_event("CREATE", event.src_path, None)
    
    def on_modified(self, event):
        """Called when a file or directory is modified."""
        if not event.is_directory:
            print(f"[FILE MODIFIED] {event.src_path}")
            
            try:
                entropy = calculate_entropy(event.src_path)
                print(f"    Entropy: {entropy:.4f}")
                save_event("MODIFY", event.src_path, entropy)
            except Exception as e:
                print(f"    Error calculating entropy: {e}")
                save_event("MODIFY", event.src_path, None)
    
    def on_deleted(self, event):
        """Called when a file or directory is deleted."""
        if not event.is_directory:
            print(f"[FILE DELETED] {event.src_path}")
            # Cannot calculate entropy for deleted files
            save_event("DELETE", event.src_path, None)
    
    def on_moved(self, event):
        """Called when a file or directory is moved or renamed."""
        if not event.is_directory:
            print(f"[FILE RENAMED]")
            print(f"    FROM: {event.src_path}")
            print(f"    TO:   {event.dest_path}")
            # Save the destination path with entropy
            try:
                entropy = calculate_entropy(event.dest_path)
                print(f"    Entropy: {entropy:.4f}")
                save_event("RENAME", event.dest_path, entropy)
            except Exception as e:
                print(f"    Error calculating entropy: {e}")
                save_event("RENAME", event.dest_path, None)


def start_file_monitor(path, recursive=True):
    """
    Start the file monitor for the given path.
    
    Args:
        path: Directory path to monitor
        recursive: Whether to monitor subdirectories
    """
    event_handler = RDRSEventHandler()
    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=recursive)
    observer.start()
    
    print("=" * 50)
    print("RDRS FILE MONITOR")
    print("=" * 50)
    print(f"Monitoring: {path}")
    print(f"Recursive: {recursive}")
    print("Press CTRL+C to stop.")
    print()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()


if __name__ == "__main__":
    # Monitor the sandbox directory
    sandbox_path = os.path.join(
        os.path.dirname(__file__), "..", "..", "sandbox"
    )
    
    # Ensure sandbox directory exists
    if not os.path.exists(sandbox_path):
        os.makedirs(sandbox_path)
        print(f"Created sandbox directory: {sandbox_path}")
    
    start_file_monitor(sandbox_path)
