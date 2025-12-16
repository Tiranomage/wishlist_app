from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from models import User
from routes.deps import get_current_user
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse, PasswordResetRequest, PasswordResetConfirm
from services.security import hash_password, verify_password, create_password_reset_token, decode_token, create_access_token, create_refresh_token
from fastapi import Request


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
	existing_user = db.query(User).filter(User.email == payload.email).first()
	if existing_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = User(email=payload.email, password_hash=hash_password(payload.password))
	try:
		db.add(user)
		db.commit()
		db.refresh(user)
		return {"id": user.id, "email": user.email}
	except Exception as e:
		db.rollback()
		# Проверяем, возможно, ошибка из-за уникальности
		if db.query(User).filter(User.email == payload.email).first():
			raise HTTPException(status_code=400, detail="Email already registered")
		else:
			raise HTTPException(status_code=500, detail="An error occurred during registration")


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Set session for compatibility
    request.session['user_id'] = user.id
    
    # Generate JWT tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"detail": "ok"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_token_endpoint(request: Request, refresh_token: str, db: Session = Depends(get_db)):
    try:
        # Decode the provided refresh token to get user id
        token_data = decode_token(refresh_token, refresh=True)
        user_id = int(token_data.get("sub"))
        
        # Verify user exists
        user = db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        # Generate new tokens
        new_access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@router.get("/me")
def get_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}


@router.post("/password-reset", status_code=200)
def password_reset_request(payload: PasswordResetRequest, db: Session = Depends(get_db)):
	user = db.query(User).filter(User.email == payload.email).first()
	if not user:
		# Do not reveal existence
		return {"detail": "If the email exists, a reset token has been issued"}
	token = create_password_reset_token(user.id)
	print(f"[Password Reset] email={user.email} token={token}")
	return {"detail": "If the email exists, a reset token has been issued"}


@router.post("/password-reset/confirm", status_code=200)
def password_reset_confirm(payload: PasswordResetConfirm, db: Session = Depends(get_db)):
	try:
		data = decode_token(payload.token)
		if data.get("type") != "password_reset":
			raise ValueError("wrong type")
		user_id = int(data["sub"])
	except Exception:
		raise HTTPException(status_code=400, detail="Invalid or expired token")
	user = db.get(User, user_id)
	if not user:
		raise HTTPException(status_code=400, detail="Invalid token")
	user.password_hash = hash_password(payload.new_password)
	db.commit()
	return {"detail": "Password updated"}


