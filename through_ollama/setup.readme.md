# LlamaIndex with Ollama

This project demonstrates how to use **LlamaIndex** with **Ollama** to run Large Language Models (LLMs) locally. It also uses **Hugging Face Embedding Models** for document embeddings.

## Overview

- Run LLMs locally using Ollama
- Use LlamaIndex for building AI applications
- Generate embeddings using Hugging Face
- Build Retrieval-Augmented Generation (RAG) applications
- Fully local setup (no OpenAI API required)

---

## Prerequisites

- Python 3.10+
- Ollama installed
- Git
- At least **32 GB RAM** is recommended for larger models such as **Llama 3.1**.

---

## Step 1: Install Ollama

Download and install Ollama from the official website:

https://ollama.com/download

Verify the installation:

```bash
ollama --version
```

---

## Step 2: Download a Model

Pull the Llama 3.1 model:

```bash
ollama pull llama3.1
```

You can also download other models such as:

```bash
ollama pull qwen3:0.6b
ollama pull qwen3:4b
ollama pull deepseek-r1:7b
```

List installed models:

```bash
ollama list
```

Run a model:

```bash
ollama run llama3.1
```

---

## Step 3: Install Dependencies

Install the required LlamaIndex integrations:

```bash
pip install llama-index-llms-ollama
pip install llama-index-embeddings-huggingface
```

Or install both together:

```bash
pip install llama-index-llms-ollama llama-index-embeddings-huggingface
```

---

## Step 4: Import Packages

### Ollama LLM

```python
from llama_index.llms.ollama import Ollama
```

### Hugging Face Embeddings

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
```

---

## Example

```python
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

llm = Ollama(
    model="llama3.1",
    request_timeout=360
)

embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-base-en-v1.5"
)
```

---

## Project Structure

```
project/
│
├── README.md
├── requirements.txt
├── main.py
└── data/
```

---

## Useful Ollama Commands

Pull a model

```bash
ollama pull llama3.1
```

Run a model

```bash
ollama run llama3.1
```

Show installed models

```bash
ollama list
```

Remove a model

```bash
ollama rm llama3.1
```

---

## Official Resources

### Ollama

https://ollama.com

### Ollama GitHub

https://github.com/ollama/ollama

### LlamaIndex Documentation

https://developers.llamaindex.ai/

### LlamaIndex Integrations

https://developers.llamaindex.ai/python/framework/community/integrations/

---

## Notes

- Ollama allows you to run LLMs locally without cloud APIs.
- LlamaIndex provides tools for indexing, retrieval, agents, and RAG pipelines.
- Hugging Face Embeddings convert text into vectors for semantic search.
- Larger models require more RAM. For systems with limited memory, consider using smaller models like `qwen3:0.6b`.

---

## License

This project is for learning and educational purposes.