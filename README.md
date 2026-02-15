# ELC Secure Network Configuration - Encryption Module

Symmetric encryption module implementing **Caesar**, **Playfair**, and **Hill** ciphers for transaction data.

## Setup

```bash
cd "Secure Network Configuration ELC Assignment"
pip install -r requirements.txt
```

Ensure `plaintext.txt` exists (copy from `Text_To_Be_Encypted.txt` if needed).

## Usage

```bash
# Interactive menu
python main.py

# One-shot encrypt + graphs (uses default keys)
python main.py --encrypt
```

**Menu options:**
1. **Encrypt** – Read `plaintext.txt`, encrypt with all three ciphers, save to `*_cipher.txt`, save keys to `keys.txt`
2. **Decrypt** – Load cipher files and keys, decrypt and verify
3. **Run full** – Encrypt + generate timing graphs (`encryption_time.png`, `decryption_time.png`)
4. **Exit**

## Default Keys

| Algorithm | Key |
|-----------|-----|
| Caesar | 3 |
| Playfair | MONARCHY |
| Hill | GYBNQKURP (3×3) |

## Output Files

- `keys.txt` – Saved encryption keys
- `caesar_cipher.txt`, `playfair_cipher.txt`, `hill_cipher.txt` – Ciphertexts
- `encryption_time.png`, `decryption_time.png` – Timing graphs (for PDF)

## Submission

- **Deadline:** February 22, 2026, 11:59 PM
- **Format:** `{roll_number}.zip` containing:
  - PDF (codes, keys, ciphertexts, graphs, analysis)
  - ~90-second video (face visible, explaining code)
