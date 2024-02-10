"""
Distributed Message Queue using Kafka
"""

from fastapi import FastAPI
from .utils import MessageItem, MessageItems

app = FastAPI()

@app.post("/message/create")
async def create_message(message_items: MessageItems):
    """Create a new message into Kafka"""
    pass

@app.get("/message/poll/{topic}")
async def poll_message(topic: str) -> MessageItem:
    """Poll a new message from the distributed queue for the topic"""
    pass
