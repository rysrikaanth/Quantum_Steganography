"""
Utility functions for Quantum Steganography
"""

import numpy as np
from typing import List

def text_to_binary(text: str) -> str:
    """
    Convert text to binary string.
    
    Args:
        text: Input text string
        
    Returns:
        Binary representation as string
    """
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary: str) -> str:
    """
    Convert binary string back to text.
    
    Args:
        binary: Binary string (length must be multiple of 8)
        
    Returns:
        Decoded text string
    """
    # Pad binary to make it multiple of 8
    padding = 8 - (len(binary) % 8) if len(binary) % 8 != 0 else 0
    binary = binary + '0' * padding
    
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text

def bits_to_string(bits: List[int]) -> str:
    """
    Convert list of bits to string.
    
    Args:
        bits: List of 0s and 1s
        
    Returns:
        String representation
    """
    return ''.join(str(bit) for bit in bits)

def string_to_bits(s: str) -> List[int]:
    """
    Convert string to list of bits.
    
    Args:
        s: String of 0s and 1s
        
    Returns:
        List of integers (0s and 1s)
    """
    return [int(bit) for bit in s]

def calculate_error_rate(bits1: List[int], bits2: List[int]) -> float:
    """
    Calculate error rate between two bit sequences.
    
    Args:
        bits1: First bit sequence
        bits2: Second bit sequence
        
    Returns:
        Error rate as percentage
    """
    if len(bits1) != len(bits2):
        min_len = min(len(bits1), len(bits2))
        bits1 = bits1[:min_len]
        bits2 = bits2[:min_len]
    
    errors = sum(b1 != b2 for b1, b2 in zip(bits1, bits2))
    return (errors / len(bits1)) * 100 if len(bits1) > 0 else 0

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_success(message: str):
    """Print success message."""
    print(f"✓ {message}")

def print_info(message: str):
    """Print info message."""
    print(f"ℹ {message}")

def print_warning(message: str):
    """Print warning message."""
    print(f"⚠ {message}")
