import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_text(plaintext: str, password: str) -> str:
    """Encrypts the given plaintext using AES encryption with CTR mode.

    Args:
        plaintext (str): The text to be encrypted.
        password (str): The password used to derive the encryption key.

    Returns:
        str: The encrypted ciphertext encoded in base16.

    Raises:
        None
    """
    backend = default_backend()
    key = password.encode()[:32]
    iv = b"\x00" * 16

    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    ciphertext = base64.b16encode(ciphertext).decode("utf-8")
    return ciphertext


def decrypt_text(ciphertext: str, password: str) -> str:
    """Decrypts the given ciphertext using AES decryption with CTR mode.

    Args:
        ciphertext (str): The ciphertext to be decrypted (encoded in base16).
        password (str): The password used to derive the decryption key.

    Returns:
        str: The decrypted plaintext.

    Raises:
        None
    """
    ciphertext = base64.b16decode(ciphertext)
    backend = default_backend()
    key = password.encode()[:32]
    iv = b"\x00" * 16

    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=backend)
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()
