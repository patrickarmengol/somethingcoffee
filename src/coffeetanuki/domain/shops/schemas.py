from __future__ import annotations
from geoalchemy2 import WKBElement, shape
from pydantic import BaseModel, UUID4, validator, HttpUrl
from shapely.geometry import Point


__all__ = [
    "Coordinates",
    "ShopBase",
    "ShopCreate",
    "ShopUpdate",
    "ShopDB",
    "ShopDBFull",
]


class Coordinates(BaseModel):
    # TODO: validate
    lon: float
    lat: float


class ShopBase(BaseModel):
    name: str
    country: str
    city: str
    address: str
    coordinates: Coordinates
    roaster: str | None
    hours_of_operation: str | None
    website: HttpUrl | None
    gmaps_link: HttpUrl | None
    description: str | None


class ShopCreate(ShopBase):
    tags: list[str]


class ShopUpdate(BaseModel):
    name: str | None
    country: str | None
    city: str | None
    address: str | None
    coordinates: Coordinates | None
    roaster: str | None
    hours_of_operation: str | None
    website: HttpUrl | None
    gmaps_link: HttpUrl | None
    description: str | None
    tags: list[str] | None


class ShopDB(ShopBase):
    id: UUID4

    @validator("coordinates", pre=True)
    def to_coords(cls, v):
        if isinstance(v, WKBElement):
            p = shape.to_shape(v)  # convert WKBElement to shapely Point
            if p and isinstance(p, Point):
                return Coordinates(lon=p.x, lat=p.y)
            else:
                raise TypeError(
                    "couldn't convert returned WKB element to shapely Point"
                )
        else:
            return v

    class Config:
        orm_mode = True


from coffeetanuki.domain.tags.schemas import TagDB  # noqa: E402


class ShopDBFull(ShopDB):
    tags: list[TagDB]
