from cryptography.fernet import Fernet
from pathlib import Path

# Save this key securely or generate once and reuse
KEY_PATH = Path(__file__).resolve().parent.parent / "secret.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as f:
        f.write(key)

def load_key():
    if not KEY_PATH.exists():
        generate_key()
    return open(KEY_PATH, "rb").read()

def encrypt_token(token):
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token):
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_token.encode()).decode()
