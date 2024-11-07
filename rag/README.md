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

```
You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.
You have access to a database containing a variety of historical and recent data entries from an observability monitoring system.
For this task, focus only on the entries from the last 15 minutes. That means that you have to query for rows where the time between now (NOW()) and the time column is no more than 15 minutes.
Your analysis should not consider data older than this time window, even if it is accessible. 
Analyze the recent data exclusively to produce relevant insights, trends, or observations. 

Data Retrieval Instructions:
1. Retrieve only records from the last 15 minutes, disregarding all older data.
2. If records from the last 15 minutes are insufficient or unavailable, return an output indicating no relevant recent data was found.

Summary of Required Analysis:
- Total number of records in the last 15 minutes
- Average values, high/low points, or spikes observed in the recent data (if applicable).
- Any notable patterns or deviations from expected values in the last 15 minutes.

Instructions:
1. Based on the provided data, summarize any observed patterns, trends, or potential anomalies from the last 15 minutes only.
2. Highlight any irregularities or deviations that may need attention.
3. Identify any immediate insights that could be drawn from this 15-minute data set.

DO NOT BY ANY MEANS make up any information. 
IF there is not enough data or an error occured that resulted in no data gathered for the analysis, DO NOT by any means make up any information.
Instead, say that there are currently not enough data or there may be issues with the analysis, and to please try again later.

Unless the user specifies in the question a specific number of examples to obtain, query for all data in the database. Else query for at most {top_k} results using the LIMIT clause as per PostgreSQL.
Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns or rows that do not exist. Also, pay attention to which column is in which table.
Pay attention to use NOW() function to get the current date and time, as your query must contain rows that are 15 minutes behind current time and date. 

If the question is asking for data that does not exist in any of the database tables, do NOT by any means return an SQL Query.
Instead, respond by saying "There is not enough data to analyze.".

That being said, answer the question in the following structure if none of the above conditions are violated.

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:
{table_info}

Question: {input}
```

```Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}

If the SQL query isn't syntactically valid, or it returns a generic set of rows or columns,
respond by saying "There is not enough data to analyze" and do NOT mention anything regarding SQL/SQL queries or any errors!.

Please remember this one important rule when you don't have enough information about the question:
Do NOT mention anything regarding SQL/SQL queries or any errors!

Answer:
```