# Module 06 — Vector Stores

## 📌 Overview

A **Vector Store** is a system used to store, manage, and search vector embeddings.

In a typical RAG (Retrieval-Augmented Generation) system, documents are first converted into smaller pieces called **Nodes**. Each Node is then converted into a numerical representation called an **embedding**. These embeddings are stored inside a vector store.

When a user asks a question, the question is also converted into an embedding. The vector store compares the query embedding with stored embeddings and retrieves the most relevant Nodes.

The basic flow is:

```text
Documents
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
Final Answer
```

In this module, we use **ChromaDB** as the vector store.

---

## 🎯 Learning Objectives

After completing this module, you should understand:

- What a vector store is
- Why vector stores are required in RAG
- Difference between a traditional database and a vector store
- What ChromaDB is
- How to create a ChromaDB client
- What a ChromaDB collection is
- How to store documents and embeddings
- How to use real embeddings from an embedding model
- How to perform vector similarity search
- What query embeddings are
- What Top-K means
- How distance is used for ranking
- What metadata is
- How metadata filtering works
- How semantic search and metadata filtering work together
- How vector stores fit into the complete RAG pipeline

---

## 📂 Module Structure

```text
06_vector_stores/
│
├── 01_what_is_vector_store.py
├── 02_chroma_basic.py
├── 03_store_embeddings.py
├── 04_vector_search.py
├── 05_top_k_value.py
├── 06_metadata_filter.py
└── README.md
```

---

## 🧭 Prerequisites

Before starting this module, you should understand:

- Module 03 → Documents
- Module 04 → Nodes & Text Splitters
- Module 05 → Embeddings

The complete pipeline learned so far is:

```text
Data
 ↓
Document
 ↓
Node
 ↓
Embedding
 ↓
Vector Store
```

---

## 📦 Required Installation

Install ChromaDB:

```bash
pip install chromadb
```

Install the LlamaIndex ChromaDB integration:

```bash
pip install llama-index-vector-stores-chroma
```

For the local embedding model used in this module:

```bash
pip install llama-index-embeddings-ollama
```

Make sure Ollama is installed and running, then pull the embedding model:

```bash
ollama pull nomic-embed-text
```

---

## 1️⃣ What Is a Vector Store?

A vector store is a storage system designed to work with vector embeddings.

Suppose we have this text:

```text
Deadlock occurs when processes wait indefinitely
for resources held by each other.
```

An embedding model converts this text into a vector:

```text
Text
 ↓
Embedding Model
 ↓
[0.12, -0.31, 0.72, 0.18, ...]
```

The vector is then stored in the vector store.

A stored record can conceptually contain:

- ID
- Text
- Embedding
- Metadata

For example:

```text
ID:
node_123

Text:
Deadlock occurs when processes wait indefinitely.

Embedding:
[0.12, -0.31, 0.72, ...]

Metadata:
subject = Operating Systems
topic   = Deadlock
```

> **A vector store stores vector representations of data so that similar information can be retrieved efficiently.**

---

## 2️⃣ Why Do We Need a Vector Store?

A normal database is excellent for structured and exact queries.

```sql
SELECT * FROM notes
WHERE subject = 'Operating Systems';
```

This is an exact condition.

But AI applications often need **semantic search**.

Suppose the stored document contains:

```text
Processes can become permanently blocked while
waiting for resources held by other processes.
```

The user asks:

```text
What is deadlock?
```

The exact words may not match, but the meanings are related. Embeddings allow us to represent the meaning of the text numerically.

The process becomes:

```text
User Question
      ↓
Query Embedding
      ↓
Vector Store
      ↓
Similarity Search
      ↓
Most Relevant Documents
```

---

## 3️⃣ Traditional Database vs Vector Store

| Traditional Database | Vector Store |
|---|---|
| Works mainly with structured data | Works mainly with vector embeddings |
| Exact / structured queries | Similarity / semantic search |
| `WHERE subject = "DBMS"` | Find vectors closest to query |
| Good for transactions | Good for AI retrieval |
| Tables / rows | Vectors + documents + metadata |
| Exact matching | Meaning-based matching |

These systems are not necessarily competitors. A real application can use both:

```text
MongoDB   → Application Data
ChromaDB  → Semantic Search / RAG
```

---

## 4️⃣ ChromaDB

ChromaDB is a vector database that can store:

- IDs
- Documents
- Embeddings
- Metadata

A persistent ChromaDB client can be created with:

```python
import chromadb

client = chromadb.PersistentClient(
    path="./chroma_data"
)
```

The path `./chroma_data` is where ChromaDB keeps its persistent data.

