from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status
from sqlalchemy.orm import Session
from sqlalchemy import func
import random, string
from typing import List
from db import get_db
from models import Wishlist, Gift, User
from schemas.wishlist import WishlistCreate, WishlistUpdate, WishlistOut
from routes.deps import get_current_user, get_optional_user


router = APIRouter(prefix="/wishlists", tags=["wishlists"])


@router.get("", response_model=List[WishlistOut])
def list_wishlists(
	public: bool | None = Query(default=None),
	q: str | None = Query(default=None, description="search by title or gift name"),
	db: Session = Depends(get_db),
	user=Depends(get_optional_user)
):
	query = db.query(Wishlist, func.count(Gift.id).label("gift_count"), User.email.label("owner_email")).outerjoin(Gift).join(User, User.id == Wishlist.user_id)
	if public is True:
		query = query.filter(Wishlist.is_public == True)
	elif user:
		query = query.filter(Wishlist.user_id == user.id)
	else:
		# Not authenticated and not public => no data
		return []
	if q:
		like = f"%{q}%"
		query = query.filter((Wishlist.title.ilike(like)) | (Gift.name.ilike(like)))
	query = query.group_by(Wishlist.id, User.email)
	rows = query.all()
	return [WishlistOut.from_orm(w).copy(update={"gift_count": gc, "owner_email": owner_email if public else None}) for (w, gc, owner_email) in rows]


@router.post("", response_model=WishlistOut, status_code=status.HTTP_201_CREATED)
def create_wishlist(payload: WishlistCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	# generate 5-char share_token
	def gen_token():
		return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
	token = gen_token()
	while db.query(Wishlist).filter(Wishlist.share_token == token).first() is not None:
		token = gen_token()
	w = Wishlist(user_id=user.id, title=payload.title, description=payload.description, is_public=payload.is_public, share_token=token)
	db.add(w)
	db.commit()
	db.refresh(w)
	return WishlistOut.from_orm(w)


@router.patch("/{wishlist_id}", response_model=WishlistOut)
def update_wishlist(wishlist_id: int, payload: WishlistUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	w = db.get(Wishlist, wishlist_id)
	if not w:
		raise HTTPException(status_code=404, detail="Wishlist not found")
	if w.user_id != user.id:
		raise HTTPException(status_code=403, detail="Forbidden")
	for field, value in payload.dict(exclude_unset=True).items():
		setattr(w, field, value)
	db.commit()
	db.refresh(w)
	return WishlistOut.from_orm(w)


@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist(wishlist_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	w = db.get(Wishlist, wishlist_id)
	if not w:
		raise HTTPException(status_code=404, detail="Wishlist not found")
	if w.user_id != user.id:
		raise HTTPException(status_code=403, detail="Forbidden")
	db.delete(w)
	db.commit()
	return None


@router.get("/token/{share_token}", response_model=WishlistOut)
def get_by_token(share_token: str, db: Session = Depends(get_db)):
	w = db.query(Wishlist).filter(Wishlist.share_token == share_token).first()
	if not w:
		raise HTTPException(status_code=404, detail="Wishlist not found")
	gc = db.query(func.count(Gift.id)).filter(Gift.wishlist_id == w.id).scalar() or 0
	return WishlistOut.from_orm(w).copy(update={"gift_count": gc, "owner_email": None})


