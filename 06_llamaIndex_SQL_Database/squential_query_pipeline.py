from llama_index.core.query_pipeline import QueryPipeline #QueryPipeline is deprecated/removed in newer versions (0.14+)
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key=os.getenv("OpenAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

prompt_str = "You are a helpful assistant for converting natural language questions into SQL queries."
prompt_tmpl=PromptTemplate(prompt_str)
llm=OpenAI(model="gpt-3.5-turbo")

p = QueryPipeline (chain=[prompt_tmpl, llm],verbose=True)

response=p.run(movie_name="The Matrix")

print(response)
