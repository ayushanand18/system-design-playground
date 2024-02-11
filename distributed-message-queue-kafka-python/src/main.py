"""
Distributed Message Queue using Kafka
"""

from fastapi import FastAPI
from .utils import MessageItem, MessageItems
from .kafka_utils import kafka_create_message, kafka_poll_message

app = FastAPI()

@app.post("/message/create")
async def create_message(message_items: MessageItems) -> dict:
    """Create a new message into Kafka"""
    try:
        for message in message_items:
            await kafka_create_message(message)
    except BaseException as error:
        logging.error(f"Error: {str(error)}")

@app.get("/message/poll/{topic}")
async def poll_message(topic: str) -> MessageItem:
    """Poll a new message from the distributed queue for the topic"""
    try:
        return await kafka_poll_message(topic)
    except BaseException as error:
        logging.error(f"Error: {str(error)}")
