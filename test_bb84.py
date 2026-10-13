"""
Test script for BB84 protocol
"""

from bb84 import BB84
from utils import print_section, print_success, print_warning

def test_bb84_basic():
    """Test basic BB84 protocol without eavesdropping."""
    print_section("Test 1: Basic BB84 Protocol (No Eavesdropping)")
    
    bb84 = BB84(key_length=64)
    shared_key, error_rate = bb84.generate_shared_key(verbose=True)
    
    if error_rate < 5:
        print_success(f"Test passed! Error rate: {error_rate:.2f}%")
    else:
        print_warning(f"Unexpected error rate: {error_rate:.2f}%")

def test_bb84_with_eve():
    """Test BB84 protocol with simulated eavesdropping."""
    print_section("Test 2: BB84 Protocol WITH Eavesdropper (Eve)")
    
    bb84 = BB84(key_length=64)
    
    print("Simulating eavesdropper intercepting 50% of qubits...\n")
    
    # Alice prepares qubits
    alice_bits, alice_bases = bb84.alice_prepare_qubits()
    
    # Eve intercepts!
    modified_bits, eve_bases = bb84.simulate_eavesdropping(alice_bits, alice_bases, intercept_rate=0.5)
    
    # Bob measures (receiving Eve's modified qubits)
    bob_results, bob_bases = bb84.bob_measure_qubits(modified_bits, alice_bases)
    
    # Sift key
    alice_key, bob_key = bb84.sift_key(alice_bits, alice_bases, bob_results, bob_bases)
    
    # Check error rate
    error_rate, _, _ = bb84.estimate_error_rate(alice_key, bob_key)
    
    print(f"\n{'='*60}")
    print(f"  EAVESDROPPING DETECTION RESULTS")
    print(f"{'='*60}")
    print(f"Error rate with Eve: {error_rate:.2f}%")
    
    if error_rate > 10:
        print_success("✓ Eavesdropper DETECTED! (Error rate > 10%)")
        print("  The protocol successfully detected Eve's presence!")
    else:
        print_warning("⚠ Eavesdropper not clearly detected (low error rate)")
    
    print(f"{'='*60}\n")

def test_different_key_lengths():
    """Test BB84 with different key lengths."""
    print_section("Test 3: Different Key Lengths")
    
    key_lengths = [32, 64, 128]
    
    for length in key_lengths:
        print(f"\nGenerating {length}-bit key...")
        bb84 = BB84(key_length=length)
        shared_key, error_rate = bb84.generate_shared_key(verbose=False)
        
        print(f"  ✓ Generated {len(shared_key)}-bit key")
        print(f"  ✓ Error rate: {error_rate:.2f}%")
        print(f"  ✓ Key sample: {''.join(map(str, shared_key[:16]))}...")

if __name__ == "__main__":
    test_bb84_basic()
    print("\n" + "="*60 + "\n")
    
    test_bb84_with_eve()
    print("\n" + "="*60 + "\n")
    
    test_different_key_lengths()
    
    print("\n" + "="*60)
    print("  ✓ All BB84 tests completed!")
    print("="*60 + "\n")
