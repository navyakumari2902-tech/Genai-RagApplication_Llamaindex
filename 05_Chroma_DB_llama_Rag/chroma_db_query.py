#description : This code is used to crate a chromadb vectorindex and upload the documents to the index
#after ,it queries the index with llamaindex and return the response



import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex,SimpleDirectoryReader
from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("Google_API_KEY")
os.environ["GOOGLE_API_KEY"]=api_key


context_window=4096
num_output=200

Settings.llm = OpenAI(model ="gpt-3.5-turbo",temperature=0.7, max_tokens=num_output,context_window=context_window)

"""
settings.llm=Gemini(
    model="gemini-1.5-pro",
    temperature=0.7,
    max_tokens=num_output,
    context_window=context_window,
    )
"""
documents = SimpleDirectoryReader('data').load_data()

print("Number of documents:", len(documents))

#intialize chromadb persistent client,path to save data 
db=chromadb.PersistentClient(path="./chroma_db")

#create a collection in chromadb to store the vector embeddings of the documents                            
chroma_collection = db.get_or_create_collection("quickstart")
#assign chroma as the vector store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context=StorageContext.from_defaults(vector_store=vector_store)

#ceate your index
index =VectorStoreIndex.from_documents(documents,storage_context=storage_context)

#create a query engine and query
query_engine = index.as_query_engine()
response = query_engine.query("What is the capital of France?")
print("Response:", response)
                             