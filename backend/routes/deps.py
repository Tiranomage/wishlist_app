from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from db import get_db
from models import User


def _get_user_from_session(request: Request, db: Session) -> User | None:
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return db.get(User, int(user_id))


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user = _get_user_from_session(request, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return user


def get_optional_user(request: Request, db: Session = Depends(get_db)):
    return _get_user_from_session(request, db)


