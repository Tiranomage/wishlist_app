from pydantic import BaseModel, EmailStr, constr, ConfigDict


class RegisterRequest(BaseModel):
	email: EmailStr
	password: constr(min_length=8)


class LoginRequest(BaseModel):
	email: EmailStr
	password: constr(min_length=8)


class TokenResponse(BaseModel):
	access_token: str
	refresh_token: str
	token_type: str = "bearer"


class PasswordResetRequest(BaseModel):
	email: EmailStr


class PasswordResetConfirm(BaseModel):
	token: str
	new_password: constr(min_length=8)


