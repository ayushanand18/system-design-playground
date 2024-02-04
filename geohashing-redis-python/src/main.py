"""
Geohashing based proximity service.
"""

from fastapi import FastAPI

from .utils import generate_uuid, LocationItem, generate_8char_geohash
from .redis_utils import set_location_to_redis

app = FastAPI()

@app.get("/api/locations/search/{longitude}/{latitude}/{distance}")
async def get_locations_at_distance(longitude: float, latitude: float, distance: int) -> dict:
    """Return a set of location_ids at some distance"""
    geohash = generate_8char_geohash(latitude, longitude)
    location_ids = await find_keys_with_prefix(geohash)
    return {"data": location_ids}

@app.post("/api/locations/create")
async def create_new_location(location: LocationItem):
    """Create a new location and return the id"""
    location_id = generate_uuid()
    location_hash = generate_8char_geohash(location.latitude, location.longitude)
    await set_location_to_redis(location_id, location.data, location_hash)
    return {"status": "success", "message": location_id}

@app.get("/api/location/{location__id}")
async def get_location_data(location_id: int) -> dict:
    """Return metadata of the location_id"""
    return await get_location_from_redis(location_id)