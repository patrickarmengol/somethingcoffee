from geoalchemy2 import WKBElement, shape
from pydantic import BaseModel, UUID4, validator
from shapely.geometry import Point


class Coordinates(BaseModel):
    # TODO: validate
    lon: float
    lat: float


class ShopBase(BaseModel):
    name: str
    address: str
    coordinates: Coordinates


class ShopCreate(ShopBase):
    pass


class Shop(ShopBase):
    id: UUID4 | None

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
