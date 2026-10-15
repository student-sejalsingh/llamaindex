# Module 05 — Embeddings

## 📌 Overview

In Module 04, we learned how to divide Documents into smaller pieces called **Nodes**.

In this module, we learn how to convert those Nodes into **numerical vectors called embeddings**.

Embeddings allow computers to compare data based on **semantic meaning** rather than only exact word matching.

The basic pipeline is:

```text
Text
  ↓
Embedding Model
  ↓
Vector
  ↓
Similarity Search
  ↓
Relevant Information
```

For a RAG system:

```text
PDF
 ↓
Document
 ↓
Nodes
 ↓
Embeddings
 ↓
Vector Store
 ↓
Similarity Search
 ↓
Relevant Nodes
 ↓
LLM
 ↓
Answer
```

---

# 🎯 Learning Objectives

After completing this module, you should understand:

* What is an embedding?
* What is an embedding vector?
* What does embedding dimension mean?
* Why does a short sentence produce hundreds of numbers?
* How to generate embeddings using LlamaIndex
* How to use Ollama for local embeddings
* What is semantic similarity?
* What is cosine similarity?
* Difference between document and query embeddings
* How to compare multiple embeddings
* How embeddings are used in real-world RAG systems
* Why embedding models cannot simply be mixed
* Why embedding dimension affects vector storage

---

# 📁 Folder Structure

```text
05_embeddings/
│
├── 01_basic_embedding.py
├── 02_embedding_dimensions.py
├── 03_semantic_similarity.py
├── 04_document_embeddings.py
├── 05_query_embeddings.py
├── 06_compare_embeddings.py
└── README.md
```

---

# 1️⃣ What is an Embedding?

An embedding is a **dense numerical vector representing the semantic meaning of data**.

For text:

```text
"Binary search is a searching algorithm."
                ↓
         Embedding Model
                ↓
[0.12, -0.43, 0.81, 0.21, ...]
```

The numbers represent the text in a form that computers can mathematically compare.

The important point is:

> Embeddings represent meaning rather than simply matching exact words.

---

# 2️⃣ Why Do We Need Embeddings?

Consider these sentences:

```text
Text A:
"Binary search works on sorted arrays."

Text B:
"Binary search efficiently finds elements in sorted data."
```

The wording is different, but the meaning is similar.

Traditional keyword search may focus on exact words.

Embedding-based search converts both sentences into vectors:

```text
Text A
  ↓
Vector A


Text B
  ↓
Vector B
```

If the vectors are close according to an appropriate similarity measure, the texts are considered semantically similar.

---

# 3️⃣ Embedding Model vs LLM

These two should not be confused.

## LLM

Examples:

```text
Qwen
Llama
GPT
DeepSeek
```

Main purpose:

```text
Question
   ↓
LLM
   ↓
Generated Answer
```

## Embedding Model

Examples:

```text
Nomic
BGE
E5
Sentence Transformers
OpenAI Embeddings
```

Main purpose:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Therefore:

> **LLM generates language. Embedding models represent information numerically.**

---

# 4️⃣ `01_basic_embedding.py`

This file demonstrates the simplest embedding pipeline.

```text
Text
 ↓
OllamaEmbedding
 ↓
Vector
```

The code uses:

```python
from llama_index.embeddings.ollama import OllamaEmbedding

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)
```

Then:

```python
embedding = embed_model.get_text_embedding(text)
```

This converts the text into a numerical vector.

---

# 5️⃣ Ollama Embeddings

For this module, we use:

```text
nomic-embed-text
```

through Ollama.

Install the LlamaIndex integration:

```bash
pip install llama-index-embeddings-ollama
```

Download the model:

```bash
ollama pull nomic-embed-text
```

The advantage of this setup is that the embedding model can run locally.

---

# 6️⃣ What is an Embedding Vector?

A vector is simply a list of numbers.

For example:

```text
[0.12, -0.43, 0.81, 0.21, -0.15, ...]
```

A real embedding vector can contain hundreds or thousands of values depending on the model.

For example:

```text
Text
 ↓
Embedding Model
 ↓
768-dimensional vector
```

---

# 7️⃣ What Does Embedding Dimension Mean?

Suppose the output is:

```text
Embedding Dimension: 768
```

This means:

> The model represents the text using 768 numerical values.

It does **not** mean:

```text
768 words ❌
768 characters ❌
768 understandable features ❌
```

It means:

```text
768 numerical dimensions ✅
```

For example:

```text
Short text
    ↓
768 values


Long text
    ↓
768 values
```

The text length does not determine the embedding dimension.

The **embedding model determines the output dimension**.

---

# 8️⃣ `02_embedding_dimensions.py`

This file demonstrates that different text lengths still produce the same vector dimension when using the same embedding model.

For example:

```text
Text 1 → 768 dimensions
Text 2 → 768 dimensions
Text 3 → 768 dimensions
```

The actual dimension depends on the selected model.

The values change according to the text, but the number of dimensions remains fixed for that model.

---

# 9️⃣ Why Does Dimension Matter?

