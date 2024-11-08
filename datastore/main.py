from broker.consumer.instance import Consumer
from clickhouse.vectorstore import ClickhouseClient
from config.utils import setup_env, get_env_value
from sql.postgresql import PostgreSQLClient


if __name__ == '__main__':

    setup_env()

    KAFKA_BROKER = get_env_value('KAFKA_BROKER')
    KAFKA_TOPIC = get_env_value('KAFKA_TOPIC')

    sql_client = PostgreSQLClient(
        host=get_env_value("DB_HOST"),
        port=get_env_value("DB_PORT"),
        user=get_env_value("DB_USER"),
        password=get_env_value("DB_PASSWORD"),
        database=get_env_value("DB_NAME")
    )

    consumer = Consumer(
        broker=KAFKA_BROKER, 
        topic=KAFKA_TOPIC,
        # vector_store=clickhouse_client
        db=sql_client
    )


    try:
        consumer.create_instance()
        consumer.consume()
    except KeyboardInterrupt:
        exit(1)

