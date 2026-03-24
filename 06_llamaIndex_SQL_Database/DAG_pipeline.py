#Earlier LlamaIndex had QueryPipeline with DAG support, but now DAGs are implemented by orchestrating modular components manually or using agent/workflow frameworks. Each node represents a function like prompt → LLM → post-processing, and outputs are merged.

from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model="gpt-3.5-turbo")

# Step 1: Input
query = "Get all movies released after 2000"

# Step 2A: SQL Generator branch
sql_prompt = PromptTemplate("""
Convert the following question into SQL:
Question: {query}
""")

sql_query = llm.complete(sql_prompt.format(query=query))

# Step 2B: Explanation branch
explain_prompt = PromptTemplate("""
Explain the following question in simple terms:
Question: {query}
""")

explanation = llm.complete(explain_prompt.format(query=query))

# Step 3: Combine outputs
final_output = f"""
SQL Query:
{sql_query}

Explanation:
{explanation}
"""

print(final_output)