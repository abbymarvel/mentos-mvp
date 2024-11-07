import json

from config.logging import Logger
from clickhouse.vectorstore import ClickhouseClient

from kafka import KafkaConsumer


class Consumer:
    def __init__(self, broker: str, topic: str, vector_store: ClickhouseClient) -> None:
        self.KAFKA_SERVER = broker
        self.KAFKA_TOPIC = topic
        self.instance = None
        self.vector_store = vector_store
        self.logger = Logger().setup_logger(service_name='consumer')
    
    def create_instance(self) -> KafkaConsumer:
        """
        Creates new kafka consumer and returns an instance of KafkaConsumer.
        """
        self.instance = KafkaConsumer(
            self.KAFKA_TOPIC,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            bootstrap_servers=self.KAFKA_SERVER,
            api_version=(0,9) # enables full group coordination features with automatic partition assignment and rebalancing,
        )
        return self.instance
    
    def consume(self) -> None:
        """
        Consume messages indefinitely with a delay of 1 second
        """
        self.logger.info(" [*] Starting Kafka consumer...")
        try:
            for message in self.instance:
                self.logger.info(f" [*] recv: {message}")
                # convert data to vector then store data in vector store
                self.vector_store.write_document(message.value)
        except Exception as e:
            self.logger.error(f" [x] Failed to consume message: {e}")
        finally:
            # close the consumer 
            self.instance.close()
