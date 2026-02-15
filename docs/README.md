# ELC Secure Network Configuration - Encryption Module

Symmetric encryption module implementing **Caesar**, **Playfair**, and **Hill** ciphers for transaction data.

## Project Structure

```
├── data/           # Text files (plaintext, keys, ciphertexts)
├── docs/           # Documentation (this README)
├── src/            # Python source code
├── assets/         # Generated graphs (PNG)
├── output/         # Generated PDF (submission.pdf)
├── run.py          # Entry point (run from project root)
└── requirements.txt
```

## Setup

```bash
cd "Secure Network Configuration ELC Assignment"
pip install -r requirements.txt
```

Ensure `data/plaintext.txt` exists (copy from `Text_To_Be_Encypted.txt` if needed).

## Usage

```bash
# Interactive menu (from project root)
python run.py

# Or run directly
python src/main.py

# One-shot encrypt + graphs (uses default keys)
python run.py --encrypt

# Generate submission PDF
python run.py --pdf
```

**Menu options:**
1. **Encrypt** – Read `data/plaintext.txt`, encrypt with all three ciphers, save to `data/*_cipher.txt`, save keys to `data/keys.txt`
2. **Decrypt** – Load cipher files and keys, decrypt and verify
3. **Run full** – Encrypt + generate timing graphs to `assets/`
4. **Exit**

## Default Keys

| Algorithm | Key |
|-----------|-----|
| Caesar | 3 |
| Playfair | MONARCHY |
| Hill | GYBNQKURP (3×3) |

## Output Files

- `data/keys.txt` – Saved encryption keys
- `data/caesar_cipher.txt`, `data/playfair_cipher.txt`, `data/hill_cipher.txt` – Ciphertexts
- `assets/encryption_time.png`, `assets/decryption_time.png` – Timing graphs
- `output/submission.pdf` – Submission document

## Submission

- **Deadline:** February 22, 2026, 11:59 PM
- **Format:** `{roll_number}.zip` containing:
  - PDF (codes, keys, ciphertexts, graphs, analysis)
  - ~90-second video (face visible, explaining code)
