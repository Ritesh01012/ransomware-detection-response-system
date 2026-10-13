"""
Safe Quarantine Simulation for RDRS.
Creates evidence copies of files with hash verification.
"""

import os
import hashlib
import shutil
import json
import sys
from datetime import datetime

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from database.operations import save_quarantine_record


# Configuration
SANDBOX_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "sandbox")
QUARANTINE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "quarantine")


def calculate_sha256(file_path):
    """
    Calculate SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file
    
    Returns:
        str: Hexadecimal SHA-256 hash
    
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
    """
    sha256_hash = hashlib.sha256()
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()


def validate_sandbox_path(file_path):
    """
    Validate that file is inside sandbox directory.
    Prevents path traversal attacks.
    
    Args:
        file_path: Path to validate
    
    Returns:
        bool: True if path is safe
    
    Raises:
        ValueError: If path is outside sandbox or contains traversal
    """
    # Resolve absolute paths
    abs_file_path = os.path.abspath(file_path)
    abs_sandbox_path = os.path.abspath(SANDBOX_PATH)
    
    # Normalize paths to resolve any ".." components
    abs_file_path = os.path.normpath(abs_file_path)
    abs_sandbox_path = os.path.normpath(abs_sandbox_path)
    
    # Check if file is inside sandbox
    if not abs_file_path.startswith(abs_sandbox_path):
        raise ValueError(
            f"File is outside sandbox directory: {file_path} not in {abs_sandbox_path}"
        )
    
    return True


def generate_evidence_filename(original_path):
    """
    Generate a collision-safe filename for evidence copy.
    Format: original_name_timestamp_random.ext
    
    Args:
        original_path: Original file path
    
    Returns:
        str: Safe filename for evidence copy
    """
    original_name = os.path.basename(original_path)
    name, ext = os.path.splitext(original_name)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = os.urandom(4).hex()
    
    evidence_name = f"{name}_{timestamp}_{random_suffix}{ext}"
    return evidence_name


def quarantine_file(file_path):
    """
    Create an evidence copy of a file in quarantine.
    Original file is NOT modified or moved.
    
    Args:
        file_path: Path to the file to quarantine
    
    Returns:
        dict: Quarantine record with hashes and paths
    
    Raises:
        ValueError: If validation fails
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be accessed
    """
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Validate file is inside sandbox
    validate_sandbox_path(file_path)
    
    # Check if it's a file (not directory)
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Calculate original hash
    original_hash = calculate_sha256(file_path)
    
    # Generate evidence filename
    evidence_filename = generate_evidence_filename(file_path)
    evidence_path = os.path.join(QUARANTINE_PATH, evidence_filename)
    
    # Ensure quarantine directory exists
    os.makedirs(QUARANTINE_PATH, exist_ok=True)
    
    # Copy file to quarantine
    shutil.copy2(file_path, evidence_path)
    
    # Calculate evidence hash
    evidence_hash = calculate_sha256(evidence_path)
    
    # Verify hashes match
    if original_hash != evidence_hash:
        # Cleanup failed copy
        if os.path.exists(evidence_path):
            os.remove(evidence_path)
        raise ValueError(
            f"Hash verification failed: original={original_hash}, evidence={evidence_hash}"
        )
    
    # Prepare action result with hash info
    action_result = json.dumps({
        "original_hash": original_hash,
        "evidence_hash": evidence_hash,
        "hash_verified": True,
        "simulation": True,
        "original_file_preserved": True
    })
    
    # Save to database
    record_id = save_quarantine_record(file_path, evidence_path, action_result)
    
    return {
        "record_id": record_id,
        "original_path": file_path,
        "evidence_path": evidence_path,
        "original_hash": original_hash,
        "evidence_hash": evidence_hash,
        "hash_verified": True,
        "action_result": action_result
    }


if __name__ == "__main__":
    # Test quarantine
    print("=" * 50)
    print("Quarantine Simulation Test")
    print("=" * 50)
    
    # Create a test file in sandbox
    test_file = os.path.join(SANDBOX_PATH, "quarantine_test.txt")
    
    try:
        with open(test_file, "w") as f:
            f.write("This is a test file for quarantine simulation.")
        
        print(f"\nTest file created: {test_file}")
        
        # Quarantine the file
        result = quarantine_file(test_file)
        
        print(f"\nQuarantine successful:")
        print(f"  Record ID: {result['record_id']}")
        print(f"  Original: {result['original_path']}")
        print(f"  Evidence: {result['evidence_path']}")
        print(f"  Original Hash: {result['original_hash']}")
        print(f"  Evidence Hash: {result['evidence_hash']}")
        print(f"  Hash Verified: {result['hash_verified']}")
        
        # Verify original file still exists
        if os.path.exists(test_file):
            print(f"\n✓ Original file preserved: {test_file}")
        
        # Verify evidence copy exists
        if os.path.exists(result['evidence_path']):
            print(f"✓ Evidence copy created: {result['evidence_path']}")
        
        print("\n" + "=" * 50)
        print("Quarantine Test Complete")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError: {e}")