---

## 5️⃣ Persistent vs Temporary Storage

A vector store can be temporary or persistent.

- **Temporary / in-memory** — data may disappear when the program stops.
- **Persistent** — data is saved to disk.

We use:

```python
client = chromadb.PersistentClient(
    path="./chroma_data"
)
```

Therefore:

```text
Python Program
      ↓
   ChromaDB
      ↓
./chroma_data/
      ↓
Data remains available
```

This is useful because we don't want to regenerate all embeddings every time the program runs.

---

## 6️⃣ ChromaDB Collection

A ChromaDB collection is a logical group of related records.

```python
collection = client.get_or_create_collection(
    name="cs_notes"
)
```

Think of a collection as a container for related vectors:

```text
cs_notes
│
├── Node 1
│   ├── ID
│   ├── Text
│   ├── Embedding
│   └── Metadata
│
├── Node 2
│   ├── ID
│   ├── Text
│   ├── Embedding
│   └── Metadata
│
└── Node 3
    ├── ID
    ├── Text
    ├── Embedding
    └── Metadata
```

---

## 7️⃣ `01_what_is_vector_store.py`

The first file demonstrates the basic idea of storing vectors.

```text
Text
 ↓
Embedding
 ↓
Vector
 ↓
Vector Store
```

For learning purposes, we can represent the storage using a Python list:

```python
vector_store = []

vector_store.append({
    "text": "Deadlock occurs when processes wait indefinitely.",
    "embedding": [0.1, 0.2, 0.3, 0.4]
})
```

This is useful for understanding the concept. However, **this is not a real vector database.**

A real vector store provides capabilities such as:

- persistent storage
- similarity search
- metadata filtering
- indexing
- scalable retrieval

---

## 8️⃣ `02_chroma_basic.py`

This file introduces ChromaDB directly.

```python
import chromadb

client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="computer_science_notes"
)
```

We can then store records:

```python
collection.add(
    ids=["doc1", "doc2", "doc3"],
    documents=[
        "Deadlock occurs when processes wait indefinitely for resources.",
        "Binary search works efficiently on sorted arrays.",
        "Normalization reduces redundancy in databases."
    ],
    embeddings=[
        [0.1, 0.2, 0.3, 0.4],
        [0.5, 0.6, 0.7, 0.8],
        [0.9, 0.1, 0.2, 0.3]
    ],
    metadatas=[
        {"subject": "Operating Systems", "topic": "Deadlock"},
        {"subject": "DSA", "topic": "Searching"},
        {"subject": "DBMS", "topic": "Normalization"}
    ]
)
```

### ⚠️ Dummy Embeddings

The vectors such as `[0.1, 0.2, 0.3, 0.4]` are **only dummy vectors**.

They are used to understand how ChromaDB stores vectors. They are **not** meaningful embeddings produced by an embedding model.

For real semantic search, we need an embedding model. That is what the next file demonstrates.

---

## 9️⃣ `03_store_embeddings.py`

Now we move from dummy vectors to real embeddings. Our pipeline becomes:

```text
PDF / TXT / MD
      ↓
Documents
      ↓
Nodes
      ↓
nomic-embed-text
      ↓
Real Embeddings
      ↓
ChromaDB
```

We use:

```python
from llama_index.embeddings.ollama import OllamaEmbedding

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)
```

For every Node:

```python
embedding = embed_model.get_text_embedding(
    node.text
)
```

Then store it:

```python
collection.upsert(
    ids=[node.node_id],
    documents=[node.text],
    embeddings=[embedding],
    metadatas=[node.metadata]
)
```

---

## 🔟 What Does One ChromaDB Record Contain?

```text
One Record
│
├── ID
├── Document / Text
├── Embedding
└── Metadata
```

Example:

```text
ID:
node_001

Document:
Deadlock occurs when processes wait indefinitely.

Embedding:
[0.123, -0.421, 0.762, ...]

Metadata:
{
    "file_name": "deadlock.txt",
    "subject": "Operating Systems"
}
```

This combination allows us to retrieve the original text after finding the matching vector.

---

## 1️⃣1️⃣ Why Store the Original Text?

A common question: *If we already have the embedding, why store the original text?*

Because the embedding is mainly useful for **similarity comparison**. The LLM needs the **actual text** to generate an answer.

```text
Original Text
     ↓
Embedding
     ↓
Vector Search
     ↓
Find Matching Record
     ↓
Retrieve Original Text
     ↓
Send Text to LLM
```

Therefore, we generally need both:

- **Embedding** → retrieval
- **Text** → answer generation

---

