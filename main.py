"""
Quantum Steganography - Main Application
Interactive CLI for quantum steganography demonstration
"""

from steganography import QuantumSteganographySystem
from utils import print_section, print_success, print_info, print_warning
import sys

class QuantumSteganographyApp:
    """Interactive application for quantum steganography."""
    
    def __init__(self):
        self.system = None
        self.stego_text = None
        self.message_length = None
    
    def display_banner(self):
        """Display application banner."""
        print("\n" + "="*70)
        print(" " * 15 + "QUANTUM STEGANOGRAPHY SYSTEM")
        print(" " * 10 + "Secure Message Hiding using Quantum Cryptography")
        print("="*70)
        print("\n  Powered by BB84 Quantum Key Distribution Protocol")
        print("="*70 + "\n")
    
    def display_menu(self):
        """Display main menu."""
        print("\n" + "-"*70)
        print("MAIN MENU")
        print("-"*70)
        print("1. Setup Quantum Channel (Required First)")
        print("2. Hide Secret Message")
        print("3. Extract Secret Message")
        print("4. Run Demo")
        print("5. View Statistics")
        print("6. About Quantum Steganography")
        print("7. Exit")
        print("-"*70)
    
    def setup_quantum_channel(self):
        """Initialize quantum key distribution."""
        print_section("Setting Up Quantum Channel")
        
        try:
            # Get key length from user
            print("\nQuantum Key Length Options:")
            print("  1. 64 bits  (Fast, less secure)")
            print("  2. 128 bits (Balanced) [Recommended]")
            print("  3. 256 bits (Slower, more secure)")
            
            choice = input("\nSelect key length (1-3) [default: 2]: ").strip()
            
            key_lengths = {
                '1': 64,
                '2': 128,
                '3': 256,
                '': 128  # Default
            }
            
            key_length = key_lengths.get(choice, 128)
            
            self.system = QuantumSteganographySystem(key_length=key_length)
            error_rate = self.system.setup_quantum_channel(verbose=True)
            
            if error_rate < 5:
                print_success("\n✓ Quantum channel ready for secure communication!")
            else:
                print_warning(f"\n⚠ Warning: High error rate ({error_rate:.2f}%)")
                print_warning("  The channel may be compromised. Proceed with caution.")
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\n❌ Error setting up quantum channel: {e}")
            input("\nPress Enter to continue...")
    
    def hide_message(self):
        """Hide a secret message in cover text."""
        if self.system is None:
            print_warning("\n⚠ Please setup quantum channel first (Option 1)")
            input("\nPress Enter to continue...")
            return
        
        print_section("Hide Secret Message")
        
        try:
            # Get cover text
            print("\n[STEP 1] Enter Cover Text")
            print("This is the innocent-looking text that will hide your message.")
            print("(Minimum 50 characters recommended)\n")
            
            use_sample = input("Use sample cover text? (y/n) [default: y]: ").strip().lower()
            
            if use_sample in ['', 'y', 'yes']:
                cover_text = """Quantum computing represents a revolutionary approach to information processing. 
By leveraging quantum mechanical phenomena such as superposition and entanglement, quantum computers 
can solve certain problems exponentially faster than classical computers. This technology has profound 
implications for cryptography, optimization, and scientific simulation."""
                print(f"\nUsing sample cover text ({len(cover_text)} characters)")
            else:
                print("\nEnter your cover text (end with empty line):")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                cover_text = " ".join(lines)
            
            if len(cover_text) < 20:
                print_warning("\n⚠ Cover text too short! Need at least 20 characters.")
                input("\nPress Enter to continue...")
                return
            
            # Show capacity
            capacity = self.system.stego.calculate_embedding_capacity(cover_text)
            print(f"\n✓ Cover text length: {len(cover_text)} characters")
            print(f"✓ Maximum message capacity: {capacity} characters")
            
            # Get secret message
            print("\n[STEP 2] Enter Secret Message")
            print(f"(Maximum {capacity} characters)\n")
            
            secret_message = input("Secret message: ").strip()
            
            if not secret_message:
                print_warning("\n⚠ Secret message cannot be empty!")
                input("\nPress Enter to continue...")
                return
            
            if len(secret_message) > capacity:
                print_warning(f"\n⚠ Message too long! Maximum {capacity} characters.")
                input("\nPress Enter to continue...")
                return
            
            # Embed message
            print("\n[STEP 3] Embedding Message...")
            self.stego_text = self.system.send_secret_message(cover_text, secret_message, verbose=True)
            self.message_length = len(secret_message)
            
            # Display result
            print("\n" + "="*70)
            print("STEGO-TEXT (Send this to receiver)")
            print("="*70)
            print(f"\n{self.stego_text}\n")
            print("="*70)
            
            # Option to save
            save = input("\nSave stego-text to file? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                filename = input("Enter filename [default: stego.txt]: ").strip() or "stego.txt"
                try:
                    with open(filename, 'w') as f:
                        f.write(f"# Quantum Steganography Output\n")
                        f.write(f"# Message Length: {self.message_length}\n")
                        f.write(f"# Stego-Text:\n\n")
                        f.write(self.stego_text)
                    print_success(f"\n✓ Saved to {filename}")
                except Exception as e:
                    print(f"\n❌ Error saving file: {e}")
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\n❌ Error hiding message: {e}")
            input("\nPress Enter to continue...")
    
    def extract_message(self):
        """Extract hidden message from stego-text."""
        if self.system is None:
            print_warning("\n⚠ Please setup quantum channel first (Option 1)")
            input("\nPress Enter to continue...")
            return
        
        print_section("Extract Secret Message")
        
        try:
            # Get stego-text
            print("\n[STEP 1] Provide Stego-Text")
            
            if self.stego_text:
                use_current = input("Use stego-text from previous hide operation? (y/n) [default: y]: ").strip().lower()
                if use_current in ['', 'y', 'yes']:
                    stego_text = self.stego_text
                    message_length = self.message_length
                    print(f"\n✓ Using current stego-text")
                else:
                    stego_text = input("\nEnter stego-text: ").strip()
                    message_length = int(input("Enter message length: ").strip())
            else:
                print("\nYou can:")
                print("  1. Paste stego-text directly")
                print("  2. Load from file")
                
                choice = input("\nChoice (1-2): ").strip()
                
                if choice == '2':
                    filename = input("Enter filename: ").strip()
                    try:
                        with open(filename, 'r') as f:
                            lines = f.readlines()
                            # Extract message length from comment
                            for line in lines:
                                if line.startswith('# Message Length:'):
                                    message_length = int(line.split(':')[1].strip())
                            # Get stego-text (skip comments)
                            stego_text = ''.join([l for l in lines if not l.startswith('#')]).strip()
                        print_success(f"\n✓ Loaded from {filename}")
                    except Exception as e:
                        print(f"\n❌ Error loading file: {e}")
                        input("\nPress Enter to continue...")
                        return
                else:
                    stego_text = input("\nEnter stego-text: ").strip()
                    message_length = int(input("Enter message length: ").strip())
            
            if not stego_text:
                print_warning("\n⚠ Stego-text cannot be empty!")
                input("\nPress Enter to continue...")
                return
            
            # Extract message
            print("\n[STEP 2] Extracting Message...")
            extracted = self.system.receive_secret_message(stego_text, message_length, verbose=True)
            
            # Display result
            print("\n" + "="*70)
            print("EXTRACTED SECRET MESSAGE")
            print("="*70)
            print(f"\n  \"{extracted}\"\n")
            print("="*70)
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\n❌ Error extracting message: {e}")
            import traceback
            traceback.print_exc()
            input("\nPress Enter to continue...")
    
    def run_demo(self):
        """Run automated demonstration."""
        print_section("Quantum Steganography Demo")
        
        print("\nThis demo will:")
        print("  1. Establish quantum key using BB84")
        print("  2. Hide a secret message")
        print("  3. Extract the message")
        print("  4. Show that different keys fail\n")
        
        input("Press Enter to start demo...")
        
        try:
            # Demo 1: Successful communication
            print_section("Demo 1: Successful Secure Communication")
            
            system = QuantumSteganographySystem(key_length=128)
            system.setup_quantum_channel(verbose=True)
            
            cover = "The weather today is quite pleasant with clear blue skies. Perfect for outdoor activities and enjoying nature."
            secret = "Attack at dawn"
            
            print_info(f"\nCover text: \"{cover}\"")
            print_info(f"Secret message: \"{secret}\"")
            
            stego = system.send_secret_message(cover, secret, verbose=True)
            extracted = system.receive_secret_message(stego, len(secret), verbose=True)
            
            print_info(f"\nExtracted: \"{extracted}\"")
            
            if extracted == secret:
                print_success("\n✓ Demo 1 PASSED: Secure communication successful!")
            
            input("\nPress Enter for Demo 2...")
            
            # Demo 2: Security demonstration
            print_section("Demo 2: Security - Wrong Quantum Key")
            
            print("\nAlice and Bob establish quantum key...")
            system1 = QuantumSteganographySystem(key_length=128)
            system1.setup_quantum_channel(verbose=False)
            
            stego1 = system1.send_secret_message(cover, secret, verbose=False)
            print_success("✓ Alice sends stego-text")
            
            print("\nEve tries to extract with different quantum key...")
            system2 = QuantumSteganographySystem(key_length=128)
            system2.setup_quantum_channel(verbose=False)
            
            try:
                wrong_extract = system2.receive_secret_message(stego1, len(secret), verbose=False)
                print_info(f"Eve's extraction: \"{wrong_extract}\"")
                
                if wrong_extract != secret:
                    print_success("\n✓ Security verified: Wrong key produces garbage!")
                    print(f"  Original message: \"{secret}\"")
                    print(f"  Eve's result: \"{wrong_extract}\"")
            except:
                print_success("\n✓ Security verified: Wrong key causes extraction failure!")
            
            print("\n" + "="*70)
            print_success("  ✓ DEMO COMPLETE!")
            print("="*70)
            
            input("\nPress Enter to continue...")
            
        except Exception as e:
            print(f"\n❌ Demo error: {e}")
            input("\nPress Enter to continue...")
    
    def view_statistics(self):
        """Display statistics about the system."""
        print_section("System Statistics & Information")
        
        if self.system is None:
            print_warning("\n⚠ Quantum channel not established yet")
            print("\nGeneral Information:")
        else:
            print("\nQuantum Channel Status:")
            print(f"  ✓ Established")
            print(f"  ✓ Key length: {len(self.system.quantum_key)} bits")
            print(f"  ✓ Key sample: {self.system.quantum_key[:16]}...")
        
        print("\nBB84 Protocol Information:")
        print("  - Uses quantum superposition and measurement")
        print("  - Detects eavesdropping through quantum mechanics")
        print("  - Typical sifting rate: ~50% of qubits")
        print("  - Secure error threshold: < 11%")
        
        print("\nSteganography Method:")
        print("  - XOR-based character embedding")
        print("  - Positions determined by quantum key")
        print("  - Deterministic for same key")
        print("  - Secure against wrong key extraction")
        
        print("\nSecurity Features:")
        print("  ✓ Quantum key distribution (provably secure)")
        print("  ✓ Eavesdropping detection")
        print("  ✓ Key-dependent embedding positions")
        print("  ✓ No encryption overhead (stealth)")
        
        input("\nPress Enter to continue...")
    
    def show_about(self):
        """Display information about quantum steganography."""
        print_section("About Quantum Steganography")
        
        print("""
WHAT IS QUANTUM STEGANOGRAPHY?

Quantum steganography combines two powerful concepts:

1. STEGANOGRAPHY - The art of hiding information within innocent-
   looking cover data. Unlike encryption (which is obvious), 
   steganography makes the message invisible.

2. QUANTUM CRYPTOGRAPHY - Uses quantum mechanics principles to 
   establish provably secure cryptographic keys. The BB84 protocol
   detects any eavesdropping through quantum state disturbance.

HOW THIS SYSTEM WORKS:

Step 1: Alice and Bob establish a shared secret key using the BB84
        quantum key distribution protocol.

Step 2: Alice uses the quantum key to determine pseudo-random 
        positions in her cover text.

Step 3: Alice embeds her secret message at these positions using
        XOR operations.

Step 4: Bob uses the same quantum key to determine the same 
        positions and extracts the message.

SECURITY:

- Without the quantum key, an attacker cannot know which positions
  contain the secret message
- Any attempt to intercept the quantum key exchange will be detected
- The stego-text looks like normal text with minor variations

APPLICATIONS:

- Covert military communications
- Corporate espionage protection
- Secure diplomatic channels
- Whistleblower protection
- Privacy-focused messaging
        """)
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main application loop."""
        self.display_banner()
        
        while True:
            try:
                self.display_menu()
                choice = input("\nSelect option (1-7): ").strip()
                
                if choice == '1':
                    self.setup_quantum_channel()
                elif choice == '2':
                    self.hide_message()
                elif choice == '3':
                    self.extract_message()
                elif choice == '4':
                    self.run_demo()
                elif choice == '5':
                    self.view_statistics()
                elif choice == '6':
                    self.show_about()
                elif choice == '7':
                    print("\n" + "="*70)
                    print("  Thank you for using Quantum Steganography System!")
                    print("="*70 + "\n")
                    sys.exit(0)
                else:
                    print_warning("\n⚠ Invalid option. Please select 1-7.")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("  Interrupted by user")
                print("="*70 + "\n")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")
                import traceback
                traceback.print_exc()
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = QuantumSteganographyApp()
    app.run()
