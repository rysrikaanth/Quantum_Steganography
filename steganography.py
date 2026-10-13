"""
Quantum Steganography Implementation
Uses BB84-generated keys for secure message embedding
"""

from typing import List, Tuple
from utils import text_to_binary, binary_to_text, bits_to_string
import random

class QuantumSteganography:
    """
    Steganography system using quantum-generated keys.
    
    Hides secret messages in cover text using positions determined
    by a quantum key from BB84 protocol.
    """
    
    def __init__(self, quantum_key: List[int]):
        """
        Initialize with a quantum-generated key.
        
        Args:
            quantum_key: Shared key from BB84 protocol
        """
        self.quantum_key = quantum_key
        self.key_string = bits_to_string(quantum_key)
    
    def generate_embedding_positions(self, num_positions: int, 
                                    max_position: int) -> List[int]:
        """
        Generate pseudo-random positions for embedding using quantum key.
        
        Args:
            num_positions: Number of positions to generate
            max_position: Maximum position value (exclusive)
            
        Returns:
            List of positions where message bits will be embedded
        """
        # Use quantum key as seed for deterministic pseudo-random positions
        seed = int(self.key_string[:min(len(self.key_string), 31)], 2) if self.key_string else 42
        rng = random.Random(seed)
        
        # Generate positions ensuring no duplicates
        if num_positions > max_position:
            raise ValueError(f"Need {num_positions} positions but only {max_position} available.")
        
        positions = rng.sample(range(max_position), num_positions)
        return sorted(positions)
    
    def embed_message(self, cover_text: str, secret_message: str) -> str:
        """
        Embed secret message into cover text using quantum key.
        
        Simple character-based embedding where we XOR message characters
        with cover characters at quantum-determined positions.
        
        Args:
            cover_text: Innocent-looking cover text
            secret_message: Secret message to hide
            
        Returns:
            Stego-text with embedded message (as hex string for safety)
        """
        # Check capacity
        if len(secret_message) > len(cover_text) - 2:
            raise ValueError(f"Message too long! Maximum {len(cover_text)-2} characters, got {len(secret_message)}")
        
        # Convert to list for modification
        cover_chars = list(cover_text)
        
        # Store message length in first 2 positions (can handle up to 65535 chars)
        msg_len = len(secret_message)
        length_positions = self.generate_embedding_positions(2, len(cover_chars))
        
        # Encode length into first 2 positions
        cover_chars[length_positions[0]] = chr(ord(cover_chars[length_positions[0]]) ^ (msg_len >> 8))
        cover_chars[length_positions[1]] = chr(ord(cover_chars[length_positions[1]]) ^ (msg_len & 0xFF))
        
        # Generate positions for message (excluding length positions)
        available_positions = [i for i in range(len(cover_chars)) if i not in length_positions]
        msg_positions = self.generate_embedding_positions(msg_len, len(available_positions))
        actual_positions = [available_positions[i] for i in msg_positions]
        
        # Embed message using XOR
        for i, pos in enumerate(actual_positions):
            cover_chars[pos] = chr(ord(cover_chars[pos]) ^ ord(secret_message[i]))
        
        # Convert to hex string for safe transport
        stego_text = ''.join(cover_chars)
        hex_stego = stego_text.encode('utf-8', errors='replace').hex()
        
        return hex_stego
    
    def extract_message(self, hex_stego: str) -> str:
        """
        Extract hidden message from stego-text using quantum key.
        
        Args:
            hex_stego: Hex-encoded stego-text
            
        Returns:
            Extracted secret message
        """
        # Decode from hex
        stego_bytes = bytes.fromhex(hex_stego)
        stego_text = stego_bytes.decode('utf-8', errors='replace')
        stego_chars = list(stego_text)
        
        # Extract length from first 2 positions
        length_positions = self.generate_embedding_positions(2, len(stego_chars))
        
        high_byte = ord(stego_chars[length_positions[0]])
        low_byte = ord(stego_chars[length_positions[1]])
        
        # We need the original cover characters to XOR back
        # For this demo, we'll use a simpler approach with the quantum key directly
        
        # Generate positions for message
        available_positions = [i for i in range(len(stego_chars)) if i not in length_positions]
        
        # Try to extract reasonable length (brute force small lengths for demo)
        # In real system, sender would transmit length separately or use fixed protocol
        # For now, we'll embed differently...
        
        raise NotImplementedError("This approach needs the original cover text")
    
    def calculate_embedding_capacity(self, cover_text: str) -> int:
        """
        Calculate how many characters can be hidden in the cover text.
        
        Args:
            cover_text: The cover text
            
        Returns:
            Maximum number of characters that can be hidden
        """
        return len(cover_text) - 2  # Reserve 2 for length encoding


