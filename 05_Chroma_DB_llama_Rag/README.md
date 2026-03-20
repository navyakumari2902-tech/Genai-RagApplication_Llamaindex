# Querying a Chroma Vector Database with LlamaIndex

This repository demonstrates how to query a Chroma vector database using LlamaIndex.
The example shows how embeddings stored in a vector database can be retrieved to answer a query.

This project is part of my LlamaIndex and Generative AI learning journey, where I experiment with core RAG components such as vector databases, embeddings, and retrieval pipelines.

# Overview

Vector databases are a key component of Retrieval Augmented Generation (RAG) systems. They store document embeddings and allow semantic search over large datasets.

In this example, the workflow demonstrates:

Creating a Chroma vector database

Storing document embeddings

Retrieving relevant documents using a query

Using LlamaIndex to interact with the vector store

# Technologies Used

Python

LlamaIndex

ChromaDB

OpenAI Embeddings

# Project Structure
chroma-vector-query-llamaindex
│
├── chroma_db_query.py
└── README.md

The repository contains a single Python script that demonstrates querying a Chroma vector database.

# Implementation Logic

The script demonstrates the following workflow:

1. Load Documents

Documents are loaded into the system using a document reader.

2. Create Embeddings

Text is converted into vector embeddings using an embedding model.

3. Store Embeddings in ChromaDB

The embeddings are stored inside a Chroma vector database.

4. Create Vector Index

LlamaIndex creates a VectorStoreIndex on top of the Chroma vector database.

5. Query the Index

A query is executed against the vector store to retrieve relevant information.

Example Code
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext
import chromadb

# create chroma client
chroma_client = chromadb.Client()

# create collection
chroma_collection = chroma_client.create_collection("example_collection")

# create vector store
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# create storage context
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# load documents
documents = SimpleDirectoryReader("data").load_data()

# create index
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)

# create query engine
query_engine = index.as_query_engine()

# query
response = query_engine.query("What is this document about?")

print(response)

# Installation

Install required dependencies:

pip install llama-index
pip install chromadb
pip install openai
Running the Script

Run the script using:

python chroma_db_query.py

# Known Issue

This script may encounter the following error when running:

RateLimitError: Error code 429
You exceeded your current quota
Why This Happens

The example uses OpenAI embeddings, which require:

A valid API key

Available API quota

Active billing

If the quota is exceeded or billing is not enabled, the API returns a 429 rate limit error.

# Possible Solutions

To resolve this issue:

1. Set your OpenAI API key

Linux / Mac

export OPENAI_API_KEY="your_api_key"

Windows PowerShell

setx OPENAI_API_KEY "your_api_key"
2. Enable OpenAI billing

Check your quota and billing settings on the OpenAI dashboard.

3. Use a local embedding model

Instead of OpenAI embeddings, a local embedding model such as SentenceTransformers can be used.

#Learning Objective

This example helps understand:

Vector databases in RAG systems

How embeddings are stored and retrieved

Integration of ChromaDB with LlamaIndex

Querying vector indexes using semantic search

# Repository Purpose

This repository is part of my hands-on exploration of LlamaIndex and Retrieval Augmented Generation, where I experiment with:

Vector databases

RAG pipelines

LLM evaluation

Prompt and retrieval workflows