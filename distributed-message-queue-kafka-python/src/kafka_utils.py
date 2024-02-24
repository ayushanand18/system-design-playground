"""
Kafka Utility Functions
"""

from fastapi import HTTPException
from kafka import KafkaAdminClient, KafkaProducer, KafkaConsumer
from aiokafka import AIOKafkaConsumer
from datetime import datetime
import sys
import os
from dotenv import load_dotenv
from typing import Optional

from .utils import MessageItem, generate_uuid, MessageItems

load_dotenv()

KAFKA_ADDR = os.getenv("KAFKA_ADDR")
KAFKA_GRP = os.getenv("KAFKA_GRP")
KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
KAFKA_TOPIC = 'your_topic'

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
    return MessageItem(await consume_kafka(topic))

async def consume_kafka(topic):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_ADDR,
        group_id=KAFKA_GRP,
        auto_offset_reset='latest',  # Set to 'latest' to read only latest messages
        enable_auto_commit=False
    )

    await consumer.start()

    
    async for msg in consumer:
        yield msg.value.decode('utf-8')
    
    await consumer.stop()
