#!/usr/bin/env python3
"""
Secure API Key Storage Module

Provides encrypted storage and retrieval of API keys with persistence
across server restarts. Uses Fernet encryption for secure storage.
"""

import os
import json
import base64
import time
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureKeyStorage:
    """Secure storage for API keys with encryption and persistence."""
    
    def __init__(self, storage_dir: str = None):
        """Initialize secure key storage."""
        self.storage_dir = Path(storage_dir) if storage_dir else Path(__file__).parent / 'secure_storage'
        self.storage_dir.mkdir(exist_ok=True, mode=0o700)  # Owner only permissions
        
        self.key_file = self.storage_dir / 'api_keys.enc'
        self.salt_file = self.storage_dir / 'key.salt'
        
        # Generate or load encryption key
        self._ensure_encryption_key()
        
    def _ensure_encryption_key(self):
        """Generate or load the encryption key."""
        # Create a salt for key derivation if it doesn't exist
        if not self.salt_file.exists():
            salt = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
            os.chmod(self.salt_file, 0o600)  # Owner read/write only
        else:
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
        
        # Derive encryption key from app secret + salt
        from flask import current_app
        try:
            secret = current_app.secret_key.encode()
        except RuntimeError:
            # Fallback for testing without app context
            secret = b'dev-key-change-in-production'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret))
        self.cipher = Fernet(key)
    
    def store_key(self, provider: str, api_key: str, model: str = None) -> bool:
        """
        Store an API key securely.
        
        Args:
            provider: LLM provider name (e.g., 'requestyai', 'openai')
            api_key: The API key to store
            model: Optional model name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Load existing keys or create new dict
            keys_data = self._load_keys_data()
            
            # Store key data
            keys_data[provider] = {
                'api_key': api_key,
                'model': model,
                'stored_at': str(int(time.time()))
            }
            
            # Encrypt and save
            self._save_keys_data(keys_data)
            return True
            
        except Exception as e:
            print(f"Error storing API key: {e}")
            return False
    
    def get_key(self, provider: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an API key.
        
        Args:
            provider: LLM provider name
            
        Returns:
            Dict with 'api_key', 'model', and 'stored_at' or None if not found
        """
        try:
            keys_data = self._load_keys_data()
            return keys_data.get(provider)
        except Exception as e:
            print(f"Error retrieving API key: {e}")
            return None
    
    def delete_key(self, provider: str) -> bool:
        """
        Delete an API key.
        
        Args:
            provider: LLM provider name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            keys_data = self._load_keys_data()
            if provider in keys_data:
                del keys_data[provider]
                self._save_keys_data(keys_data)
                return True
            return False
        except Exception as e:
            print(f"Error deleting API key: {e}")
            return False
    
    def list_stored_providers(self) -> list:
        """
        Get list of providers that have stored keys.
        
        Returns:
            List of provider names
        """
        try:
            keys_data = self._load_keys_data()
            return list(keys_data.keys())
        except Exception:
            return []
    
    def has_key(self, provider: str) -> bool:
        """
        Check if a provider has a stored key.
        
        Args:
            provider: LLM provider name
            
        Returns:
            bool: True if key exists, False otherwise
        """
        return provider in self.list_stored_providers()
    
    def _load_keys_data(self) -> Dict[str, Any]:
        """Load and decrypt keys data."""
        if not self.key_file.exists():
            return {}
        
        try:
            with open(self.key_file, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                return {}
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
            
        except Exception:
            # If we can't decrypt (key changed, file corrupted, etc.), return empty
            return {}
    
    def _save_keys_data(self, keys_data: Dict[str, Any]):
        """Encrypt and save keys data."""
        json_data = json.dumps(keys_data, indent=2)
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        with open(self.key_file, 'wb') as f:
            f.write(encrypted_data)
        
        # Set restrictive permissions
        os.chmod(self.key_file, 0o600)  # Owner read/write only
    
    def clear_all_keys(self) -> bool:
        """
        Clear all stored keys.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.key_file.exists():
                self.key_file.unlink()
            return True
        except Exception as e:
            print(f"Error clearing keys: {e}")
            return False


# Global storage instance
_storage = None

def get_key_storage() -> SecureKeyStorage:
    """Get the global key storage instance."""
    global _storage
    if _storage is None:
        _storage = SecureKeyStorage()
    return _storage