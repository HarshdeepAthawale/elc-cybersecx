"""
ELC Secure Network Configuration - Main Application
Encrypt/decrypt transaction data using Caesar, Playfair, and Hill ciphers.
Saves keys to file, measures encryption/decryption time.

Usage:
  python main.py              # Interactive menu
  python main.py --encrypt    # Run full encrypt + graphs, then exit
"""

import argparse
import sys
import time
from pathlib import Path

from cipher_module import (
    caesar_encrypt,
    caesar_decrypt,
    playfair_encrypt,
    playfair_decrypt,
    hill_encrypt,
    hill_decrypt,
)

# File paths (project root = parent of src/)
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PLAINTEXT_FILE = DATA_DIR / "plaintext.txt"
KEYS_FILE = DATA_DIR / "keys.txt"
CAESAR_CIPHER_FILE = DATA_DIR / "caesar_cipher.txt"
PLAYFAIR_CIPHER_FILE = DATA_DIR / "playfair_cipher.txt"
HILL_CIPHER_FILE = DATA_DIR / "hill_cipher.txt"

# Default keys (assignment examples)
DEFAULT_CAESAR_SHIFT = 3
DEFAULT_PLAYFAIR_KEYWORD = "MONARCHY"
DEFAULT_HILL_KEY = "GYBNQKURP"

# Timing iterations for averaging
TIMING_ITERATIONS = 5


def save_keys(caesar_shift: int, playfair_keyword: str, hill_key: str) -> None:
    """Save encryption keys to keys.txt."""
    with open(KEYS_FILE, "w") as f:
        f.write(f"CAESAR: {caesar_shift}\n")
        f.write(f"PLAYFAIR: {playfair_keyword}\n")
        f.write(f"HILL: {hill_key}\n")
    print(f"Keys saved to {KEYS_FILE}")


def load_keys() -> tuple[int, str, str]:
    """Load keys from keys.txt. Raises FileNotFoundError if not found."""
    if not KEYS_FILE.exists():
        raise FileNotFoundError(f"{KEYS_FILE} not found. Run encrypt first or enter keys.")
    data = {}
    with open(KEYS_FILE) as f:
        for line in f:
            line = line.strip()
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()

    caesar = int(data.get("CAESAR", DEFAULT_CAESAR_SHIFT))
    playfair = data.get("PLAYFAIR", DEFAULT_PLAYFAIR_KEYWORD)
    hill = data.get("HILL", DEFAULT_HILL_KEY)
    return caesar, playfair, hill


def get_keys_from_user() -> tuple[int, str, str]:
    """Prompt user for keys or use saved/default."""
    if KEYS_FILE.exists():
        use = input("Use saved keys from keys.txt? (y/n) [y]: ").strip().lower() or "y"
        if use == "y":
            return load_keys()

    print("Enter encryption keys (press Enter for default):")
    caesar_in = input(f"  Caesar shift [default: {DEFAULT_CAESAR_SHIFT}]: ").strip()
    playfair_in = input(f"  Playfair keyword [default: {DEFAULT_PLAYFAIR_KEYWORD}]: ").strip()
    hill_in = input(f"  Hill key (9 letters for 3x3) [default: {DEFAULT_HILL_KEY}]: ").strip()

    caesar = int(caesar_in) if caesar_in else DEFAULT_CAESAR_SHIFT
    playfair = playfair_in or DEFAULT_PLAYFAIR_KEYWORD
    hill = hill_in or DEFAULT_HILL_KEY

    return caesar, playfair, hill


def read_plaintext() -> str:
    """Read plaintext from file."""
    if not PLAINTEXT_FILE.exists():
        raise FileNotFoundError(
            f"{PLAINTEXT_FILE} not found. Copy Text_To_Be_Encypted.txt to plaintext.txt"
        )
    return PLAINTEXT_FILE.read_text(encoding="utf-8")