class QuantumSteganographySystem:
    """
    Complete quantum steganography system combining BB84 and steganography.
    
    Simplified version: Stores cover text to enable proper extraction.
    """
    
    def __init__(self, key_length: int = 128):
        """
        Initialize the system.
        
        Args:
            key_length: Length of quantum key to generate
        """
        self.key_length = key_length
        self.quantum_key = None
        self.stego = None
        self.cover_text = None  # Store cover text for extraction
    
    def setup_quantum_channel(self, verbose: bool = True) -> float:
        """
        Establish quantum key distribution using BB84.
        
        Args:
            verbose: Whether to print progress
            
        Returns:
            Error rate from BB84 protocol
        """
        from bb84 import BB84
        
        if verbose:
            print("\n" + "="*60)
            print("  QUANTUM CHANNEL SETUP")
            print("="*60)
            print("\nEstablishing quantum key distribution...")
        
        bb84 = BB84(key_length=self.key_length)
        self.quantum_key, error_rate = bb84.generate_shared_key(verbose=verbose)
        
        if error_rate < 5:
            if verbose:
                print("\n✓ Quantum channel established successfully!")
                print(f"✓ Shared key generated ({len(self.quantum_key)} bits)")
        else:
            if verbose:
                print("\n⚠ Warning: High error rate detected!")
                print("  Quantum channel may be compromised.")
        
        self.stego = QuantumSteganography(self.quantum_key)
        
        return error_rate
    
    def send_secret_message(self, cover_text: str, secret_message: str, 
                           verbose: bool = True) -> str:
        """
        Send a secret message hidden in cover text.
        
        Args:
            cover_text: Innocent-looking cover text
            secret_message: Secret message to hide
            verbose: Whether to print progress
            
        Returns:
            Hex-encoded stego-text with embedded message
        """
        if self.stego is None:
            raise RuntimeError("Quantum channel not established. Call setup_quantum_channel() first.")
        
        self.cover_text = cover_text  # Store for extraction
        
        if verbose:
            print("\n" + "="*60)
            print("  MESSAGE EMBEDDING")
            print("="*60)
            print(f"\nCover text length: {len(cover_text)} characters")
            print(f"Secret message length: {len(secret_message)} characters")
            print(f"Embedding capacity: {self.stego.calculate_embedding_capacity(cover_text)} characters")
        
        # Check capacity
        capacity = self.stego.calculate_embedding_capacity(cover_text)
        if len(secret_message) > capacity:
            raise ValueError(f"Message too long! Maximum {capacity} characters, got {len(secret_message)}")
        
        if verbose:
            print("\nEmbedding message using quantum key...")
        
        # Use simpler XOR-based embedding
        cover_chars = list(cover_text)
        msg_len = len(secret_message)
        
        # Generate positions using quantum key
        positions = self.stego.generate_embedding_positions(msg_len, len(cover_chars))
        
        # XOR message into cover at determined positions
        for i, pos in enumerate(positions):
            cover_chars[pos] = chr(ord(cover_chars[pos]) ^ ord(secret_message[i]))
        
        stego_text = ''.join(cover_chars)
        
        if verbose:
            print(f"\n✓ Message embedded successfully!")
            print(f"  - Positions used: {msg_len}")
            print(f"  - Capacity used: {(msg_len/capacity)*100:.1f}%")
            print(f"  - Stego-text (first 60 chars): {repr(stego_text[:60])}...")
        
        return stego_text
    
    def receive_secret_message(self, stego_text: str, message_length: int, verbose: bool = True) -> str:
        """
        Receive and extract secret message from stego-text.
        
        Args:
            stego_text: Text containing hidden message
            message_length: Length of hidden message (must be known)
            verbose: Whether to print progress
            
        Returns:
            Extracted secret message
        """
        if self.stego is None:
            raise RuntimeError("Quantum channel not established. Call setup_quantum_channel() first.")
        
        if self.cover_text is None:
            raise RuntimeError("Cover text not available. Need original cover for XOR extraction.")
        
        if verbose:
            print("\n" + "="*60)
            print("  MESSAGE EXTRACTION")
            print("="*60)
            print("\nExtracting hidden message using quantum key...")
        
        # Generate same positions using quantum key
        positions = self.stego.generate_embedding_positions(message_length, len(stego_text))
        
        # XOR stego with cover at determined positions to extract message
        message_chars = []
        for pos in positions:
            # XOR stego character with original cover character
            extracted_char = chr(ord(stego_text[pos]) ^ ord(self.cover_text[pos]))
            message_chars.append(extracted_char)
        
        secret_message = ''.join(message_chars)
        
        if verbose:
            print(f"\n✓ Message extracted successfully!")
            print(f"  - Message length: {len(secret_message)} characters")
        
        return secret_message



