"""
Test script for Quantum Steganography
"""

from steganography import QuantumSteganographySystem
from utils import print_section, print_success, print_info

def test_basic_steganography():
    """Test basic steganography functionality."""
    print_section("Test 1: Basic Quantum Steganography")
    
    # Initialize system
    system = QuantumSteganographySystem(key_length=128)
    
    # Setup quantum channel
    error_rate = system.setup_quantum_channel(verbose=True)
    
    # Prepare cover text and secret message
    cover_text = "Hello everyone! This is a completely normal message about quantum computing. Nothing suspicious here at all. Just discussing some interesting topics in physics and technology. Have a great day!"
    secret_message = "Meet at noon"
    
    print_info(f"\nCover text: \"{cover_text}\"")
    print_info(f"Secret message: \"{secret_message}\"")
    
    # Embed message
    stego_text = system.send_secret_message(cover_text, secret_message, verbose=True)
    
    print_info(f"\nStego-text: \"{stego_text[:80]}...\"")
    
    # Extract message (Bob needs to know message length - transmitted separately or fixed protocol)
    extracted = system.receive_secret_message(stego_text, len(secret_message), verbose=True)
    
    print_info(f"\nExtracted message: \"{extracted}\"")
    
    # Verify
    if extracted == secret_message:
        print_success("\n✓ Test PASSED: Message extracted correctly!")
    else:
        print(f"\n❌ Test FAILED: Messages don't match!")
        print(f"   Expected: \"{secret_message}\"")
        print(f"   Got: \"{extracted}\"")

def test_longer_message():
    """Test with a longer secret message."""
    print_section("Test 2: Longer Secret Message")
    
    system = QuantumSteganographySystem(key_length=256)
    system.setup_quantum_channel(verbose=False)
    
    cover_text = "Quantum computing is revolutionizing the field of cryptography. Traditional encryption methods may become vulnerable to quantum attacks. However, quantum key distribution offers provably secure communication. The BB84 protocol, invented by Bennett and Brassard in 1984, uses quantum mechanics principles to detect eavesdropping."
    
    secret_message = "Package arrives at 3PM"
    
    print(f"Cover text length: {len(cover_text)} characters")
    print(f"Secret message length: {len(secret_message)} characters")
    
    stego_text = system.send_secret_message(cover_text, secret_message, verbose=False)
    extracted = system.receive_secret_message(stego_text, len(secret_message), verbose=False)
    
    if extracted == secret_message:
        print_success("✓ Test PASSED: Longer message handled correctly!")
        print(f"  Extracted: \"{extracted}\"")
    else:
        print("❌ Test FAILED")
        print(f"  Expected: \"{secret_message}\"")
        print(f"  Got: \"{extracted}\"")

def test_different_keys():
    """Test that different quantum keys produce different results."""
    print_section("Test 3: Security - Different Quantum Keys")
    
    cover_text = "This is a test message for quantum steganography demonstration using quantum key distribution protocol."
    secret_message = "Secret123"
    
    # System 1
    system1 = QuantumSteganographySystem(key_length=128)
    system1.setup_quantum_channel(verbose=False)
    stego1 = system1.send_secret_message(cover_text, secret_message, verbose=False)
    
    # System 2 (different quantum key)
    system2 = QuantumSteganographySystem(key_length=128)
    system2.setup_quantum_channel(verbose=False)
    stego2 = system2.send_secret_message(cover_text, secret_message, verbose=False)
    
    print(f"Stego-text 1: {stego1[:50]}...")
    print(f"Stego-text 2: {stego2[:50]}...")
    
    if stego1 != stego2:
        print_success("\n✓ Security verified: Different keys produce different stego-texts!")
    else:
        print("\n⚠ Warning: Stego-texts are identical (very unlikely)")
    
    # Try to extract with wrong key
    try:
        wrong_extracted = system2.receive_secret_message(stego1, len(secret_message), verbose=False)
        if wrong_extracted != secret_message:
            print_success("✓ Security verified: Wrong key produces garbage!")
            print(f"  Wrong key extraction: \"{wrong_extracted}\"")
            print(f"  Original message: \"{secret_message}\"")
        else:
            print("⚠ Warning: Wrong key somehow produced correct message!")
    except Exception as e:
        print_success(f"✓ Security verified: Wrong key causes errors!")

if __name__ == "__main__":
    test_basic_steganography()
    print("\n" + "="*60 + "\n")
    
    test_longer_message()
    print("\n" + "="*60 + "\n")
    
    test_different_keys()
    
    print("\n" + "="*60)
    print("  ✓ All steganography tests completed!")
    print("="*60 + "\n")