## 1️⃣2️⃣ `add()` vs `upsert()`

ChromaDB provides operations such as `collection.add(...)` and `collection.upsert(...)`.

**`add()`** — used to add records. If the same ID already exists, it can cause a duplicate-ID problem.

**`upsert()`** — means *insert if it doesn't exist, or update if it already exists*.

For our Node-based pipeline, `upsert()` is useful:

```python
collection.upsert(
    ids=[node.node_id],
    documents=[node.text],
    embeddings=[embedding],
    metadatas=[node.metadata]
)
```

---

## 1️⃣3️⃣ `04_vector_search.py`

After storing embeddings, we can perform semantic search. Suppose the user enters:

```text
What is deadlock?
```

First, convert the query into an embedding:

```python
query_embedding = embed_model.get_query_embedding(
    query
)
```

Then search ChromaDB:

```python
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)
```

The process is:

```text
"What is deadlock?"
        ↓
Query Embedding
        ↓
ChromaDB
        ↓
Compare with Stored Vectors
        ↓
Find Nearest Vectors
        ↓
Return Relevant Text
```

---

## 1️⃣4️⃣ Query Embedding

There are two important embedding operations.

**Document embedding** — used when storing documents/nodes:

```python
embed_model.get_text_embedding(text)
```

```text
Document → Embedding → Vector Store
```

**Query embedding** — used when searching:

```python
embed_model.get_query_embedding(query)
```

```text
User Query → Query Embedding → Vector Search
```

The basic idea:

```text
Documents → document embeddings → database
Query     → query embedding     → search database
```

---

## 1️⃣5️⃣ Similarity Search

The vector store compares the query vector with stored vectors.

```text
Query Vector
     ↓
 ┌───────────────┐
 │ Vector Store  │
 └───────────────┘
   ↓      ↓      ↓
Vector A Vector B Vector C
   ↓      ↓      ↓
Distance Distance Distance
   ↓      ↓      ↓
 Ranking / Retrieval
```

The closest vectors are returned.

---

## 1️⃣6️⃣ Distance

Search results can contain `results["distances"]`. For example:

```text
Result 1 → 0.488
Result 2 → 0.495
Result 3 → 0.509
Result 4 → 0.570
```

The **smaller** value generally means the vector is **closer** under the configured distance metric.

```text
0.488 → closer
0.495 → slightly farther
0.509 → farther
0.570 → farther
```

> ⚠️ Do **not** interpret distance as `0.488 = 48.8% relevant`.
> It is not a relevance percentage. The exact meaning depends on the distance metric.

---

## 1️⃣7️⃣ `05_top_k_value.py`

Top-K controls how many results we retrieve. For example, `n_results=3` means: *return the 3 nearest results.*

---

## 1️⃣8️⃣ Understanding Top-K

**K = 1** — best 1 result.

- Useful when the answer is very specific or only one document is needed.
- Risk: useful supporting information may be missed.

**K = 3** — top 3 results. A common starting point for experiments.

**K = 5** — top 5 results. Provides more context but can introduce noise.

---

## 1️⃣9️⃣ Top-K Trade-off

```text
Small K                          Large K
   ↓                                ↓
Less context                     More context
   ↓                                ↓
Less noise                       More information
   ↓                                ↓
May miss useful information      May contain irrelevant information
```

There is no universal best K. The best value depends on:

- dataset
- query type
- chunk size
- embedding model
- LLM context window
- application requirements

---

## 2️⃣0️⃣ Example Top-K Search

Suppose we ask: **What is deadlock?**

The search might return:

| Rank | Content | Distance |
|---|---|---|
| 1 | Deadlock definition | 0.488 |
| 2 | Hidden deadlocks | 0.495 |
| 3 | Four necessary conditions | 0.509 |
| 4 | Real-world examples | 0.570 |
| 5 | Debugging / prevention | 0.581 |

This demonstrates how the vector store ranks results according to semantic closeness. The top results can then be passed to an LLM.

---

## 2️⃣1️⃣ `06_metadata_filter.py`

Vector search alone asks:

> Which stored content is semantically closest to my question?

Metadata filtering adds another condition:

> Search only inside records having specific properties.

```python
where={
    "subject": "Operating Systems"
}
```

This means: only consider records where `subject = Operating Systems`.

---

## 2️⃣2️⃣ What Is Metadata?

Metadata is information that describes the content.

```python
{
    "subject": "Operating Systems",
    "topic": "Deadlock"
}
```

For an educational system, metadata could be:

```python
{
    "state": "Bihar",
    "district": "Saran",
    "class": "2",
    "subject": "Numeracy",
    "language": "Hindi",
    "assessment": "Baseline"
}
```

