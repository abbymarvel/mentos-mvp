import os

from dotenv import load_dotenv

from broker.producer.instance import Producer


if __name__ == '__main__':
    load_dotenv()

    KAFKA_BROKER = os.getenv('KAFKA_BROKER')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

    producer = Producer(
        KAFKA_BROKER, KAFKA_TOPIC
    )

    try:
        producer.create_instance()
        producer.produce()
    except KeyboardInterrupt:
        exit(1)
