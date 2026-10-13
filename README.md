# Quantum Steganography with BB84 Quantum Key Distribution

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit 1.0+](https://img.shields.io/badge/qiskit-1.0+-6133B4.svg)](https://qiskit.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A quantum-cryptographic steganography system that combines the **BB84 Quantum Key Distribution (QKD)** protocol with information hiding. The system establishes unconditionally secure symmetric keys through simulated quantum channels and uses those keys to securely embed and extract hidden messages within cover text.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Theoretical Foundation](#theoretical-foundation)
  - [BB84 Protocol (Bennett & Brassard, 1984)](#bb84-protocol-bennett--brassard-1984)
  - [Eavesdropping Detection](#eavesdropping-detection)
  - [Quantum-Driven Steganography](#quantum-driven-steganography)
- [Project Architecture](#project-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
  - [Interactive CLI](#interactive-cli)
  - [Automated Demo Flow](#automated-demo-flow)
  - [Programmatic API](#programmatic-api)
- [Running the Test Suite](#running-the-test-suite)
- [Security Analysis](#security-analysis)
- [File Structure](#file-structure)
- [License](#license)

---

## Overview

Traditional steganography conceals the existence of secret information within ordinary carrier mediums (text, images, audio). However, classical key exchange mechanisms remain vulnerable to interception, cryptanalysis, and future quantum computing attacks (e.g., Shor's algorithm).

This project integrates:
1. **BB84 Quantum Key Distribution**: Leverages quantum superposition and measurement collapse to establish an identical, secret cryptographic key between Alice and Bob while detecting any eavesdropping attempt (Eve).
2. **Quantum Steganography**: Employs the quantum-negotiated key to deterministically select dispersed embedding positions within cover text and encrypt secret payloads via XOR transposition, making unauthorized extraction mathematically infeasible without the exact quantum key.

---

## Key Features

- **Qiskit-Powered Quantum Simulation**: Implements quantum circuits with Pauli-X and Hadamard gates for qubit state preparation and measurement.
- **Eavesdropper Detection**: Measures the Quantum Bit Error Rate (QBER). An intercepted channel naturally yields ~25% error rate when measured in incompatible bases, triggering instant eavesdropper detection.
- **Configurable Quantum Key Lengths**: Supports 64-bit, 128-bit, and 256-bit key generation with 4x oversampling and sifting.
- **Cover Text Steganography**: Conceals secret payloads inside normal text with minimal perceptual impact.
- **Interactive CLI & Automated Demonstration**: Clean command-line interface featuring step-by-step guidance, statistics, and full demo capabilities.
- **Comprehensive Unit & Integration Tests**: Ready-to-run test suites covering environment readiness, QKD physics, and steganographic fidelity.

---

## Theoretical Foundation

### BB84 Protocol (Bennett & Brassard, 1984)

The protocol operates over two channels: a **quantum channel** (for qubit transmission) and a **public classical channel** (for basis comparison):

1. **State Preparation (Alice)**:
   - Alice creates a random bit sequence $b \in \{0, 1\}$.
   - Alice selects random bases $B \in \{Z, X\}$:
     - **Computational basis ($Z$)**: $|0\rangle$ and $|1\rangle = X|0\rangle$
     - **Diagonal basis ($X$)**: $|+\rangle = H|0\rangle$ and $|-\rangle = H|1\rangle$
2. **Measurement (Bob)**:
   - Bob measures incoming qubits using randomly chosen bases ($Z$ or $X$).
3. **Key Sifting**:
   - Alice and Bob announce their measurement bases over the classical channel.
   - When their bases match, Bob's measurement is guaranteed to equal Alice's bit (theoretically 100% correlation). Mismatched bases are discarded (~50% retention).
4. **Error Estimation**:
   - A subset of sifted bits is compared to estimate the Quantum Bit Error Rate (QBER).
   - If QBER exceeds the security threshold ($< 5\%$), eavesdropping is flagged and the key is aborted.

### Eavesdropping Detection

By the **No-Cloning Theorem** and the **Heisenberg Uncertainty Principle**, Eve cannot measure a qubit in an unknown state without collapsing it:
- If Eve measures in the wrong basis (50% chance), she alters the state.
- Bob then measures Eve's altered qubit, introducing an expected error rate of **25%** across intercepted bits.
- Even with partial interception (e.g., 50% intercept rate), the error rate significantly exceeds normal channel noise ($> 10\%$).

### Quantum-Driven Steganography

1. **Position Generation**: The shared quantum key seeds a deterministic pseudorandom number generator (PRNG) that identifies dispersed indices in the cover text.
2. **Payload Embedding**: The secret characters are XOR-transformed with the carrier text at the quantum-determined positions.
3. **Extraction**: Only a receiver with the exact identical quantum key can reconstruct the valid indices and reverse the XOR operation.

---

## Project Architecture

```
                    +-----------------------------+
                    |  BB84 Protocol (bb84.py)    |
                    +-----------------------------+
                     /                           \
         Alice prepares qubits            Bob measures qubits
         (Random Bits + Bases)           (Random Bases)
                     \                           /
                      +-------------------------+
                      | Sifting & QBER Check    |
                      +-------------------------+
                                   |
                             Shared Key
                                   v
             +-------------------------------------------+
             | QuantumSteganography (steganography.py)   |
             +-------------------------------------------+
              /                                         \
    Sender (Alice):                           Receiver (Bob):
    - Seeds PRNG with Quantum Key             - Seeds PRNG with Quantum Key
    - Derives secret index positions          - Reconstructs secret index positions
    - XOR-embeds message into cover text      - XOR-extracts original secret message
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/rysrikaanth/Quantum_Steganography.git
cd Quantum_Steganography
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate    # On macOS / Linux
# or: .\venv\Scripts\activate  (Windows)
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Usage Guide

### Interactive CLI

Launch the interactive console application:
```bash
python main.py
```

Menu options:
```text
======================================================================
               QUANTUM STEGANOGRAPHY SYSTEM
          Secure Message Hiding using Quantum Cryptography
======================================================================

1. Setup Quantum Channel (Required First)
2. Hide Secret Message
3. Extract Secret Message
4. Run Demo
5. View Statistics
6. About Quantum Steganography
7. Exit
```

### Automated Demo Flow

To run the automated demonstration without manual input:
```bash
printf "4\n\n\n\n7\n" | python main.py
```

### Programmatic API

You can also integrate the quantum steganography modules into your own Python applications:

```python
from bb84 import BB84
from steganography import QuantumSteganographySystem

# 1. Initialize system with 128-bit key
system = QuantumSteganographySystem(key_length=128)

# 2. Establish quantum channel via BB84
error_rate = system.setup_quantum_channel(verbose=False)
print(f"Channel established with QBER: {error_rate:.2f}%")

# 3. Embed secret message into cover text
cover_text = "The weather today is pleasant with clear skies and bright sunshine."
secret_message = "Meet at dawn"

stego_text = system.send_secret_message(cover_text, secret_message, verbose=False)

# 4. Extract secret message on receiver side
extracted_msg = system.receive_secret_message(stego_text, len(secret_message), verbose=False)
print(f"Extracted Secret: {extracted_msg}")
assert extracted_msg == secret_message
```

---

## Running the Test Suite

The project includes unit and integration tests to validate each component:

### 1. Environment & Setup Test
Verifies Qiskit installation, single-qubit circuits, and primitive sampling:
```bash
python test_setup.py
```

### 2. BB84 Protocol Tests
Validates key generation, sifting efficiency, and eavesdropper detection:
```bash
python test_bb84.py
```

### 3. Quantum Steganography Tests
Tests message embedding, extraction accuracy, and cryptographic security against incorrect keys:
```bash
python test_steganography.py
```

---

## Security Analysis

| Threat Model | Classical Steganography | Quantum Steganography (This Project) |
|---|---|---|
| **Key Interception (Man-in-the-Middle)** | Vulnerable to passive sniffing | **Detected immediately** via QBER spike (>10%) |
| **Brute Force on Key** | Vulnerable if key size is small | **Protected** with configurable 128-bit / 256-bit keys |
| **Statistical Steganalysis** | Detectable if carrier statistics change | **High stealth**: character variations localized to quantum positions |
| **Unauthorized Extraction** | Recoverable if PRNG seed is guessed | **Fails**: wrong key produces pseudo-random corrupted strings |

---

## File Structure

```
Quantum_Steganography/
├── .gitignore             # Git ignore patterns for venv, caches, and system files
├── requirements.txt       # Project dependencies (qiskit, numpy, qiskit-aer)
├── README.md              # Project documentation and usage guide
├── bb84.py                # BB84 Quantum Key Distribution implementation
├── steganography.py       # Quantum steganography embedding & extraction engine
├── utils.py               # Bit manipulation, conversions, and UI helpers
├── main.py                # Interactive CLI application
├── test_setup.py          # Setup & Qiskit verification test
├── test_bb84.py           # BB84 protocol and eavesdropper simulation tests
└── test_steganography.py  # Steganography embedding, extraction & security tests
```

---

## License

This project is licensed under the [MIT License](LICENSE).
