import os
from datetime import datetime, timezone
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

def generate_password_hash(password: str):
    return password_hash.hash(password)

def check_password_hash(password, password_hashed):
    return password_hash.verify(password, password_hashed)

def get_timestamp_utc_now():
    return datetime.now(timezone.utc)

def gerar_env():
    if not os.path.exists(".env"):
        vars = {
            "DB_USERNAME": "root",
            "DB_PASSWORD": "admin",
            "DB_HOST": "localhost",
            "DB_PORT": 3306,
            "DATABASE": "ecommerce"
        }
        
        lines = []
        for key, value in vars.items():
            lines.append(f"{key}={value}\n")

        with open(".env", "w") as file:
            file.writelines(lines)