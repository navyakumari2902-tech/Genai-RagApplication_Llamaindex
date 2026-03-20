# LlamaIndex RAG Learning Project – Iteration 1

A hands-on learning project exploring Retrieval-Augmented Generation (RAG) using LlamaIndex and OpenAI GPT models.
A hands-on learning project exploring Retrieval-Augmented Generation (RAG) using LlamaIndex and OpenAI GPT models.

This repository documents my learning journey while understanding how RAG systems work internally, including retrievers, post-processing, and response synthesis.

## 🎯 Project Objective

This project builds a custom RAG pipeline (without using high-level shortcuts) to understand how each component works individually.

The system:

- Loads documents from a local folder
- Creates vector embeddings using OpenAI
- Retrieves relevant document chunks
- Filters low-quality matches
- Generates answers using GPT-3.5-turbo

This is a single-query RAG implementation (no chat memory yet).

## 🧠 What is RAG?

**RAG = Retrieval-Augmented Generation**

Instead of relying only on the model's training data:

- Relevant documents are retrieved from a knowledge base
- These documents are provided as context to the LLM
- The LLM generates answers grounded in retrieved data

This improves:

- Accuracy
- Traceability
- Domain-specific responses

## 🏗️ Architecture (Actual Implementation)

This project manually wires the RAG components instead of using `.as_query_engine()`.

```
User Query
    │
    ▼
VectorIndexRetriever
    │
    ▼
SimilarityPostprocessor (filters low-quality matches)
    │
    ▼
ResponseSynthesizer (COMPACT mode)
    │
    ▼
GPT-3.5-turbo
    │
    ▼
Final Response
```

## 🔬 Implementation Details

### 1️⃣ LLM Configuration
```python
settings.LLM = OpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",
    max_retries=3
)
```

- Low temperature → more deterministic responses
- `max_retries=3` → handles API rate limit errors (HTTP 429)

### 2️⃣ Document Loading
```python
documents = SimpleDirectoryReader("data").load_data()
```

- Loads .txt, .pdf, .md
- Converts them into LlamaIndex Document objects

### 3️⃣ Vector Index Creation
```python
index = VectorStoreIndex.from_documents(documents)
```

Internally:
- Documents are chunked
- Each chunk is converted into embeddings
- Stored in a vector index for semantic search

### 4️⃣ Custom Retriever
```python
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10
)
```

- Retrieves top 10 semantically similar chunks
- Gives fine-grained control over retrieval behavior

### 5️⃣ Post Processing (Important Learning)
```python
SimilarityPostprocessor(
    similarity_cutoff=0.7,
    filter_empty=True,
    filter_duplicates=True,
    filter_similar=True
)
```

This filters:
- Low similarity matches
- Empty responses
- Duplicate chunks
- Near-duplicate content

This improves final response quality.

### 6️⃣ Response Synthesizer
```python
get_response_synthesizer(
    response_mode=ResponseMode.COMPACT
)
```

**COMPACT mode:**
- Merges context efficiently
- Reduces token usage
- Optimizes cost

## 📦 Prerequisites

- Python 3.8+
- OpenAI API key
- pip

## 🚀 Setup Instructions

### 1️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Add Environment Variable

Create a `.env` file:

```env
OPENAI_API_KEY=sk-your-key-here
```

⚠️ Do not commit `.env` to git.

### 4️⃣ Add Documents

Create a `data/` folder and add:

- .txt
- .pdf
- .md

### 5️⃣ Run the Program
```bash
python program.py
```

## ⚠️ Issue Encountered During Learning

### HTTP 429 – Too Many Requests

**Cause:**
- OpenAI rate limits
- Embedding creation makes multiple API calls

**Solution:**
- Added `max_retries=3`
- Upgraded to paid OpenAI tier
- Reduced dataset size during testing

## 📚 Learning Insights

### 1️⃣ Embeddings Enable Semantic Search

Text → vectors → similarity comparison. This allows meaning-based retrieval, not keyword matching.

### 2️⃣ Retrieval Quality Affects Generation Quality

Better retrieval = better final answer.

`similarity_top_k` and `similarity_cutoff` directly impact output quality.

### 3️⃣ Post-Processing Matters

Filtering duplicates and low-score chunks significantly improves response clarity.

### 4️⃣ API Rate Limiting is Real

Building LLM systems requires:
- Retry logic
- Cost awareness
- Token budgeting

## 📌 Current Status

**Iteration 1** – Single Query RAG

**Focus:** Understanding retriever + synthesizer pipeline

## 🔜 Next Learning Steps

- Add multi-turn conversation support (ChatEngine + memory)
- Experiment with hybrid search (BM25 + vector)
- Add evaluation metrics for retrieval quality
- Explore streaming responses

## 🛠️ Technologies Used

- LlamaIndex
- OpenAI GPT-3.5-turbo
- OpenAI Embeddings
- Python-dotenv
- Python

## 📂 Project Structure

```
02_rag_with_retrieval_and_postprocessing/
│
├── program.py              # Main RAG application
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── .env                   # ⚠️ Environment variables (NOT in git)
├── .gitignore            # Git ignore rules
│
├── data/                 # 📁 Your documents go here
│   ├── document1.txt
│   ├── document2.pdf
│   └── document3.md
│
└── .venv/               # Virtual environment (NOT in git)
```

## 📝 Note

This is a structured learning project focused on understanding RAG internals step-by-step rather than building a production-ready system.

