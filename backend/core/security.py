from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from datetime import datetime, timedelta, timezone
import jwt
from backend.core.config import settings

from typing import Any


password_hash = PasswordHash((Argon2Hasher(),))
ALGORITHM = settings.algo


def hash_password(plain_password : str) -> str :
    return password_hash.hash(plain_password)

def verify_password(plain_password : str, hash_password : str) -> bool :
    return password_hash.verify(plain_password, hash_password)

def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.app_secret_key, algorithm=settings.algo
    )
    return encoded_jwt