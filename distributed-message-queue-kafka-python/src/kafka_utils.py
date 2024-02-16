"""
Kafka Utility Functions
"""

from fastapi import HTTPException
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
from typing import Optional

from .utils import MessageItem, generate_uuid, MessageItems

load_dotenv()

KAFKA_ADDR = os.getenv("KAFKA_ADDR")
KAFKA_GRP = os.getenv("KAFKA_GRP")

producer = KafkaProducer(bootstrap_servers=KAFKA_ADDR)

async def kafka_create_message(message: MessageItems):
    """Create a Kafka Message on the topic"""
    id = generate_uuid()
    item = {
        'timestamp': message.timestamp,
        'title': message.title,
        'body': message.body,
        'author': message.author,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'id': id,
    }
    try:
        producer.send(message.topic, key=id.encode(), value=str(item).encode())
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
    return {"id": id}

async def kafka_poll_message(topic: str) -> Optional[MessageItem]:
    """Poll the next message from the queue on the topic"""
    consumer = KafkaConsumer(topic, bootstrap_servers=KAFKA_ADDR, group_id=KAFKA_GRP)
    try:
        message = next(consumer)
    except StopIteration:
        raise HTTPException(status_code=404, detail="No messages available in the topic")
    
    message_value = message.value.decode('utf-8')
    message_data = eval(message_value)  # This is a simple way to convert string dictionary to dictionary. Ensure data integrity in production.

    return MessageItem(**message_data)
