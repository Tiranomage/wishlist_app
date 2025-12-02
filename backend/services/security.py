from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from authlib.jose import jwt
from passlib.context import CryptContext
from config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
	return pwd_context.verify(password, password_hash)


def create_access_token(subject: str | int, expires_minutes: Optional[int] = None) -> str:
	expires_delta = timedelta(minutes=expires_minutes or settings.access_token_expires_minutes)
	expire = datetime.now(timezone.utc) + expires_delta
	claims = {"exp": int(expire.timestamp()), "sub": str(subject), "type": "access"}
	header = {"alg": settings.jwt_algorithm}
	return jwt.encode(header, claims, settings.jwt_secret_key).decode()


def create_refresh_token(subject: str | int, expires_days: Optional[int] = None) -> str:
	expires_delta = timedelta(days=expires_days or settings.refresh_token_expires_days)
	expire = datetime.now(timezone.utc) + expires_delta
	claims = {"exp": int(expire.timestamp()), "sub": str(subject), "type": "refresh"}
	header = {"alg": settings.jwt_algorithm}
	return jwt.encode(header, claims, settings.jwt_refresh_secret_key).decode()


def decode_token(token: str, refresh: bool = False) -> dict[str, Any]:
	secret = settings.jwt_refresh_secret_key if refresh else settings.jwt_secret_key
	claims = jwt.decode(token, secret)
	jwt.validate_claims(claims, claims_options={"exp": {"essential": True}})
	return claims


def create_password_reset_token(subject: str | int, expires_minutes: int = 30) -> str:
	expires_delta = timedelta(minutes=expires_minutes)
	expire = datetime.now(timezone.utc) + expires_delta
	claims = {"exp": int(expire.timestamp()), "sub": str(subject), "type": "password_reset"}
	header = {"alg": settings.jwt_algorithm}
	return jwt.encode(header, claims, settings.jwt_secret_key).decode()


