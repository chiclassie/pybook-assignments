import string
import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for index in plaintext:
        if ord("z") >= ord(index) >= ord("a") or ord("Z") >= ord(index) >= ord("A"):
            ch = string.ascii_lowercase.find(index)
            if ch == -1:
                ch = string.ascii_uppercase.find(index)
                if ch == -1:
                    ciphertext += index
                else:
                    res = (ch + shift) % len(string.ascii_uppercase)
                    ciphertext += string.ascii_uppercase[res]
            else:
                res = (ch + shift) % len(string.ascii_lowercase)
                ciphertext += string.ascii_lowercase[res]
        else:
            ciphertext += index
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for index in ciphertext:
        if ord("z") >= ord(index) >= ord("a") or ord("Z") >= ord(index) >= ord("A"):
            ch = string.ascii_lowercase.find(index)
            if ch == -1:
                ch = string.ascii_uppercase.find(index)
                if ch == -1:
                    plaintext += index
                else:
                    res = (ch - shift) % len(string.ascii_uppercase)
                    plaintext += string.ascii_uppercase[res]
            else:
                res = (ch - shift) % len(string.ascii_lowercase)
                plaintext += string.ascii_lowercase[res]
        else:
            plaintext += index
    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    k = 0
    for shift in range(26):
        s = 0
        plaintext = decrypt_caesar(ciphertext, shift)
        words = plaintext.split()
        for word in words:
            if word in dictionary:
                s += 1
            if s > k:
                k = s
                best_shift = shift
    return best_shift
