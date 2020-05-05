import hashlib

def encrypt_string(value):
    sha_signature = hashlib.sha256(value.encode()).hexdigest()
    return sha_signature