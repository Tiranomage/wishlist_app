from pydantic import BaseModel, AnyUrl, constr, field_validator, ConfigDict
from typing import Optional


class GiftBase(BaseModel):
	name: constr(min_length=1, max_length=100)
	price: Optional[float] = None
	image_url: Optional[str] = None
	purchase_link: Optional[AnyUrl] = None
	status: Optional[str] = "Свободен"

	@field_validator("image_url")
	def validate_image_url(cls, v):
		if v is None or v == "":
			return v
		if not (v.startswith("http://") or v.startswith("https://")):
			raise ValueError("image_url must be a valid URL")
		return v


class GiftCreate(GiftBase):
	pass


class GiftUpdate(BaseModel):
	name: Optional[constr(min_length=1, max_length=100)] = None
	price: Optional[float] = None
	image_url: Optional[str] = None
	purchase_link: Optional[AnyUrl] = None
	status: Optional[str] = None


class GiftOut(GiftBase):
	id: int

	model_config = ConfigDict(from_attributes=True)


