#I built a pipeline where an LLM converts user queries into pandas operations, executes them on a dataframe, and then synthesizes a natural language response. This mimics a structured DAG pipeline with generation, execution, and interpretation stages
import pandas as pd
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv

# ---------------------------
# Setup
# ---------------------------
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model="gpt-3.5-turbo")

# ---------------------------
# Step 1: Create DataFrame
# ---------------------------
data = {
    "movie": ["Inception", "The Matrix", "Interstellar", "Avatar"],
    "year": [2010, 1999, 2014, 2009],
    "rating": [8.8, 8.7, 8.6, 7.8],
    "revenue": [829, 463, 677, 2923]
}

df = pd.DataFrame(data)

# ---------------------------
# Step 2: Pandas Instruction Prompt
# ---------------------------
pandas_prompt = PromptTemplate("""
You are a pandas expert.

Given a user query, generate ONLY valid pandas code (no explanation).
The dataframe is named df.

Query: {query}
""")

# ---------------------------
# Step 3: Generate Pandas Code
# ---------------------------
user_query = "Get movies with rating above 8.7"

pandas_code = llm.complete(
    pandas_prompt.format(query=user_query)
).text.strip()

print("\nGenerated Pandas Code:\n", pandas_code)

# ---------------------------
# Step 4: Execute Pandas Code (Parser)
# ---------------------------
local_vars = {"df": df}

try:
    result = eval(pandas_code, {}, local_vars)
except Exception as e:
    result = str(e)

print("\nExecution Result:\n", result)

# ---------------------------
# Step 5: Response Synthesis Prompt
# ---------------------------
synthesis_prompt = PromptTemplate("""
You are a helpful assistant.

Given the user query and the dataframe result, generate a clear natural language response.

Query: {query}
Result: {result}
""")

final_response = llm.complete(
    synthesis_prompt.format(query=user_query, result=result)
)

print("\nFinal Response:\n", final_response.text)