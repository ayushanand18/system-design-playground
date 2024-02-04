"""Utility functions"""

from pydantic import BaseModel
import uuid
import pygeohash as pgh


def generate_uuid() -> str:
    """Generate a unique identifier for a user session"""
    random_uuid = uuid.uuid4()
    return str(random_uuid)

def generate_8char_geohash(latitude, longitude):
    """Generate the GeoHash using the given latitude and longitude"""
    geohash_value = pgh.encode(latitude, longitude, precision=8)
    return geohash_value

class LocationItem(BaseModel):
    longitude: float
    latitude: float
    data: str

def geohash_precision_for_size(size_meters):
    """
    Determine the geohash precision level based on the given cell size.

    Parameters:
    - size_meters: The desired size of the geohash cell in meters.

    Returns:
    - Geohash precision level (length of the geohash string).
    """

    # Define a geohash cell size table with precalculated sizes
    geohash_sizes = {
        1: 5_009_416.8125,
        2: 1_252_354.203125,
        3: 156_544.275390625,
        4: 39_136.06884765625,
        5: 4_892.008605957031,
        6: 1_222.5467262268066,
        7: 152.81834077835083,
        8: 38.20458519458771,
        9: 4.775573149323463,
        10: 1.1938932873308658,
        11: 0.1492366609163582,
        12: 0.03730916522908956,
    }
    # Find the closest geohash precision for the given size
    closest_precision = min(geohash_sizes, key=lambda x: abs(geohash_sizes[x] - size_meters))

    # return one minus the precision because we have to find prefixes in adjacent cells too
    return max(0, closest_precision-1)