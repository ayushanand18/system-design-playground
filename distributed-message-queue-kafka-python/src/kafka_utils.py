"""
Kafka Utility Functions
"""
from datetime import datetime
from .utils import MessageItem, generate_uuid

async def kafka_create_message(message: MessageItems):
    """Create a Kafka Message on the topic"""
    id = generate_uuid()
    item = {
        'timestamp': message.timestamp,
        'title': message.item,
        'body': message.body,
        'author': message.author,
        'created_at': datetime.now(),
        'id': id,
    }
    try:
        pass
        # write to kafka
        # await kafka.write()
    except BaseException as error:
        raise HTTPException(status_code=404, detail=str(error))
    
    return id

async def kafka_poll_message(topic: str) -> MessageItem:
    """Poll the next message from the queue on the topic"""
    pass