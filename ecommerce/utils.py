from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def generate_password_hash(password: str):
    return password_hash.hash(password)

def check_password_hash(password, password_hashed):
    return password_hash.verify(password, password_hashed)
