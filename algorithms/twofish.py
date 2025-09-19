import chilkat2
import os
import binascii


class Twofish:
    
    def __init__(self, key_size=256):
        if key_size not in [128, 192, 256]:
            raise ValueError("Tamanho da chave deve ser 128, 192 ou 256 bits")
        
        self.key_size = key_size
        self.key = None
        self.crypt = chilkat2.Crypt2()
        
        # Configurar o algoritmo Twofish
        self.crypt.CryptAlgorithm = "twofish"
        self.crypt.CipherMode = "cbc"
        self.crypt.KeyLength = key_size
        self.crypt.PaddingScheme = 0  # PKCS7 padding
        self.crypt.EncodingMode = "hex"

    def generate_key(self):
        key_length = self.key_size // 8
        self.key = os.urandom(key_length)
        
        # Converter para hex e configurar na instância Chilkat
        key_hex = binascii.hexlify(self.key).decode('ascii')
        self.crypt.SetEncodedKey(key_hex, "hex")
        
        return self.key

    def set_key(self, key):
        expected_length = self.key_size // 8
        if len(key) != expected_length:
            raise ValueError(f"Chave deve ter {expected_length} bytes")
        
        self.key = key
        
        # Converter para hex e configurar na instância Chilkat
        key_hex = binascii.hexlify(self.key).decode('ascii')
        self.crypt.SetEncodedKey(key_hex, "hex")

    def encrypt(self, plaintext):
        if self.key is None:
            raise ValueError("Chave não definida. Use generate_key() ou set_key()")

        # Gerar IV aleatório (16 bytes para Twofish)
        iv = os.urandom(16)
        iv_hex = binascii.hexlify(iv).decode('ascii')
        self.crypt.SetEncodedIV(iv_hex, "hex")

        # Converter plaintext para hex
        plaintext_hex = binascii.hexlify(plaintext).decode('ascii')
        
        # Criptografar
        encrypted_hex = self.crypt.EncryptStringENC(plaintext_hex)
        if not encrypted_hex:
            raise RuntimeError("Falha na criptografia")
        
        # Converter resultado de volta para bytes
        ciphertext = binascii.unhexlify(encrypted_hex)
        
        return iv, ciphertext

    def decrypt(self, iv, ciphertext):
        if self.key is None:
            raise ValueError("Chave não definida. Use generate_key() ou set_key()")

        # Configurar IV
        iv_hex = binascii.hexlify(iv).decode('ascii')
        self.crypt.SetEncodedIV(iv_hex, "hex")

        # Converter ciphertext para hex
        ciphertext_hex = binascii.hexlify(ciphertext).decode('ascii')
        
        # Descriptografar
        decrypted_hex = self.crypt.DecryptStringENC(ciphertext_hex)
        if not decrypted_hex:
            raise RuntimeError("Falha na descriptografia")
        
        # Converter resultado de volta para bytes
        plaintext = binascii.unhexlify(decrypted_hex)
        
        return plaintext
