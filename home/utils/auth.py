import secrets
import string
import hashlib
import base64

def generate_code_verifier():
    alphabet = string.ascii_letters + string.digits + '-._~'
    return ''.join(secrets.choice(alphabet) for _ in range(43))

def generate_code_challenge(code_verifier):
    ascii_bytes = code_verifier.encode('ascii')
    sha256_hash = hashlib.sha256(ascii_bytes).digest()
    base64_encoded = base64.urlsafe_b64encode(sha256_hash).rstrip(b'=')
    return base64_encoded.decode('ascii')