from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from db import get_db
from models import User
from services.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()


def _get_user_from_session(request: Request, db: Session) -> User | None:
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return db.get(User, int(user_id))


def _get_user_from_token(credentials: HTTPAuthorizationCredentials, db: Session) -> User | None:
    try:
        token = credentials.credentials
        token_data = decode_token(token, refresh=False)
        user_id = int(token_data.get("sub"))
        return db.get(User, user_id)
    except Exception as e:
        # Логируем ошибку для отладки, но не возвращаем подробности клиенту
        print(f"[Auth Debug] Token decode error: {str(e)}")
        return None


def get_current_user(
    request: Request, 
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # First try to get user from JWT token
    user = _get_user_from_token(credentials, db)
    
    # Fallback to session if token not valid
    if not user:
        user = _get_user_from_session(request, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)):
    # Try token first, then session
    credentials = request.headers.get("authorization")
    if credentials and credentials.startswith("Bearer "):
        token = credentials[7:]  # Remove "Bearer " prefix
        try:
            token_data = decode_token(token, refresh=False)
            user_id = int(token_data.get("sub"))
            return db.get(User, user_id)
        except Exception as e:
            print(f"[Auth Debug] Optional user token decode error: {str(e)}")
            pass
    
    # Fallback to session
    return _get_user_from_session(request, db)


