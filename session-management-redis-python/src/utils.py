"""Utility functions"""

import uuid

def generate_uuid() -> str:
    """Generate a unique identifier for a user session"""
    random_uuid = uuid.uuid4()
    return uuid_str