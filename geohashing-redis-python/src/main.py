"""
Geohashing based proximity service.
"""

from fastapi import FastAPI

from .utils import generate_uuid, LocationItem
from .redis_utils import set_location_to_redis

app = FastAPI()

@app.get("/api/locations/search/{longitude}/{latitude}/{distance}")
async def get_locations_at_distance(longitude: float, latitude: float, distance: int) -> dict:
    """Return a set of location_ids at some distance"""
    # To Do: implement the ranking function
    pass

@app.post("/api/locations/create")
async def create_new_location(request: LocationItem):
    """Create a new location and return the id"""
    location_id = generate_uuid()
    location_hash = "" # To Do: define logic to assign a geohash to location
    set_location_to_redis(location_id, location_data, location_hash)

@app.get("/api/location/{location__id}")
async def get_location_data(location_id: int) -> dict:
    """Return metadata of the location_id"""
    return get_location_from_redis(location_id)