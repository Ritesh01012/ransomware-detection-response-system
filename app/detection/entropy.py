"""
Shannon entropy calculation for file analysis.
High entropy indicates encrypted or compressed data.
"""

import math
from collections import Counter


def calculate_entropy(file_path):
    """
    Calculate Shannon entropy of a file.
    
    Shannon entropy measures the randomness of data.
    Range: 0.0 (completely predictable) to 8.0 (completely random)
    
    Args:
        file_path: Path to the file to analyze
    
    Returns:
        entropy: Float value between 0.0 and 8.0
    
    Raises:
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
        IOError: If read operation fails
    """
    try:
        with open(file_path, "rb") as file:
            data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {e}")
    
    # Empty file has zero entropy
    if len(data) == 0:
        return 0.0
    
    # Count frequency of each byte value
    byte_counts = Counter(data)
    
    # Calculate entropy
    entropy = 0.0
    total_bytes = len(data)
    
    for count in byte_counts.values():
        probability = count / total_bytes
        entropy -= probability * math.log2(probability)
    
    return entropy


def is_high_entropy(entropy, threshold=7.0):
    """
    Check if entropy is above threshold.
    
    Args:
        entropy: Entropy value
        threshold: Threshold value (default 7.0)
    
    Returns:
        bool: True if entropy >= threshold
    """
    return entropy >= threshold


if __name__ == "__main__":
    # Test entropy calculation
    print("=" * 50)
    print("Entropy Calculation Test")
    print("=" * 50)
    
    # Test with a simple text file
    test_file = "sandbox/entropy_test.txt"
    
    try:
        with open(test_file, "w") as f:
            f.write("Hello, this is a simple test file.")
        
        entropy = calculate_entropy(test_file)
        print(f"\nFile: {test_file}")
        print(f"Entropy: {entropy:.4f}")
        print(f"High entropy: {is_high_entropy(entropy)}")
        
    except Exception as e:
        print(f"Error: {e}")