Metadata can be used for:

- filtering
- organization
- access control
- source identification
- analytics
- debugging
- improving retrieval

---

## 2️⃣3️⃣ Metadata Filtering + Semantic Search

This is one of the most important concepts in this module.

**Without metadata filtering**

```text
Query
 ↓
Search ALL vectors
 ↓
Top-K
```

**With metadata filtering**

```text
Query
 ↓
Metadata Filter
 ↓
Only matching records
 ↓
Semantic Search
 ↓
Top-K
```

For example:

```text
Question: "What is deadlock?"
Filter:   subject = Operating Systems
```

The system searches only Operating Systems content.

---

## 2️⃣4️⃣ Where Does Metadata Come From?

Metadata can come from the original source. For example, when reading `deadlock.txt`, the reader may automatically provide:

- `file_name`
- `file_path`
- `file_type`

We can also add our own semantic metadata:

```python
{
    "subject": "Operating Systems",
    "topic": "Deadlock"
}
```

This is particularly useful in RAG applications.

---

## 2️⃣5️⃣ Important Metadata Design Principle

Good metadata should describe **useful retrieval dimensions**, for example:

`subject` · `topic` · `class` · `state` · `district` · `language` · `semester` · `difficulty` · `source`

Bad metadata is information that provides no useful retrieval or organization value.

Ask yourself:

> *"Will I ever want to filter, group, or understand my documents using this field?"*

If yes, it may be useful metadata.

---

## 2️⃣6️⃣ Real-World Education Example

Imagine a database containing educational content for India.

```text
States:   Bihar, Jharkhand, Assam, Tamil Nadu, ...
Classes:  1, 2, 3, ...
Subjects: Numeracy, Language, EVS, ...
```

Each Node could contain:

```python
{
    "state": "Bihar",
    "district": "Saran",
    "class": "2",
    "subject": "Numeracy",
    "language": "Hindi"
}
```

A teacher asks:

```text
Give me material for Class 2 numeracy in Hindi for Bihar.
```

The system can filter:

```text
state    = Bihar
class    = 2
subject  = Numeracy
language = Hindi
```

Then semantic search determines which pieces are most relevant.

---

## 2️⃣7️⃣ Complete RAG Retrieval Pipeline

At this point, the retrieval pipeline looks like:

```text
                    DATA
                     ↓
                 Documents
                     ↓
                    Nodes
                     ↓
                Embeddings
                     ↓
                Vector Store
                     ↑
                     │
              Query Embedding
                     ↑
                     │
                User Question
```

With metadata filtering:

```text
User Question
      ↓
Query Embedding
      ↓
Metadata Filter
      ↓
Filtered Records
      ↓
Similarity Search
      ↓
Top-K Nodes
      ↓
LLM
      ↓
Final Answer
```

---

## 2️⃣8️⃣ Full RAG Architecture

The concepts learned so far fit into a larger RAG architecture:

```text
                    INGESTION
                        │
                        ↓
                  Source Data
                        │
                        ↓
                    Documents
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
              ┌─────────┴─────────┐
              │                   │
              ↓                   ↓
        Query Embedding      Metadata Filter
              │                   │
              └─────────┬─────────┘
                        ↓
                 Similarity Search
                        ↓
                      Top-K
                        ↓
                Relevant Context
                        ↓
                       LLM
                        ↓
                   Final Answer
```

---

## 2️⃣9️⃣ PDF/Text Extraction Matters

During this module, we observed an important issue with one of the Computer Networks PDFs.

The PDF itself contained readable content, but the current PDF extraction path produced **corrupted/garbled text**.

This is important because:

```text
Bad Extraction
      ↓
Bad Text
      ↓
Bad Nodes
      ↓
Bad Embeddings
      ↓
Bad Vector Search
      ↓
Bad RAG Answer
```

> **A vector database cannot fix bad input data.**
> The quality of retrieval depends heavily on the quality of ingestion.

---

## 3️⃣0️⃣ Different Types of Source Data

A real RAG system may receive:

PDF · TXT · Markdown · HTML · Web pages · Images · Scanned documents · Tables · Databases · APIs · JSON

Different sources may require different processing:

```text
Normal PDF       → Text Extraction
Scanned PDF      → OCR
Table            → Table Extraction
Image / Diagram  → OCR / Vision / Captioning
```

Then the processed information can become:

```text
Documents
   ↓
Nodes
   ↓
Embeddings
   ↓
Vector Store
```

---

## 3️⃣1️⃣ Why Garbage Extraction Produces Bad Retrieval

