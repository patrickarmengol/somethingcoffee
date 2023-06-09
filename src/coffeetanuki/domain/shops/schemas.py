from __future__ import annotations
from geoalchemy2 import WKBElement, shape
from pydantic import BaseModel, UUID4, validator
from shapely.geometry import Point


__all__ = [
    "Coordinates",
    "ShopBase",
    "ShopCreate",
    "ShopUpdate",
    "ShopDB",
    "AmenityBase",
    "AmenityCreate",
    "AmenityUpdate",
    "AmenityDB",
]


class Coordinates(BaseModel):
    # TODO: validate
    lon: float
    lat: float


class AmenityBase(BaseModel):
    name: str


class AmenityCreate(AmenityBase):
    pass


class AmenityUpdate(BaseModel):
    name: str | None


class AmenityDB(AmenityBase):
    id: UUID4

    class Config:
        orm_mode = True


class ShopBase(BaseModel):
    name: str
    address: str
    coordinates: Coordinates
    roaster: str | None
    hours_of_operation: str | None
    description: str | None


class ShopCreate(ShopBase):
    amenities: list[str]


class ShopUpdate(BaseModel):
    name: str | None
    address: str | None
    coordinates: Coordinates | None
    roaster: str | None
    hours_of_operation: str | None
    description: str | None
    amenities: list[str] | None


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


class AmenityDBFull(AmenityDB):
    shops: list[ShopDB]


class ShopDBFull(ShopDB):
    amenities: list[AmenityDB]
