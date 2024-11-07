from langchain_community.vectorstores import Clickhouse
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI


class LLMQuery:
    """
    Initializes connection to DB for LLM to create queries according to user questions.
    """
    
    def __init__(
        self,
        vector_store: Clickhouse,
        together_endpoint: str, 
        together_api_key: str, 
        together_llm_model: str,
        template: str
    ):
        self.llm = ChatOpenAI(
            base_url=together_endpoint,
            api_key=together_api_key,
            model=together_llm_model,
            temperature=0,
            verbose=True
        )
        self.template = template
        self.vector_store = vector_store

    def write_query(self) -> VectorStoreRetriever:
        return self.vector_store.as_retriever(
            search_type="similarity",
        )

    # DEPRECATED
    def execute_query(self):
        return self.write_query.invoke()