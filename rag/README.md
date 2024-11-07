https://hub.docker.com/r/clickhouse/clickhouse-server/
https://python.langchain.com/docs/integrations/vectorstores/clickhouse/
https://grafana.com/grafana/plugins/grafana-clickhouse-datasource/
https://clickhouse.com/docs/knowledgebase/vector-search
https://python.langchain.com/docs/integrations/llms/together/
https://python.langchain.com/docs/tutorials/rag/

## Quickstart

1. Run Clickhouse (docker image):

    ```
    docker run -d -p 8123:8123 -p9000:9000 --name langchain-clickhouse-server --ulimit nofile=262144:262144 clickhouse/clickhouse-server:latest
    ```

2. Connect to Clickhouse instance & create table (if not present):
   
    ```
    docker exec -it langchain-clickhouse-server clickhouse-client
    ```

    ```
    CREATE TABLE sensor_data
    (
        `sensor` String,
        `time` DateTime64(3),
        `temp` Float32,
        `hum` Float32,
        `gyro` Array(Float32),
        `accel` Array(Float32)
    )
    ENGINE = MergeTree
    ORDER BY (time, sensor)
    PRIMARY KEY (time);
    ```

3. adwe
4. 