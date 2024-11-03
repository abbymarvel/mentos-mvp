import os

from dotenv import load_dotenv

from broker.producer.instance import Producer
from broker.consumer.instance import Consumer


if __name__ == '__main__':
    load_dotenv()

    KAFKA_BROKER = os.getenv('KAFKA_BROKER')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

    consumer = Consumer(
        KAFKA_BROKER, KAFKA_TOPIC
    )

    try:
        consumer.create_instance()
        consumer.consume()
    except KeyboardInterrupt:
        exit(1)