Suppose:

```text
Embedding dimension = 768
```

and you have:

```text
100,000 Nodes
```

Then you have:

```text
100,000 × 768
=
76,800,000 numerical values
```

Therefore, embedding dimension affects vector storage requirements.

A model with fewer dimensions can require less raw vector storage.

However:

> Lower dimension does not automatically mean better performance.

Retrieval quality must also be considered.

---

# 🔟 Can We Reduce the Dimension?

There are several approaches.

## Smaller embedding model

Use a model that naturally produces fewer dimensions.

```text
Text
 ↓
384-dimensional model
 ↓
384 values
```

This is usually preferable to simply cutting the vector.

---

## ❌ Do Not Simply Truncate

Don't do:

```python
embedding = embedding[:256]
```

This discards part of the representation and is not a proper dimensionality-reduction method.

---

## Dimensionality Reduction

Techniques such as PCA can transform:

```text
768 dimensions
       ↓
PCA
       ↓
256 dimensions
```

But both document and query embeddings must go through the same transformation.

---

## Quantization

Another approach is to reduce the number of bits used to store each value.

For example:

```text
float32
   ↓
lower-precision representation
```

This can reduce storage while keeping the same number of dimensions.

These are more advanced optimization topics.

---

# 1️⃣1️⃣ `03_semantic_similarity.py`

This file demonstrates how embeddings allow us to compare meanings.

We use:

```text
Text 1:
"Binary search works on sorted arrays."

Text 2:
"Binary search is used to efficiently find elements in sorted data."

Text 3:
"The weather is very pleasant today."
```

Conceptually:

```text
Text 1 ↔ Text 2
     ↓
High similarity


Text 1 ↔ Text 3
     ↓
Low similarity
```

The words don't need to be identical.

---

# 1️⃣2️⃣ Similarity Metrics

After converting text into vectors, we need a way to compare them.

Common metrics include:

### Cosine Similarity

Measures the similarity between the directions of two vectors.

For text embeddings, it is one of the most commonly used similarity measures.

Conceptually:

```text
Vector A
    ↘
      ↘
        Vector B
```

Similar direction:

```text
High similarity
```

Different direction:

```text
Low similarity
```

---

### Dot Product

For vectors:

```text
A = [a₁, a₂, a₃]

B = [b₁, b₂, b₃]
```

the dot product is:

```text
A · B = a₁b₁ + a₂b₂ + a₃b₃
```

---

### Euclidean Distance

Measures straight-line distance between vectors.

```text
A ●────────● B
     distance
```

For distance-based comparison:

```text
Smaller distance
      ↓
More similar
```

---

# 1️⃣3️⃣ `04_document_embeddings.py`

This file connects embeddings with the work from Module 04.

Instead of manually creating a few sentences:

```text
PDF
 ↓
Documents
 ↓
Nodes
 ↓
Embedding Model
 ↓
Vectors
```

The code loads the actual PDF dataset:

```python
documents = SimpleDirectoryReader(
    input_dir="../03_documents/data/01_pdf",
    recursive=True,
    required_exts=[".pdf"],
).load_data()
```

Then creates Nodes:

```python
splitter = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

nodes = splitter.get_nodes_from_documents(documents)
```

Finally:

```python
embedding = embed_model.get_text_embedding(
    node.text
)
```

creates an embedding for each Node.

At this stage, the embeddings are only generated in memory.

They are **not yet stored in a vector database**.

---

# 1️⃣4️⃣ `05_query_embeddings.py`

A RAG system has two sides.

## Document side

```text
Document
 ↓
Node
 ↓
Embedding
 ↓
Vector
```

## Query side

```text
User Question
 ↓
Query Embedding
 ↓
Query Vector
```

For example:

```text
User:
"What are the four necessary conditions for deadlock?"
```

becomes:

```text
Question
   ↓
Embedding Model
   ↓
Query Vector
```

The query vector is then compared against stored Node vectors.

---

# 1️⃣5️⃣ Document Embedding vs Query Embedding

Conceptually:

```text
DOCUMENT SIDE

Node
 ↓
Document Embedding
 ↓
Vector
 ↓
Vector Database
```

and:

```text
QUERY SIDE

User Question
 ↓
Query Embedding
 ↓
Query Vector
 ↓
Similarity Search
```

Eventually:

```text
Query Vector
     ↓
Compare with
     ↓
Stored Node Vectors
     ↓
Top Relevant Nodes
```

Some retrieval-focused embedding models use different conventions or instructions for queries and documents, so always follow the model's recommended usage.

---

# 1️⃣6️⃣ `06_compare_embeddings.py`

This file performs a small semantic search experiment.

We create:

```text
User Query:
"What are the necessary conditions for deadlock?"
```

Then several candidate texts:

```text
1. Deadlock conditions
2. Deadlock definition
3. CPU scheduling
4. DBMS normalization
5. Binary search
```

Each text is embedded.

Then cosine similarity is calculated:

```text
Query
 ↓
Query Vector
 ↓
Compare with every candidate vector
 ↓
Similarity Scores
 ↓
Sort
 ↓
Top Results
```

Example:

```text
Rank 1 → Deadlock conditions
Rank 2 → Deadlock definition
Rank 3 → CPU scheduling
Rank 4 → DBMS normalization
Rank 5 → Binary search
```

The exact scores depend on the embedding model.

---

# 1️⃣7️⃣ Real-World Semantic Search

In a real application, we don't manually compare three sentences.

Suppose you have:

```text
100 PDFs
 ↓
10,000 Nodes
 ↓
10,000 Embeddings
```

The embeddings are stored in a vector database.

Then:

```text
User Query
    ↓
Query Embedding
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Top-K Relevant Nodes
```

For example:

```text
User:
"What are the four conditions of deadlock?"

             ↓

        Query Vector

             ↓

      Vector Database

             ↓

Node 2847 → 0.91
Node 2848 → 0.88
Node 1203 → 0.81

             ↓

      Relevant Context

             ↓

             LLM

             ↓

           Answer
```

---

# 1️⃣8️⃣ Embeddings in RAG

Embeddings are one of the foundations of RAG.

Complete pipeline:

```text
                    INGESTION
                       │
                       ↓
                      PDF
                       │
                       ↓
                   Document
                       │
                       ↓
                     Nodes
                       │
                       ↓
                  Embeddings
                       │
                       ↓
                 Vector Store
                       │
                       │
                       │
                       ↑
                  User Query
                       │
                       ↓
               Query Embedding
                       │
                       ↓
              Similarity Search
                       │
                       ↓
               Relevant Nodes
                       │
                       ↓
                      LLM
                       │
                       ↓
                    Answer
```

---

# 1️⃣9️⃣ Embedding Models

Popular embedding model families include:

| Model                 | General characteristic              |
| --------------------- | ----------------------------------- |
| Nomic                 | Good local embedding option         |
| BGE                   | Strong open-source retrieval models |
| E5                    | Designed for retrieval-oriented use |
| Sentence Transformers | Large open-source ecosystem         |
| OpenAI Embeddings     | API-based high-quality embeddings   |
| Instructor            | Can use task-oriented instructions  |

Different models can have different:

* Dimensions
* Languages supported
* Retrieval quality
* Speed
* Memory requirements
* Storage requirements

---

# 2️⃣0️⃣ Can Different Models Be Mixed?

Generally, don't mix vectors from unrelated embedding models in the same vector-search collection.

For example:

```text
Document A
 ↓
Nomic
 ↓
768D
```

and:

```text
Document B
 ↓
BGE
 ↓
384D
```

should not simply be put into one collection and compared directly.

Different models produce vectors in different representation spaces.

If you switch embedding models:

```text
Old embeddings
      ↓
Remove/recreate collection
      ↓
Re-embed documents
      ↓
Store new embeddings
```

---

# 2️⃣1️⃣ Hybrid Search

Embedding search is not always enough.

Production systems often combine:

```text
                Search
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
 Keyword Search        Semantic Search
     BM25                 Embeddings
        ↓                     ↓
 Exact terms             Meaning
        └──────────┬──────────┘
                   ↓
             Combined Results
```

### Keyword Search is useful for:

* IDs
* Codes
* Exact names
* Error messages
* Exact technical terms

### Semantic Search is useful for:

* Natural-language questions
* Paraphrases
* Similar meanings
* Conceptual searches

Combining both can improve retrieval quality.

---

# 2️⃣2️⃣ Important Concepts

Remember these:

```text
Document
    ↓
Large source content

Node
    ↓
Small piece of a Document

Embedding
    ↓
Numerical representation of meaning

Vector
    ↓
List of numerical values

Dimension
    ↓
Number of values in the vector

Similarity
    ↓
How closely two vectors are related

Query Embedding
    ↓
Numerical representation of the user's question
```

---

# 🧠 One-Line Memory Trick

```text
Text → Embedding → Vector → Similarity → Relevant Information
```

Or for RAG:

```text
PDF → Nodes → Embeddings → Vector Store
                              ↑
                         Query Vector
                              ↑
                           Question
```

---

# ✅ Module 05 Completion Checklist

```text
01_basic_embedding.py          ✅
02_embedding_dimensions.py     ✅
03_semantic_similarity.py      ✅
04_document_embeddings.py      ✅
05_query_embeddings.py         ✅
06_compare_embeddings.py       ✅
README.md                      ✅
```

---

# 🚀 Next Module — Vector Stores

So far, we have generated embeddings, but we haven't properly **stored and searched them**.

That's the problem solved by the next module.

```text
Module 05
Embeddings
     ↓
Text → Vectors
```

Next:

```text
Module 06
Vector Stores
     ↓
Vectors → Store → Search
```

We'll learn:

```text
Vector Store
     ↓
ChromaDB
     ↓
Collections
     ↓
Store Embeddings
     ↓
Similarity Search
     ↓
Retrieve Top-K Nodes
```

This is where your current embedding experiments turn into an actual **vector search system**.
