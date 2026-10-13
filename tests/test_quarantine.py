"""
Tests for Quarantine Simulation.
Tests safe file copying, hash verification, and path validation.
"""

import sys
import os
import shutil

# Add app directory to path for imports
app_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, app_dir)

from app.response.quarantine import (
    quarantine_file,
    calculate_sha256,
    validate_sandbox_path,
    generate_evidence_filename,
    SANDBOX_PATH,
    QUARANTINE_PATH
)


def test_successful_quarantine():
    """Test successful file quarantine with hash verification."""
    print("\n1. Testing successful quarantine...")
    
    # Create test file
    test_file = os.path.join(SANDBOX_PATH, "test_quarantine_1.txt")
    with open(test_file, "w") as f:
        f.write("Test content for quarantine")
    
    try:
        result = quarantine_file(test_file)
        
        # Verify result structure
        assert "record_id" in result
        assert "original_path" in result
        assert "evidence_path" in result
        assert "original_hash" in result
        assert "evidence_hash" in result
        assert "hash_verified" in result
        
        # Verify hash verification
        assert result["hash_verified"] is True
        assert result["original_hash"] == result["evidence_hash"]
        
        # Verify original file preserved
        assert os.path.exists(test_file)
        
        # Verify evidence copy created
        assert os.path.exists(result["evidence_path"])
        
        # Verify evidence is in quarantine directory
        assert result["evidence_path"].startswith(QUARANTINE_PATH)
        
        print(f"   ✓ Quarantine successful, record ID: {result['record_id']}")
        print(f"   ✓ Hash verified: {result['original_hash'][:16]}...")
        
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        if "result" in locals() and os.path.exists(result["evidence_path"]):
            os.remove(result["evidence_path"])


def test_hash_verification():
    """Test that hash verification works correctly."""
    print("\n2. Testing hash verification...")
    
    # Create test file
    test_file = os.path.join(SANDBOX_PATH, "test_hash.txt")
    with open(test_file, "w") as f:
        f.write("Hash verification test content")
    
    try:
        # Calculate hash before quarantine
        original_hash = calculate_sha256(test_file)
        
        # Quarantine
        result = quarantine_file(test_file)
        
        # Verify hashes match
        assert result["original_hash"] == original_hash
        assert result["evidence_hash"] == original_hash
        assert result["hash_verified"] is True
        
        print(f"   ✓ Hash verification successful")
        print(f"   ✓ Hash: {original_hash[:16]}...")
        
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
        if "result" in locals() and os.path.exists(result["evidence_path"]):
            os.remove(result["evidence_path"])


def test_missing_file():
    """Test quarantine of missing file raises error."""
    print("\n3. Testing missing file handling...")
    
    missing_file = os.path.join(SANDBOX_PATH, "nonexistent_file.txt")
    
    try:
        quarantine_file(missing_file)
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        print(f"   ✓ Missing file error raised: {e}")
        assert "File not found" in str(e)


def test_outside_sandbox_path():
    """Test that files outside sandbox are rejected."""
    print("\n4. Testing outside-sandbox path rejection...")
    
    # Test with a file outside sandbox (in project root)
    outside_file = os.path.join(app_dir, "..", "test_outside.txt")
    
    # Create the file first
    with open(outside_file, "w") as f:
        f.write("This file is outside sandbox")
    
    try:
        quarantine_file(outside_file)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Outside-sandbox path rejected: {e}")
        assert "outside sandbox" in str(e).lower()
    finally:
        # Cleanup
        if os.path.exists(outside_file):
            os.remove(outside_file)


def test_path_traversal():
    """Test that path traversal attempts are handled safely."""
    print("\n5. Testing path traversal handling...")
    
    # Create a file outside sandbox using absolute path
    outside_file = os.path.join(app_dir, "..", "test_traversal.txt")
    with open(outside_file, "w") as f:
        f.write("Traversal test file")
    
    try:
        # Try to quarantine using a path that would traverse
        # The validation should normalize and detect it's outside sandbox
        quarantine_file(outside_file)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Path traversal handled safely: {e}")
        assert "outside sandbox" in str(e).lower()
    finally:
        if os.path.exists(outside_file):
            os.remove(outside_file)


def test_duplicate_filename():
    """Test that duplicate filenames are handled with collision-safe names."""
    print("\n6. Testing collision-safe filename generation...")
    
    # Create test file
    test_file = os.path.join(SANDBOX_PATH, "test_duplicate.txt")
    with open(test_file, "w") as f:
        f.write("Duplicate filename test")
    
    try:
        # Quarantine twice
        result1 = quarantine_file(test_file)
        result2 = quarantine_file(test_file)
        
        # Verify different evidence filenames
        evidence1 = os.path.basename(result1["evidence_path"])
        evidence2 = os.path.basename(result2["evidence_path"])
        
        assert evidence1 != evidence2
        assert evidence1.startswith("test_duplicate_")
        assert evidence2.startswith("test_duplicate_")
        
        print(f"   ✓ Collision-safe names generated")
        print(f"   ✓ Evidence 1: {evidence1}")
        print(f"   ✓ Evidence 2: {evidence2}")
        
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)
        if "result1" in locals() and os.path.exists(result1["evidence_path"]):
            os.remove(result1["evidence_path"])
        if "result2" in locals() and os.path.exists(result2["evidence_path"]):
            os.remove(result2["evidence_path"])


def test_directory_rejection():
    """Test that directories are rejected."""
    print("\n7. Testing directory rejection...")
    
    try:
        quarantine_file(SANDBOX_PATH)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        print(f"   ✓ Directory rejected: {e}")
        assert "not a file" in str(e).lower()


if __name__ == "__main__":
    print("=" * 50)
    print("Quarantine Tests")
    print("=" * 50)
    
    # Ensure directories exist
    os.makedirs(SANDBOX_PATH, exist_ok=True)
    os.makedirs(QUARANTINE_PATH, exist_ok=True)
    
    try:
        test_successful_quarantine()
        test_hash_verification()
        test_missing_file()
        test_outside_sandbox_path()
        test_path_traversal()
        test_duplicate_filename()
        test_directory_rejection()
        
        print("\n" + "=" * 50)
        print("All quarantine tests passed")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
