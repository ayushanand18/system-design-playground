"""Utility functions"""

from pydantic import BaseModel
import uuid

def generate_uuid() -> str:
    """Generate a unique identifier for a user session"""
    random_uuid = uuid.uuid4()
    return str(random_uuid)

class LocationItem(BaseModel):
    longitude: float
    latitude: float
    data: str
