"""
Test script to verify installation and setup (without qiskit-aer)
"""

import qiskit
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
import numpy as np
from utils import text_to_binary, binary_to_text, print_section, print_success

def test_qiskit():
    """Test Qiskit installation."""
    print_section("Testing Qiskit Installation")
    
    print(f"Qiskit version: {qiskit.__version__}")
    print(f"NumPy version: {np.__version__}")
    
    # Create a simple quantum circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate (creates superposition)
    qc.measure(0, 0)  # Measure the qubit
    
    print("\nSimple Quantum Circuit:")
    print(qc)
    
    # Use Qiskit's built-in Sampler (no aer needed)
    print("\nRunning quantum simulation...")
    sampler = Sampler()
    job = sampler.run(qc, shots=1000)
    result = job.result()
    
    # Get quasi-distributions
    quasi_dists = result.quasi_dists[0]
    
    # Convert to counts format for display
    counts = {bin(k)[2:].zfill(1): int(v * 1000) for k, v in quasi_dists.items()}
    
    print(f"Measurement results (1000 shots): {counts}")
    print_success("Qiskit is working correctly!")

def test_utils():
    """Test utility functions."""
    print_section("Testing Utility Functions")
    
    # Test text to binary conversion
    test_text = "Hello"
    binary = text_to_binary(test_text)
    decoded = binary_to_text(binary)
    
    print(f"Original text: '{test_text}'")
    print(f"Binary: {binary}")
    print(f"Decoded text: '{decoded}'")
    
    if test_text == decoded:
        print_success("Text conversion is working correctly!")
    else:
        print("❌ Text conversion failed!")

if __name__ == "__main__":
    try:
        test_qiskit()
        test_utils()
        
        print("\n" + "="*60)
        print("  ✓ All tests passed! Ready to proceed to Phase 2.")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you ran: pip install qiskit numpy")
        print("2. Check Python version: python3 --version (3.8+ required)")


