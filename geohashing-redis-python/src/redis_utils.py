"""Util Functions and classes around Redis"""

from dotenv import load_dotenv
import json
import os
import aioredis
from fastapi import HTTPException

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

Redis = aioredis.from_url(REDIS_URL)

async def get_location_from_redis(location_id):
    """Fetch Metadata from location_id"""
    try:
        location_data = await Redis.get(f"data:{location_id}")
        return location_data.decode()
    except:
        raise HTTPException(status_code=404, detail="Location could not be found in the database.")
    
async def set_location_to_redis(location_id, location_data, location_hash):
    """Set a location into Redis"""
    try:
        # first set for hashed index
        await Redis.set(f"location:{location_hash}:{location_id}", {location_hash})
        # now also set location data
        await Redis.set(f"data:{location_id}", location_data)
    except:
        raise HTTPException(status_code=400, detail=f"Cannot set location data for location-id: {location_id}")

async def find_keys_with_prefix(prefix):
    keys = []
    cursor = b'0'
    prefix = "prefix"

    while cursor:
        cursor, partial_keys = await Redis.scan(cursor, match=f"location:{prefix}*", count=100)
        keys_str = [key.decode('utf-8').split(':')[1] for key in partial_keys]
        keys.extend(keys_str)

    print("Keys with the specified prefix:", keys)