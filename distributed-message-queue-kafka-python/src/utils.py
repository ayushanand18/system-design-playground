from pydantic import BaseModel
import uuid

class MessageItem(BaseModel):
    id: str
    created_at: int
    timestamp: int
    topic: str
    author: str
    title: str
    body: str

class MessageItems(BaseModel):
    timestamp: int
    topic: str
    author: str
    title: str
    body: str

def generate_uuid() -> str:
    """Generate a unique identifier for a user session"""
    random_uuid = uuid.uuid4()
    return str(random_uuid)