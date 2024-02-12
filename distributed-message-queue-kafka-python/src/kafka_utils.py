"""
Kafka Utility Functions
"""

from confluent_kafka import Producer, Consumer
from datetime import datetime
import socket

from .utils import MessageItem, generate_uuid

prod_conf = {'bootstrap.servers': 'host1:9092,host2:9092',
        'client.id': socket.gethostname()}
cons_conf = {'bootstrap.servers': 'host1:9092,host2:9092',
        'group.id': 'foo',
        'auto.offset.reset': 'smallest'}

consumer = Consumer(cons_conf)
producer = Producer(prod_conf)

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
        producer.produce(message.topic, key=id, value=item)
    except BaseException as error:
        raise HTTPException(status_code=404, detail=str(error))
    
    return id

async def kafka_poll_message(topic: str) -> MessageItem:
    """Poll the next message from the queue on the topic"""
    return await consume_loop(topic)

def consume_loop(topics):
    try:
        consumer.subscribe(topics)
        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
                yield msg
    finally:
        consumer.close()