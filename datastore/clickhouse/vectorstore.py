import json
from uuid import uuid4

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import (
    Clickhouse, 
    ClickhouseSettings
)
from langchain_openai import OpenAIEmbeddings

class ClickhouseClient:
    def __init__(self, 
        host: str,
        port: int,
        username: str,
        database: str,
        table: str
    ) -> None:
        self.client = Clickhouse(
            embedding=HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-mpnet-base-v2"
            ),
            config=ClickhouseSettings(
                host=host,
                port=port,
                username=username,
                database=database,
                table=table
            )
        )

    def write_document(self, data: dict) -> None:
        # embed data using embedding model then store to vector store
        sentence = f'Sensor {data["sensor"]} at {data["time"]} reported a temperature of {data["temp"]}, humidity of {data["hum"]}, gyro with values {data["gyro"]}, and an acceleration of {data["accel"]}.'
        document = Document(
            page_content=sentence,
            metadata={
                "source": data["sensor"], 
                "time": data["time"]
            }
        )
        self.client.add_documents(documents=[document])
    