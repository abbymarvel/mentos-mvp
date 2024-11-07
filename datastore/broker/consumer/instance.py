import json

from kafka import KafkaConsumer

from config.logging import Logger
from config.utils import get_env_value
from clickhouse.vectorstore import ClickhouseClient
from sql.postgresql import PostgreSQLClient



class Consumer:
    def __init__(self, broker: str, topic: str, vector_store: ClickhouseClient = None, db: PostgreSQLClient = None) -> None:
        self.KAFKA_SERVER = broker
        self.KAFKA_TOPIC = topic
        self.instance = None
        self.vector_store = vector_store
        self.db = db
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
                data = message.value
                x = data['gyro']
                y = data['accel']
                query = f"""
                    INSERT INTO {get_env_value('TABLE_NAME')} (sensor, time, temp, hum, gyro, accel)
                    VALUES({data['sensor']}, '{data['time']}', {data['temp']}, '{data['hum']}', '{self.db.to_sql_array(data['gyro'])}', '{self.db.to_sql_array(data['accel'])}')
                """
                self.db.query(query)
        except Exception as e:
            self.logger.error(f" [x] Failed to consume message: {e}")
        finally:
            # close the consumer 
            self.instance.close()
