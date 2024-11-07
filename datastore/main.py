from broker.consumer.instance import Consumer
from clickhouse.vectorstore import ClickhouseClient
from config.utils import setup_env, get_env_value


if __name__ == '__main__':

    setup_env()

    KAFKA_BROKER = get_env_value('KAFKA_BROKER')
    KAFKA_TOPIC = get_env_value('KAFKA_TOPIC')

    CLICKHOUSE_HOST=get_env_value("CLICKHOUSE_HOST")
    CLICKHOUSE_PORT=get_env_value("CLICKHOUSE_PORT")
    CLICKHOUSE_USERNAME=get_env_value("CLICKHOUSE_USERNAME")
    # CLICKHOUSE_PASSWORD=get_env_value("CLICKHOUSE_PASSWORD")
    CLICKHOUSE_DATABASE=get_env_value("CLICKHOUSE_DATABASE")
    CLICKHOUSE_TABLE=get_env_value("CLICKHOUSE_TABLE")


    clickhouse_client = ClickhouseClient(
        host=CLICKHOUSE_HOST,
        port=CLICKHOUSE_PORT,
        username=CLICKHOUSE_USERNAME,
        database=CLICKHOUSE_DATABASE,
        table=CLICKHOUSE_TABLE
    )

    consumer = Consumer(
        broker=KAFKA_BROKER, 
        topic=KAFKA_TOPIC,
        vector_store=clickhouse_client
    )


    try:
        consumer.create_instance()
        consumer.consume()
    except KeyboardInterrupt:
        exit(1)