Suppose the actual PDF contains:

```text
The OSI model consists of seven layers.
```

But extraction produces:

```text
]1v/ށ˗L[)N~6*...
```

The embedding model receives the corrupted text. Therefore:

```text
Correct PDF
    ↓
❌ Corrupted extraction
    ↓
❌ Meaning lost
    ↓
❌ Incorrect embedding
    ↓
❌ Poor retrieval
```

The problem is not necessarily the vector database. The problem can occur much earlier in the pipeline.

---

## 3️⃣2️⃣ Vector Store vs Index

A vector store and an index are related, but they are not the same concept.

```text
Nodes
  ↓
Index
  ↓
Vector Store
```

- The **Vector Store** is responsible for storing and retrieving vectors.
- An **Index** is a higher-level structure used by frameworks such as LlamaIndex to organize and retrieve information.

We will study Indexes in the next module.

---

## 3️⃣3️⃣ Vector Store vs Retriever

**Vector Store** is responsible for:

- Storing vectors
- Searching vectors
- Returning records

**Retriever** is responsible for:

- Taking a query
- Retrieving relevant Nodes

```text
User Query
     ↓
Retriever
     ↓
Vector Store
     ↓
Relevant Nodes
```

The retriever can use a vector store underneath. We will study Retrievers in a later module.

---

## 3️⃣4️⃣ Vector Store vs Query Engine

A vector store does not normally generate the final natural-language answer. It **retrieves** information.

A **Query Engine** goes further:

```text
User Question
      ↓
Retrieve relevant Nodes
      ↓
Build context
      ↓
LLM
      ↓
Generate answer
```

Therefore:

```text
Vector Store  → Retrieval
Query Engine  → Retrieval + LLM response
```

This distinction will become important in the upcoming Query Engine module.

---

## 3️⃣5️⃣ Important Concepts to Remember

| Concept | Meaning |
|---|---|
| **Vector** | A numerical representation, e.g. `[0.12, -0.45, 0.78, ...]` |
| **Embedding** | A vector representation of content meaning |
| **Vector Store** | Stores embeddings and associated information (vector + text + metadata) |
| **Similarity Search** | Finds stored vectors closest to the query vector |
| **Top-K** | Controls how many results are returned (K = 3 → top 3) |
| **Metadata** | Additional information describing a document or Node (subject, topic, class, state, language) |
| **Metadata Filtering** | Restricts the search to records matching specific metadata conditions |

---

## 🧠 One-Line Mental Model

```text
Embedding        = Numerical representation of meaning
Vector Store     = Place where embeddings are stored
Vector Search    = Find semantically similar vectors
Distance         = Measure used to rank closeness
Top-K            = Number of results to retrieve
Metadata         = Information describing the content
Metadata Filter  = Restrict where the search happens
```

---

## 🔥 The Most Important Mental Model

```text
                USER QUESTION
                      │
                      ↓
              Query Embedding
                      │
                      ↓
              ┌───────────────┐
              │ Vector Store  │
              └───────────────┘
                      │
             ┌────────┴────────┐
             ↓                 ↓
       Metadata Filter    Similarity Search
             │                 │
             └────────┬────────┘
                      ↓
                    Top-K
                      ↓
              Relevant Nodes
                      ↓
                     LLM
                      ↓
                Final Answer
```

---

## 🧪 Module Experiments

### Experiment 1 — Different queries

Try:

- `What is deadlock?`
- `Explain deadlock conditions.`
- `How can deadlock happen?`

Observe whether the retrieved results change.

### Experiment 2 — Different Top-K values

Try `K = 1`, `K = 3`, `K = 5`.

Compare: relevance, amount of context, noise.

### Experiment 3 — Metadata filtering

Try `subject = Operating Systems`, then `subject = DBMS`.

Observe how the search space changes.

### Experiment 4 — Different chunk sizes

Compare `chunk_size = 100`, `300`, and `500`, then observe how retrieval changes.

This connects the current module with the previous Nodes & Text Splitters module.

---

## 🔗 Connection With Previous Modules

| Module | Contribution to this module |
|---|---|
| **03 — Documents** | Source data is loaded into Documents |
| **04 — Nodes & Text Splitters** | Documents are split into Nodes; chunk size affects retrieval quality |
| **05 — Embeddings** | Nodes are converted into vectors that this module stores and searches |

## ➡️ What's Next

- **Module 07 — Indexes:** a higher-level structure built on top of vector stores
- **Retrievers:** take a query and fetch relevant Nodes
- **Query Engines:** retrieval + LLM to generate the final answer