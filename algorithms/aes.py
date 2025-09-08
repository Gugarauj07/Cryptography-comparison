"""
Módulo AES - Implementação do algoritmo Advanced Encryption Standard
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


class AES:
    """Classe para operações de criptografia AES"""

    def __init__(self, key_size=256):
        """
        Inicializa o AES com tamanho de chave especificado

        Args:
            key_size (int): Tamanho da chave em bits (128, 192 ou 256)
        """
        self.key_size = key_size
        self.key = None
        self.backend = default_backend()

    def generate_key(self):
        """Gera uma chave aleatória para AES"""
        key_length = self.key_size // 8  # Converte bits para bytes
        self.key = os.urandom(key_length)
        return self.key

    def set_key(self, key):
        """Define uma chave específica"""
        self.key = key

    def encrypt(self, plaintext):
        """
        Criptografa dados usando AES

        Args:
            plaintext (bytes): Dados a serem criptografados

        Returns:
            tuple: (iv, ciphertext) - Vetor de inicialização e texto criptografado
        """
        if self.key is None:
            raise ValueError("Chave não definida. Use generate_key() ou set_key()")

        # Gera IV aleatório
        iv = os.urandom(16)

        # Cria o cipher
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Aplica padding PKCS7 se necessário
        padded_data = self._pad(plaintext)

        # Criptografa
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return iv, ciphertext

    def decrypt(self, iv, ciphertext):
        """
        Descriptografa dados usando AES

        Args:
            iv (bytes): Vetor de inicialização
            ciphertext (bytes): Dados criptografados

        Returns:
            bytes: Dados descriptografados
        """
        if self.key is None:
            raise ValueError("Chave não definida. Use generate_key() ou set_key()")

        # Cria o cipher
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        # Descriptografa
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove padding
        plaintext = self._unpad(padded_plaintext)

        return plaintext

    def _pad(self, data):
        """Aplica padding PKCS7"""
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def _unpad(self, data):
        """Remove padding PKCS7"""
        if not data:
            return data
        padding_length = data[-1]
        return data[:-padding_length]
