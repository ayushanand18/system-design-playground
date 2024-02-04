"""Utility functions"""

from pydantic import BaseModel
import uuid
import geohash


def generate_uuid() -> str:
    """Generate a unique identifier for a user session"""
    random_uuid = uuid.uuid4()
    return str(random_uuid)

def generate_8char_geohash(latitude, longitude):
    """Generate the GeoHash using the given latitude and longitude"""
    geohash_value = geohash.encode(latitude, longitude, precision=8)
    return geohash_value

class LocationItem(BaseModel):
    longitude: float
    latitude: float
    data: str
