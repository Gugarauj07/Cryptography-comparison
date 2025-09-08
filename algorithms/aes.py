from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class AES:

    def __init__(self, key_size=256):
        self.key_size = key_size
        self.key = None
        self.backend = default_backend()

    def generate_key(self):
        key_length = self.key_size // 8
        self.key = os.urandom(key_length)
        return self.key

    def set_key(self, key):
        self.key = key

    def encrypt(self, plaintext):
        if self.key is None:
            raise ValueError("Chave não definida. Use generate_key() ou set_key()")

        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        padded_data = self._pad(plaintext)

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv, ciphertext

    def decrypt(self, iv, ciphertext):
        if self.key is None:
            raise ValueError("Chave não definida. Use generate_key() ou set_key()")

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        plaintext = self._unpad(padded_plaintext)

        return plaintext

    def _pad(self, data):
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad(self, data):
        if not data:
            return data
        padding_length = data[-1]
        return data[:-padding_length]
