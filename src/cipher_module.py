"""
ELC Secure Network Configuration - Cipher Module
Implements Caesar, Playfair, and Hill ciphers for symmetric encryption.
"""

import re
import numpy as np


def _normalize_text(text: str, replace_j: bool = False) -> str:
    """Remove non A-Z, uppercase. If replace_j, map J->I (for Playfair only)."""
    s = re.sub(r"[^A-Z]", "", text.upper())
    return s.replace("J", "I") if replace_j else s


# ============== CAESAR CIPHER ==============


def caesar_encrypt(plaintext: str, shift: int) -> str:
    """Encrypt text using Caesar cipher: E(x) = (x + shift) mod 26."""
    result = []
    for char in plaintext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            shifted = (ord(char) - base + shift) % 26 + base
            result.append(chr(shifted))
        else:
            result.append(char)
    return "".join(result)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    """Decrypt text using Caesar cipher: D(x) = (x - shift) mod 26."""
    return caesar_encrypt(ciphertext, -shift)


# ============== PLAYFAIR CIPHER ==============


def _build_playfair_matrix(keyword: str) -> list[list[str]]:
    """Build 5x5 Playfair matrix from keyword. I and J share same cell."""
    keyword = _normalize_text(keyword, replace_j=True)
    seen = set()
    matrix = []
    row = []

    # Add keyword letters first
    for c in keyword:
        if c not in seen:
            seen.add(c)
            row.append(c)
            if len(row) == 5:
                matrix.append(row)
                row = []

    # Add remaining alphabet (A-Z except J, treat as I)
    for c in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if c not in seen:
            seen.add(c)
            row.append(c)
            if len(row) == 5:
                matrix.append(row)
                row = []

    if row:
        matrix.append(row)
    return matrix


def _playfair_find_position(matrix: list[list[str]], char: str) -> tuple[int, int]:
    """Find (row, col) of character in matrix."""
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    raise ValueError(f"Character {char} not in matrix")


def _playfair_encrypt_pair(matrix: list[list[str]], a: str, b: str) -> str:
    """Encrypt a digraph using Playfair rules."""
    r1, c1 = _playfair_find_position(matrix, a)
    r2, c2 = _playfair_find_position(matrix, b)

    if r1 == r2:  # Same row: replace with letters to the right
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:  # Same column: replace with letters below
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:  # Rectangle: opposite corners
        return matrix[r1][c2] + matrix[r2][c1]


def _playfair_decrypt_pair(matrix: list[list[str]], a: str, b: str) -> str:
    """Decrypt a digraph using Playfair rules."""
    r1, c1 = _playfair_find_position(matrix, a)
    r2, c2 = _playfair_find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]


def playfair_encrypt(plaintext: str, keyword: str) -> str:
    """Encrypt using Playfair cipher."""
    text = _normalize_text(plaintext, replace_j=True)
    matrix = _build_playfair_matrix(keyword)

    # Pad with X if odd length; handle duplicate letters in pair
    i = 0
    pairs = []
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"
        if a == b:
            b = "X"
            i += 1
        else:
            i += 2
        pairs.append((a, b))

    return "".join(_playfair_encrypt_pair(matrix, p[0], p[1]) for p in pairs)


def playfair_decrypt(ciphertext: str, keyword: str) -> str:
    """Decrypt using Playfair cipher."""
    text = _normalize_text(ciphertext, replace_j=True)
    matrix = _build_playfair_matrix(keyword)
    if len(text) % 2 != 0:
        text += "X"

    result = []
    for i in range(0, len(text), 2):
        result.append(_playfair_decrypt_pair(matrix, text[i], text[i + 1]))
    return "".join(result)


# ============== HILL CIPHER ==============


def _hill_key_to_matrix(key: str) -> np.ndarray:
    """Convert key string to nxn matrix. Key length must be n^2."""
    key = _normalize_text(key, replace_j=False)
    n = int(len(key) ** 0.5)
    if n * n != len(key):
        raise ValueError("Key length must be a perfect square (e.g. 9 for 3x3)")
    mat = np.zeros((n, n), dtype=int)
    for i, c in enumerate(key):
        mat[i // n, i % n] = ord(c) - ord("A")
    return mat


def _mod_inverse(a: int, m: int = 26) -> int:
    """Modular multiplicative inverse of a mod m."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError("Matrix is not invertible mod 26")


def _matrix_inverse_mod26(mat: np.ndarray) -> np.ndarray:
    """Compute matrix inverse modulo 26. Uses adjugate: K^(-1) = adj(K)/det(K)."""
    det = int(np.round(np.linalg.det(mat))) % 26
    det_inv = _mod_inverse(det)
    n = mat.shape[0]
    # Adjugate: (adj K)_ij = C_ji where C_ji = (-1)^(j+i) * M_ji
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            minor = np.delete(np.delete(mat, j, 0), i, 1)  # M_ji: delete row j, col i
            cofactor = ((-1) ** (j + i) * int(np.round(np.linalg.det(minor)))) % 26
            adj[i, j] = (cofactor * det_inv) % 26
    return adj


def hill_encrypt(plaintext: str, key: str) -> str:
    """Encrypt using Hill cipher with nxn key matrix."""
    text = _normalize_text(plaintext, replace_j=False)
    key_mat = _hill_key_to_matrix(key)
    n = key_mat.shape[0]

    # Pad with X if needed
    while len(text) % n != 0:
        text += "X"

    result = []
    for i in range(0, len(text), n):
        block = np.array([ord(c) - ord("A") for c in text[i : i + n]])
        encrypted = (key_mat @ block) % 26
        result.append("".join(chr(x + ord("A")) for x in encrypted))

    return "".join(result)


def hill_decrypt(ciphertext: str, key: str) -> str:
    """Decrypt using Hill cipher."""
    text = _normalize_text(ciphertext, replace_j=False)
    key_mat = _hill_key_to_matrix(key)
    inv_mat = _matrix_inverse_mod26(key_mat)
    n = key_mat.shape[0]

    while len(text) % n != 0:
        text += "X"

    result = []
    for i in range(0, len(text), n):
        block = np.array([ord(c) - ord("A") for c in text[i : i + n]])
        decrypted = (inv_mat @ block) % 26
        result.append("".join(chr(int(x) + ord("A")) for x in decrypted))

    return "".join(result)
