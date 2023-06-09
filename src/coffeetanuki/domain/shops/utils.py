from typing import Any

from coffeetanuki.domain.shops import schemas


def geojsonify(shops: list[schemas.ShopDB]):
    geojson: dict[str, Any] = {"type": "FeatureCollection", "features": []}
    for shop in shops:
        feature: dict[str, Any] = {
            "type": "Feature",
            "properties": {"name": shop.name},  # perhaps add more attributes here?
            "geometry": {
                "type": "Point",
                "coordinates": [shop.coordinates.lon, shop.coordinates.lat],
            },
        }
        geojson["features"].append(feature)
    return geojson
