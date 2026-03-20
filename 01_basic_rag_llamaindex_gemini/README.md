# LlamaIndex + Google GenAI Integration

This repository serves as a working prototype and educational record for
integrating the [LlamaIndex](https://github.com/jerryjliu/llama_index) library
with Google's GenAI (Gemini) models. The goal is to demonstrate a complete
workflow — from environment setup and API key management to document ingestion,
vector indexing, and query handling — while cataloguing the lessons learned throughout the process. 

---

## Repository structure

```
llamarag/                 # project root (workspace folder)
├── .venv/                # Python virtual environment (excluded from VCS)
├── data/                 # sample documents to be indexed (text files)
├── test.py               # primary example script demonstrating LlamaIndex
├── check.py              # helper to enumerate available GenAI models
├── .env                  # environment variables (API key)
├── README.md             # this document
└── requirements.txt      # (optional) pinned dependencies
```

## 1. Python environment and dependency management

- Created a virtual environment in the project folder:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate
  ```
- Upgraded `pip` and installed packages inside the venv.
- Verified the environment with:
  ```powershell
  python -m pip list
  python -m pip show llama-index
  ```

> **Tip:** `python -c "import sys; print(sys.executable)"` shows the active
> interpreter, which should point to `.venv\Scripts\python.exe`.

## 2. API Key Management

- Stored the Google/GenAI key in a `.env` file in the project root:
  ```dotenv
  GOOGLE_API_KEY=your_real_api_key_here
  ```
  (no quotes or extra spaces)

- Installed `python-dotenv` and loaded the file at the top of scripts:
  ```python
  from dotenv import load_dotenv
  load_dotenv()
  ```

- Verified environment variable visibility using a one-liner and by
  printing in code:
  ```python
  print(os.getenv("GOOGLE_API_KEY"))
  ```

- If the key is not picked up automatically, explicitly pass it to the
  client:
  ```python
  client = Client(api_key=os.getenv("GOOGLE_API_KEY"))
  ```

## 3. Google GenAI Model Selection

- Attempted `gemini-1.5-flash` initially and received a `404 NOT_FOUND` error
  because the model wasn't available for the used API version.
- Added a small helper (`check.py`) to list available models using the client:
  ```python
  for m in client.models.list():
      print(m.name)
  ```
- Chose one of the listed names (`gemini-2.5-flash-lite` etc.) for further
  experiments.

## 4. Code overview (`test.py`)

`test.py` is the main script that exercises the LlamaIndex pipeline. Its logic
covers the following steps:

1. **Load environment variables** using `python-dotenv` so the GenAI API key is
  accessible.
2. **Initialize a language model** object (`GoogleGenAI`) with a valid Gemini
  model name.
3. **Read documents** from the `data/` directory via
  `SimpleDirectoryReader`.
4. **Build a vector store index** from the documents, passing in the LLM for
  optional pre-processing. This step triggers embedding generation.  
5. **Print a confirmation** of the number of documents indexed.
6. **Construct a retriever and query engine** to support natural language
  questions against the indexed content.
7. **Execute a sample query** and display the response.

This file also includes comments showing how to persist the index to disk to
avoid repeated API calls, and it imports carefully chosen symbols from the
correct submodules to avoid import errors.

- Import paths are sometimes nested; use the correct modules:
  ```python
  from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
  from llama_index.llms.google_genai import GoogleGenAI
  ```

- Building an index:
  ```python
  documents = SimpleDirectoryReader("data").load_data()
  index = VectorStoreIndex.from_documents(documents, llm=llm)
  ```
  or use the helper `vector_store_index_from_documents` if you prefer.

- Add optional layers such as retriever/query engine:
  ```python
  retriever = VectorIndexRetriever(index=index, similarity_top_k=10)
  query_engine = RetrieverQueryEngine(retriever=retriever)
  response = query_engine.query("What is the document about?")
  ```

- Save the index to disk to avoid re-embedding every run:
  ```python
  index.save_to_disk("index.json")
  # later: index = VectorStoreIndex.load_from_disk("index.json")
  ```

## 5. Common issues and troubleshooting

### NameError / ImportError
- Make sure to import all classes/functions you use from the correct
  submodules. The top-level package (`llama_index`) may not export everything.
- Confirm symbols by grepping the workspace or reading the library docs.

### `ValueError: No API key was provided`
- Ensure `.env` is loaded or environment variable is set in the shell.
- Confirm with `print(os.getenv("GOOGLE_API_KEY"))` before client creation.

-### 429 Too Many Requests
-Occurs when the embedding service (OpenAI by default, or Gemini if configured)
  rate limits you. This typically happens during indexing when each document
  triggers a separate API call, or when running the script multiple times in
  quick succession.
- Workarounds:
  - Persist index to disk.
  - Reduce number of documents or pace requests.
  - Check your OpenAI usage/quotas and add payment info if needed.
  - Optionally switch embedding backend (e.g. Google GenAI) to avoid this.

### SSL Context Hang (KeyboardInterrupt)
- The Google GenAI client may spend time loading certificates via `certifi`.
- Usually transient; if it blocks, upgrade `certifi` or set `SSL_CERT_FILE`
  environment variable to a valid CA bundle.

## 6. Packages Installed

```text
llama-index
llama-index-llms-gemini
llama-index-vector-stores-chroma     # for vector stores
python-dotenv
google-genai                       # dependency of LlamaIndex
```

## 7. How to run

1. Activate the venv.
2. Ensure `.env` contains a valid `GOOGLE_API_KEY`.
3. Put some text files under `data/`.
4. Run:
   ```powershell
   & ".\.venv\Scripts\python.exe" test.py
   ```
5. Inspect the output and saved index.

---

### Key takeaways

- Virtual environments isolate dependencies; always double-check which
  `python`/`pip` you’re calling.
- `.env` files are convenient but require explicit loading or environment
  configuration; never assume they are automatically applied.
- LlamaIndex has nested imports and helper functions; keep an eye on
  `NameError` and `ImportError` messages for guidance.
- API errors often come from outside your code (quota, model availability).
- Caching/persistence is key for reducing API usage during development.

