from pydantic import BaseModel

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
