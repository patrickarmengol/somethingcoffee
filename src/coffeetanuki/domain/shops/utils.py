from typing import Any

from coffeetanuki.domain.shops import schemas


# TODO: think about using geojson_pydantic; easier seralization
def geojsonify(shops: list[schemas.ShopDB]):
    geojson: dict[str, Any] = {"type": "FeatureCollection", "features": []}
    for shop in shops:
        feature: dict[str, Any] = {
            "type": "Feature",
            "properties": {
                "id": shop.id,
                "name": shop.name,
            },  # perhaps add more attributes here?
            "geometry": {
                "type": "Point",
                "coordinates": [shop.coordinates.lon, shop.coordinates.lat],
            },
        }
        geojson["features"].append(feature)
    return geojson


# TODO: implement ungeojsonify function
