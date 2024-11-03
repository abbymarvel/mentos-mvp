from config.logging import Logger

from kafka import KafkaConsumer


class Consumer:
    def __init__(self, broker: str, topic: str) -> None:
        self.KAFKA_SERVER = broker
        self.KAFKA_TOPIC = topic
        self.instance = None
        self.logger = Logger().setup_logger(service_name='consumer')
    
    def create_instance(self) -> KafkaConsumer:
        """
        Creates new kafka consumer and returns an instance of KafkaConsumer.
        """
        self.instance = KafkaConsumer(
            self.KAFKA_TOPIC,
            bootstrap_servers=self.KAFKA_SERVER,
            api_version=(0,9) # enables full group coordination features with automatic partition assignment and rebalancing,
        )
        return self.instance
    
    def consume(self) -> None:
        """
        Consume messages indefinitely with a delay of 1 second
        """
        self.logger.info(" [*] Starting Kafka Consumer...")
        try:
            for message in self.instance:
                self.logger.info(f" [*] Received: {message}")
        except Exception as e:
            self.logger.error(f" [x] Failed to consume message: {e}")
        finally:
            # close the consumer 
            self.instance.close()
