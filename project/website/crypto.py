# website/crypto.py
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode
from flask import current_app
import os

class RoomCodeCrypto:
    def __init__(self, app=None):
        self.fernet = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize with Flask app"""
        secret_key = app.config['SECRET_KEY']
        if not secret_key:
            raise ValueError("Flask SECRET_KEY must be set")
        
        # Use the app's secret key to generate a consistent Fernet key
        key = b64encode(secret_key.encode()[:32].ljust(32, b'\0'))
        self.fernet = Fernet(key)
        
        # Add self to app
        app.crypto = self

    def encrypt_room_code(self, room_code: str) -> str:
        """Encrypt a room code"""
        if not isinstance(room_code, str):
            raise ValueError("Room code must be a string")
        
        encrypted_data = self.fernet.encrypt(room_code.encode())
        return b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_room_code(self, encrypted_code: str) -> str:
        """Decrypt an encrypted room code"""
        try:
            encrypted_data = b64decode(encrypted_code.encode('utf-8'))
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Failed to decrypt room code: {str(e)}")

room_crypto = RoomCodeCrypto()  # Create a single instance