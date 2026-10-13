"""
BB84 Quantum Key Distribution Protocol Implementation
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from typing import List, Tuple
import random

class BB84:
    """
    Implementation of the BB84 Quantum Key Distribution protocol.
    
    The BB84 protocol allows two parties (Alice and Bob) to establish
    a shared secret key using quantum mechanics principles.
    """
    
    def __init__(self, key_length: int = 128):
        """
        Initialize BB84 protocol.
        
        Args:
            key_length: Desired length of the final shared key
        """
        self.key_length = key_length
        # We need more bits initially because some will be discarded
        self.num_qubits = key_length * 4  # Oversample for better key generation
        self.sampler = Sampler()
        
    def alice_prepare_qubits(self) -> Tuple[List[int], List[int]]:
        """
        Alice prepares qubits in random states using random bases.
        
        Returns:
            Tuple of (bits, bases)
            - bits: Random bit values (0 or 1) that Alice wants to send
            - bases: Random bases (0=computational Z, 1=diagonal X) used for encoding
        """
        # Alice generates random bits to encode
        alice_bits = [random.randint(0, 1) for _ in range(self.num_qubits)]
        
        # Alice chooses random bases for each bit
        # 0 = Computational basis (Z): |0⟩ or |1⟩
        # 1 = Diagonal basis (X): |+⟩ or |-⟩
        alice_bases = [random.randint(0, 1) for _ in range(self.num_qubits)]
        
        return alice_bits, alice_bases
    
    def encode_qubit(self, bit: int, basis: int) -> QuantumCircuit:
        """
        Encode a single bit into a qubit using specified basis.
        
        Args:
            bit: The bit value to encode (0 or 1)
            basis: The basis to use (0=Z computational, 1=X diagonal)
            
        Returns:
            Quantum circuit with encoded qubit
        """
        qc = QuantumCircuit(1, 1)
        
        # Encode the bit
        if bit == 1:
            qc.x(0)  # Apply X gate to flip |0⟩ to |1⟩
        
        # Apply basis transformation
        if basis == 1:  # Diagonal basis
            qc.h(0)  # Apply Hadamard to switch to X basis
        
        return qc
    
    def bob_measure_qubits(self, alice_bits: List[int], alice_bases: List[int]) -> Tuple[List[int], List[int]]:
        """
        Bob measures the qubits sent by Alice using random bases.
        
        Args:
            alice_bits: The bits Alice encoded
            alice_bases: The bases Alice used
            
        Returns:
            Tuple of (bob_results, bob_bases)
            - bob_results: Measurement results Bob obtained
            - bob_bases: Random bases Bob chose for measurement
        """
        # Bob chooses random bases for measurement
        bob_bases = [random.randint(0, 1) for _ in range(self.num_qubits)]
        bob_results = []
        
        for i in range(self.num_qubits):
            # Create quantum circuit with Alice's encoding
            qc = self.encode_qubit(alice_bits[i], alice_bases[i])
            
            # Bob applies his measurement basis
            if bob_bases[i] == 1:  # Diagonal basis
                qc.h(0)  # Apply Hadamard before measurement
            
            # Measure the qubit
            qc.measure(0, 0)
            
            # Run the circuit
            job = self.sampler.run(qc, shots=1)
            result = job.result()
            quasi_dist = result.quasi_dists[0]
            
            # Get measurement result (0 or 1)
            measured_bit = list(quasi_dist.keys())[0]
            bob_results.append(measured_bit)
        
        return bob_results, bob_bases
    
    def sift_key(self, alice_bits: List[int], alice_bases: List[int], 
                 bob_results: List[int], bob_bases: List[int]) -> Tuple[List[int], List[int]]:
        """
        Perform basis reconciliation and key sifting.
        
        Alice and Bob publicly compare their bases and keep only the bits
        where they used the same basis.
        
        Args:
            alice_bits: Alice's original bits
            alice_bases: Alice's bases
            bob_results: Bob's measurement results
            bob_bases: Bob's bases
            
        Returns:
            Tuple of (alice_key, bob_key) - the sifted keys
        """
        alice_key = []
        bob_key = []
        
        for i in range(self.num_qubits):
            # Keep bits only where Alice and Bob used the same basis
            if alice_bases[i] == bob_bases[i]:
                alice_key.append(alice_bits[i])
                bob_key.append(bob_results[i])
        
        return alice_key, bob_key
    
    def estimate_error_rate(self, alice_key: List[int], bob_key: List[int], 
                           sample_size: int = None) -> Tuple[float, List[int], List[int]]:
        """
        Estimate the error rate by comparing a sample of bits.
        
        This helps detect eavesdropping. A high error rate indicates
        someone may have intercepted the quantum channel.
        
        Args:
            alice_key: Alice's sifted key
            bob_key: Bob's sifted key
            sample_size: Number of bits to compare (default: 25% of key)
            
        Returns:
            Tuple of (error_rate, remaining_alice_key, remaining_bob_key)
        """
        if sample_size is None:
            sample_size = len(alice_key) // 4  # Use 25% for error checking
        
        # Randomly select bits for error checking
        total_bits = len(alice_key)
        check_indices = random.sample(range(total_bits), min(sample_size, total_bits))
        
        errors = 0
        for idx in check_indices:
            if alice_key[idx] != bob_key[idx]:
                errors += 1
        
        error_rate = (errors / len(check_indices)) * 100 if len(check_indices) > 0 else 0
        
        # Remove checked bits from the key
        remaining_alice_key = [alice_key[i] for i in range(total_bits) if i not in check_indices]
        remaining_bob_key = [bob_key[i] for i in range(total_bits) if i not in check_indices]
        
        return error_rate, remaining_alice_key, remaining_bob_key
    
    def generate_shared_key(self, verbose: bool = True) -> Tuple[List[int], float]:
        """
        Execute the complete BB84 protocol to generate a shared key.
        
        Args:
            verbose: Whether to print detailed progress information
            
        Returns:
            Tuple of (shared_key, error_rate)
        """
        if verbose:
            print("\n" + "="*60)
            print("  BB84 Quantum Key Distribution Protocol")
            print("="*60)
            print(f"\nTarget key length: {self.key_length} bits")
            print(f"Preparing {self.num_qubits} qubits...\n")
        
        # Step 1: Alice prepares qubits
        if verbose:
            print("Step 1: Alice prepares qubits in random bases...")
        alice_bits, alice_bases = self.alice_prepare_qubits()
        if verbose:
            print(f"  ✓ Alice prepared {len(alice_bits)} qubits")
        
        # Step 2: Bob measures qubits
        if verbose:
            print("\nStep 2: Bob measures qubits using random bases...")
        bob_results, bob_bases = self.bob_measure_qubits(alice_bits, alice_bases)
        if verbose:
            print(f"  ✓ Bob measured {len(bob_results)} qubits")
        
        # Step 3: Basis reconciliation (public channel)
        if verbose:
            print("\nStep 3: Alice and Bob compare bases (public)...")
        alice_key, bob_key = self.sift_key(alice_bits, alice_bases, bob_results, bob_bases)
        if verbose:
            print(f"  ✓ Sifted key length: {len(alice_key)} bits")
            print(f"  ✓ Kept ~{(len(alice_key)/self.num_qubits)*100:.1f}% of qubits")
        
        # Step 4: Error rate estimation
        if verbose:
            print("\nStep 4: Checking for eavesdropping...")
        error_rate, final_alice_key, final_bob_key = self.estimate_error_rate(alice_key, bob_key)
        if verbose:
            print(f"  ✓ Error rate: {error_rate:.2f}%")
            if error_rate < 5:
                print("  ✓ Error rate is acceptable (< 5%)")
            elif error_rate < 11:
                print("  ⚠ Error rate is moderate (5-11%)")
            else:
                print("  ⚠ High error rate detected! Possible eavesdropping!")
        
        # Step 5: Truncate to desired length
        shared_key = final_alice_key[:self.key_length]
        if verbose:
            print(f"\nStep 5: Final shared key generated")
            print(f"  ✓ Final key length: {len(shared_key)} bits")
            print(f"  ✓ Key (first 32 bits): {''.join(map(str, shared_key[:32]))}...")
        
        # Verify keys match
        if final_alice_key[:self.key_length] == final_bob_key[:self.key_length]:
            if verbose:
                print("\n✓ SUCCESS: Alice and Bob have matching keys!")
        else:
            if verbose:
                print("\n⚠ WARNING: Key mismatch detected!")
        
        if verbose:
            print("="*60 + "\n")
        
        return shared_key, error_rate
    
    def simulate_eavesdropping(self, alice_bits: List[int], alice_bases: List[int], 
                               intercept_rate: float = 0.5) -> Tuple[List[int], List[int]]:
        """
        Simulate an eavesdropper (Eve) intercepting qubits.
        
        Eve intercepts some qubits, measures them, and resends them to Bob.
        This introduces errors that can be detected.
        
        Args:
            alice_bits: Alice's original bits
            alice_bases: Alice's bases
            intercept_rate: Fraction of qubits Eve intercepts (0.0 to 1.0)
            
        Returns:
            Tuple of (modified_bits, eve_bases)
        """
        eve_bases = [random.randint(0, 1) for _ in range(self.num_qubits)]
        modified_bits = alice_bits.copy()
        
        for i in range(self.num_qubits):
            # Eve intercepts with given probability
            if random.random() < intercept_rate:
                # Eve measures with random basis
                qc = self.encode_qubit(alice_bits[i], alice_bases[i])
                
                if eve_bases[i] == 1:  # Eve's diagonal basis
                    qc.h(0)
                
                qc.measure(0, 0)
                
                # Eve's measurement
                job = self.sampler.run(qc, shots=1)
                result = job.result()
                quasi_dist = result.quasi_dists[0]
                eve_result = list(quasi_dist.keys())[0]
                
                # Eve resends the qubit (may be wrong if bases don't match)
                modified_bits[i] = eve_result
        
        return modified_bits, eve_bases
