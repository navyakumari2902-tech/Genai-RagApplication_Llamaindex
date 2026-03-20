import os
from llama_index.core import SimpleDirectoryReader
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from dotenv import load_dotenv
load_dotenv()
from llama_index.llms.google_genai import GoogleGenAI
from llama_index import SimpleDirectoryReader, vector_store_index_from_documents

# create the LLM instance (Google GenAI key must be set in .env)
llm = GoogleGenAI(model="gemini-2.5-flash-lite")

# load documents and build a vector index; supply the llm if needed
# you can also use VectorStoreIndex.from_documents(documents, llm=llm)

documents = SimpleDirectoryReader('data').load_data()
index = vector_store_index_from_documents(documents, llm=llm)

print(f"built index from {len(documents)} documents")

retriever=VectorIndexRetriever(index=index,similarity_top_k=10)

query_engine=RetrieverQueryEngine(retriever=retriever)

response=query_engine.query("What is the document about?")
print(response)