def run_encrypt() -> dict[str, dict[str, float]]:
    """Encrypt plaintext with all three ciphers and measure timing."""
    plaintext = read_plaintext()
    caesar_shift, playfair_keyword, hill_key = get_keys_from_user()
    save_keys(caesar_shift, playfair_keyword, hill_key)

    print("\n--- Encryption Keys ---")
    print(f"  Caesar shift: {caesar_shift}")
    print(f"  Playfair keyword: {playfair_keyword}")
    print(f"  Hill key: {hill_key}\n")

    timings: dict[str, dict[str, float]] = {
        "Caesar": {"encrypt": 0.0, "decrypt": 0.0},
        "Playfair": {"encrypt": 0.0, "decrypt": 0.0},
        "Hill": {"encrypt": 0.0, "decrypt": 0.0},
    }

    # Caesar
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        caesar_ct = caesar_encrypt(plaintext, caesar_shift)
    timings["Caesar"]["encrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
    CAESAR_CIPHER_FILE.write_text(caesar_ct, encoding="utf-8")
    print(f"Caesar ciphertext saved to {CAESAR_CIPHER_FILE}")

    # Playfair
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        playfair_ct = playfair_encrypt(plaintext, playfair_keyword)
    timings["Playfair"]["encrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
    PLAYFAIR_CIPHER_FILE.write_text(playfair_ct, encoding="utf-8")
    print(f"Playfair ciphertext saved to {PLAYFAIR_CIPHER_FILE}")

    # Hill
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        hill_ct = hill_encrypt(plaintext, hill_key)
    timings["Hill"]["encrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
    HILL_CIPHER_FILE.write_text(hill_ct, encoding="utf-8")
    print(f"Hill ciphertext saved to {HILL_CIPHER_FILE}")

    # Decryption timing
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        caesar_decrypt(caesar_ct, caesar_shift)
    timings["Caesar"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000

    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        playfair_decrypt(playfair_ct, playfair_keyword)
    timings["Playfair"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000

    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        hill_decrypt(hill_ct, hill_key)
    timings["Hill"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000

    return timings


def run_decrypt() -> dict[str, dict[str, float]]:
    """Decrypt ciphertexts and verify. Returns timings."""
    caesar_shift, playfair_keyword, hill_key = load_keys()

    timings: dict[str, dict[str, float]] = {
        "Caesar": {"encrypt": 0.0, "decrypt": 0.0},
        "Playfair": {"encrypt": 0.0, "decrypt": 0.0},
        "Hill": {"encrypt": 0.0, "decrypt": 0.0},
    }

    # Caesar
    ct = CAESAR_CIPHER_FILE.read_text(encoding="utf-8")
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        pt = caesar_decrypt(ct, caesar_shift)
    timings["Caesar"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
    print(f"Caesar decryption OK (len={len(pt)})")

    # Playfair
    ct = PLAYFAIR_CIPHER_FILE.read_text(encoding="utf-8")
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        pt = playfair_decrypt(ct, playfair_keyword)
    timings["Playfair"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
    print(f"Playfair decryption OK (len={len(pt)})")

    # Hill
    ct = HILL_CIPHER_FILE.read_text(encoding="utf-8")
    start = time.perf_counter()
    for _ in range(TIMING_ITERATIONS):
        pt = hill_decrypt(ct, hill_key)
    timings["Hill"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
    print(f"Hill decryption OK (len={len(pt)})")

    return timings


def print_timings(timings: dict[str, dict[str, float]]) -> None:
    """Print timing results in a table."""
    print("\n--- Timing Results (ms, averaged over {} runs) ---".format(TIMING_ITERATIONS))
    print(f"{'Algorithm':<12} {'Encrypt (ms)':<14} {'Decrypt (ms)':<14}")
    print("-" * 40)
    for name, t in timings.items():
        print(f"{name:<12} {t['encrypt']:<14.4f} {t['decrypt']:<14.4f}")

    enc_fastest = min(timings.items(), key=lambda x: x[1]["encrypt"])
    dec_fastest = min(timings.items(), key=lambda x: x[1]["decrypt"])
    print(f"\nFastest encryption: {enc_fastest[0]}")
    print(f"Fastest decryption: {dec_fastest[0]}")


def main() -> None:
    print("=" * 50)
    print("ELC Secure Network Configuration")
    print("Encryption / Decryption Module")
    print("=" * 50)

    while True:
        print("\n1. Encrypt (plaintext.txt -> cipher files)")
        print("2. Decrypt (cipher files -> verify)")
        print("3. Run full encrypt + timing + graphs")
        print("4. Exit")
        choice = input("Choice [1]: ").strip() or "1"

        if choice == "1":
            timings = run_encrypt()
            print_timings(timings)
        elif choice == "2":
            timings = run_decrypt()
            print_timings(timings)
        elif choice == "3":
            timings = run_encrypt()
            print_timings(timings)
            # Generate graphs
            try:
                from timing_results import generate_graphs
                generate_graphs(timings)
            except ImportError:
                print("Run: pip install matplotlib numpy  (for graphs)")
        elif choice == "4":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--encrypt", action="store_true", help="Run full encrypt + graphs (non-interactive)")
    args = parser.parse_args()

    if args.encrypt:
        # Non-interactive: use default keys, run full encrypt and graphs
        plaintext = read_plaintext()
        save_keys(DEFAULT_CAESAR_SHIFT, DEFAULT_PLAYFAIR_KEYWORD, DEFAULT_HILL_KEY)
        print("--- Encryption Keys ---")
        print(f"  Caesar shift: {DEFAULT_CAESAR_SHIFT}")
        print(f"  Playfair keyword: {DEFAULT_PLAYFAIR_KEYWORD}")
        print(f"  Hill key: {DEFAULT_HILL_KEY}\n")
        timings = {
            "Caesar": {"encrypt": 0.0, "decrypt": 0.0},
            "Playfair": {"encrypt": 0.0, "decrypt": 0.0},
            "Hill": {"encrypt": 0.0, "decrypt": 0.0},
        }
        # Encrypt and time
        start = time.perf_counter()
        for _ in range(TIMING_ITERATIONS):
            ct = caesar_encrypt(plaintext, DEFAULT_CAESAR_SHIFT)
        timings["Caesar"]["encrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
        CAESAR_CIPHER_FILE.write_text(ct, encoding="utf-8")
        start = time.perf_counter()
        for _ in range(TIMING_ITERATIONS):
            ct = playfair_encrypt(plaintext, DEFAULT_PLAYFAIR_KEYWORD)
        timings["Playfair"]["encrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
        PLAYFAIR_CIPHER_FILE.write_text(ct, encoding="utf-8")
        start = time.perf_counter()
        for _ in range(TIMING_ITERATIONS):
            ct = hill_encrypt(plaintext, DEFAULT_HILL_KEY)
        timings["Hill"]["encrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
        HILL_CIPHER_FILE.write_text(ct, encoding="utf-8")
        # Decrypt timing
        ct_c = CAESAR_CIPHER_FILE.read_text()
        start = time.perf_counter()
        for _ in range(TIMING_ITERATIONS):
            caesar_decrypt(ct_c, DEFAULT_CAESAR_SHIFT)
        timings["Caesar"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
        ct_p = PLAYFAIR_CIPHER_FILE.read_text()
        start = time.perf_counter()
        for _ in range(TIMING_ITERATIONS):
            playfair_decrypt(ct_p, DEFAULT_PLAYFAIR_KEYWORD)
        timings["Playfair"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
        ct_h = HILL_CIPHER_FILE.read_text()
        start = time.perf_counter()
        for _ in range(TIMING_ITERATIONS):
            hill_decrypt(ct_h, DEFAULT_HILL_KEY)
        timings["Hill"]["decrypt"] = (time.perf_counter() - start) / TIMING_ITERATIONS * 1000
        print_timings(timings)
        from timing_results import generate_graphs
        generate_graphs(timings)
        sys.exit(0)
    main()
