from pydantic import BaseModel, constr, ConfigDict
from typing import Optional


class WishlistBase(BaseModel):
	title: constr(min_length=1, max_length=100)
	description: Optional[str] = None
	is_public: bool = False


class WishlistCreate(WishlistBase):
	pass


class WishlistUpdate(BaseModel):
	title: Optional[constr(min_length=1, max_length=100)] = None
	description: Optional[str] = None
	is_public: Optional[bool] = None


class WishlistOut(WishlistBase):
	id: int
	gift_count: int | None = 0
	owner_email: str | None = None
	share_token: str | None = None

	model_config = ConfigDict(from_attributes=True)


