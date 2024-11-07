from langchain_community.vectorstores import (
    Clickhouse,
    ClickhouseSettings
)
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings

from rag.query import LLMQuery
from rag.response import LLMResponse

from config.utils import (
    setup_env, 
    get_env_value
)


TEMPLATE = '''Context:
You have access to a database containing a variety of historical and recent data entries from an observability monitoring system.
For this task, focus only on the entries from the last 15 minutes. 
Your analysis should not consider data older than this time window, even if it is accessible. 
Analyze the recent data exclusively to produce relevant insights, trends, or observations. 

Data Retrieval Instructions:
1. Retrieve only records from the last 15 minutes, disregarding all older data.
2. If records from the last 15 minutes are insufficient or unavailable, return an output indicating no relevant recent data was found.

Summary of Required Analysis:
- Total number of records in the last 15 minutes: {total_recent_records}
- Average values, high/low points, or spikes observed in the recent data (if applicable).
- Any notable patterns or deviations from expected values in the last 15 minutes.

Sample of Recent Data (last 15 minutes):
{recent_data_sample}  # Replace this with a subset of relevant data points (e.g., last 5-10 entries in the time window) to provide context to the LLM.

Instructions:
1. Based on the provided data, summarize any observed patterns, trends, or potential anomalies from the last 15 minutes only.
2. Highlight any irregularities or deviations that may need attention.
3. Identify any immediate insights that could be drawn from this 15-minute data set.

Question: {input}
---

End of Instructions
'''


answer_prompt = PromptTemplate.from_template(
    """Given the following user question, answer the user question in the following format:
- Summary: A sentence or short paragraph, describing the observations, trends, and others from the last 15 minutes.
- Key Insights and Actions: A list of insights/observation/issues and actions that can be done if any to mitigate or handle any issues gathered from the analysis.

Answer: """
)


# load environment variables
setup_env()

# setup clickhouse
settings = ClickhouseSettings(
    host=get_env_value("CLICKHOUSE_HOST"),
    port=get_env_value("CLICKHOUSE_PORT"),
    username=get_env_value("CLICKHOUSE_USERNAME"),
    password=get_env_value("CLICKHOUSE_PASSWORD"),
    database=get_env_value("CLICKHOUSE_DATABASE"),
    table=get_env_value("CLICKHOUSE_TABLE")
)
vector_store = Clickhouse(OpenAIEmbeddings(), config=settings)

llm_query = LLMQuery(
    vector_store=vector_store,
    together_endpoint=get_env_value("TOGETHER_ENDPOINT"),
    together_api_key=get_env_value("TOGETHER_API_KEY"),
    together_llm_model=get_env_value("TOGETHER_LLM_MODEL"),
    template=TEMPLATE
)

llm_response = LLMResponse(
    answer_prompt=answer_prompt,
    llm_query=llm_query
)

QUESTION = """Can you generate me an analysis gathered from the vector store database from the last 15 minutes?

Summary of Required Analysis:
- Total number of records in the last 15 minutes
- Average values, high/low points, or spikes observed in the recent data (if applicable).
- Any notable patterns or deviations from expected values in the last 15 minutes.

Answer in a paragraph containing the summary of the analysis, then a list of key insights from the required analysis and any actions (if any) that can be taken to mitigate any issues.
"""

print(llm_response.get_response(QUESTION))
