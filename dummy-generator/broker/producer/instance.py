import json
import random
import time

from datetime import datetime

from config.logging import Logger

from kafka import KafkaProducer
from kafka.errors import KafkaError


class Producer:
    def __init__(self, broker: str, topic: str) -> None:
        self.KAFKA_SERVER = broker
        self.KAFKA_TOPIC = topic
        self.instance = None
        self.logger = Logger().setup_logger(service_name='producer')

    def create_instance(self) -> KafkaProducer:
        """
        Creates new kafka producer and returns an instance of KafkaProducer.
        """
        self.instance = KafkaProducer(
            bootstrap_servers=self.KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),  # JSON serialization
            api_version=(0,11,5)
        )
        return self.instance

    def is_kafka_connected(self) -> bool:
        """
        Check if the Kafka cluster is available by fetching metadata.
        """
        try:
            metadata = self.instance.bootstrap_connected()
            if metadata:
                self.logger.info(" [*] Connected to Kafka cluster successfully!")
                return True
            else:
                self.logger.error(" [x] Failed to connect to Kafka cluster.")
                return False
        except KafkaError as e:
            self.logger.error(f" [x] Kafka connection error: {e}")
            return False

    def ensure_bytes(self, message) -> bytes:
        """
        Ensure the message is in byte format.
        """
        if not isinstance(message, bytes):
            return bytes(message, encoding='utf-8')
        return message
    
    def produce(self) -> None:
        """
        Produces 10.000 messages with a delay of 1 second.
        """
        try:
            for _ in range(10000):
                # generate current timestamp
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                
                # create sensor data with random values
                sensor_data = {
                    "sensor": str(random.randint(1, 4)),  # sensor ID between 1 and 4
                    "time": current_time,
                    "temp": str(random.randint(20, 35)),  # temperature between 20 and 35
                    "hum": str(random.randint(30, 70)),   # humidity between 30 and 70
                    "gyro": [random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 150)],
                    "accel": [random.uniform(0, 5), random.uniform(0, 5), random.uniform(0, 5)]
                }
                
                # inject an outlier with low probability
                if random.random() < 0.001:  # approximately 1 out of 1000 chance
                    sensor_data["temp"] = str(random.randint(100, 150))  # outlier temperature
                    sensor_data["gyro"] = [random.uniform(100, 200), random.uniform(100, 200), random.uniform(100, 200)]
                    sensor_data["accel"] = [random.uniform(10, 20), random.uniform(10, 20), random.uniform(10, 20)]
                
                # send the sensor data to kafka
                self.instance.send(
                    self.KAFKA_TOPIC, 
                    value=sensor_data
                )

                self.logger.info(f" [*] Sent data to Kafka: {sensor_data}")
                
                # wait for a random interval between 0 and 3 seconds before generating the next log
                time.sleep(random.uniform(0, 3))
        except:
            self.logger.info(" [*] Stopping data generation.")
        finally:
            # close the kafka producer
            self.instance.close()
