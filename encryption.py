from cryptography.fernet import Fernet, InvalidToken

class EncryptionManager:
    def __init__(self, key):
        self.cipher_suite = Fernet(key)

    def encrypt_message(self, message):
        message_bytes = message.encode()
        encrypted_message = self.cipher_suite.encrypt(message_bytes)
        return encrypted_message.decode()

    def decrypt_message(self, encrypted_message):
        encrypted_message_bytes = encrypted_message.encode()
        try:
            decrypted_message = self.cipher_suite.decrypt(encrypted_message_bytes)
        except InvalidToken:
            return encrypted_message
        return decrypted_message.decode()
