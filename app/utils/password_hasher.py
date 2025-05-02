from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def hash_password(password: str) -> str:
    return PasswordHasher().hash(password)

def verify_password(hashed: str, plain_password: str) -> bool:
    try:
        return PasswordHasher().verify(hashed, plain_password)
    except VerifyMismatchError:
        return False