from llama_index.llms.openai import OpenAI
from llama_index.core import settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = api_key

settings.LLM= OpenAI(temperature=0.2,model="gpt-3.5-turbo",max_retries=3)

documents = SimpleDirectoryReader('data').load_data()
index=VectorStoreIndex.from_documents(documents)

print (f"number of documents in the index: {len(documents)}")
print(f"Display a document in the index: {documents[25].get_text()}")
print("-------------------------------")

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10
)

respose_synthesizer = get_response_synthesizer(response_mode=ResponseMode.COMPACT)

query_engine=RetrieverQueryEngine(retriever=retriever,mode_postprocessor=SimilarityPostprocessor(similarity_cutoff=0.7,filter_empty=True,filter_duplicates=True,filter_similar=True),respose_synthesizer=respose_synthesizer,)
response = query_engine.query("What are the main topics covered in the documents?")
print(response)
