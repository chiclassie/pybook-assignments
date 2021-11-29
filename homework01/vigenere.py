import string


def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    for index, i in enumerate(plaintext):
        if i == " ":
            ciphertext += " "
        else:
            f = string.ascii_uppercase.find(i)
            if f == -1:
                f = string.ascii_lowercase.find(i)
                if f == -1:
                    ciphertext += i
                else:
                    k = string.ascii_lowercase.find(keyword[index % len(keyword)])
                    res = (f + k) % len(string.ascii_lowercase)
                    ciphertext += string.ascii_lowercase[res]
            else:
                k = string.ascii_uppercase.find(keyword[index % len(keyword)])
                res = (f + k) % len(string.ascii_uppercase)
                ciphertext += string.ascii_uppercase[res]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    for index, i in enumerate(ciphertext):
        if i == " ":
            plaintext += " "
        else:
            f = string.ascii_uppercase.find(i)
            if f == -1:
                f = string.ascii_lowercase.find(i)
                if f == -1:
                    plaintext += i
                else:
                    k = string.ascii_lowercase.find(keyword[index % len(keyword)])
                    res = (f - k) % len(string.ascii_lowercase)
                    plaintext += string.ascii_lowercase[res]
            else:
                k = string.ascii_uppercase.find(keyword[index % len(keyword)])
                res = (f - k) % len(string.ascii_uppercase)
                plaintext += string.ascii_uppercase[res]
    return plaintext
