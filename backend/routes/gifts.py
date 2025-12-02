from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models import Gift, Wishlist
from schemas.gift import GiftCreate, GiftUpdate, GiftOut
from routes.deps import get_current_user, get_optional_user
from fastapi import Query


router = APIRouter(prefix="/gifts", tags=["gifts"])


@router.post("/wishlist/{wishlist_id}", response_model=GiftOut, status_code=status.HTTP_201_CREATED)
def add_gift(wishlist_id: int, payload: GiftCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
	w = db.get(Wishlist, wishlist_id)
	if not w:
		raise HTTPException(status_code=404, detail="Wishlist not found")
	if w.user_id != user.id:
		raise HTTPException(status_code=403, detail="Forbidden")
	g = Gift(wishlist_id=wishlist_id, **payload.dict())
	db.add(g)
	db.commit()
	db.refresh(g)
	return g


@router.patch("/{gift_id}", response_model=GiftOut)
def update_gift(gift_id: int, payload: GiftUpdate, db: Session = Depends(get_db), user=Depends(get_optional_user), token: str | None = Query(default=None)):
	g = db.get(Gift, gift_id)
	if not g:
		raise HTTPException(status_code=404, detail="Gift not found")
	w = db.get(Wishlist, g.wishlist_id)
	# Permissions: owner can edit any fields; others can ONLY change status with valid token
	data = payload.dict(exclude_unset=True)
	if user and w.user_id == user.id:
		pass
	else:
		if not token or token != w.share_token:
			raise HTTPException(status_code=403, detail="Forbidden")
		data = {k: v for k, v in data.items() if k == 'status'}
		if not data:
			raise HTTPException(status_code=403, detail="Only status can be changed by non-owner")
	for field, value in data.items():
		setattr(g, field, value)
	db.commit()
	db.refresh(g)
	return g


@router.delete("/{gift_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gift(gift_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
	g = db.get(Gift, gift_id)
	if not g:
		raise HTTPException(status_code=404, detail="Gift not found")
	w = db.get(Wishlist, g.wishlist_id)
	if w.user_id != user.id:
		raise HTTPException(status_code=403, detail="Forbidden")
	db.delete(g)
	db.commit()
	return None


@router.get("/wishlist/{wishlist_id}", response_model=List[GiftOut])
def list_gifts(wishlist_id: int, db: Session = Depends(get_db), user=Depends(get_optional_user)):
	w = db.get(Wishlist, wishlist_id)
	if not w:
		raise HTTPException(status_code=404, detail="Wishlist not found")
	if (not user or w.user_id != user.id) and not w.is_public:
		raise HTTPException(status_code=403, detail="Forbidden")
	return db.query(Gift).filter(Gift.wishlist_id == wishlist_id).all()


