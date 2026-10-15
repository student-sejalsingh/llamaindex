# Module 07 — Indexes in LlamaIndex

Indexes are an important part of LlamaIndex. They organize data so that relevant information can be retrieved efficiently when a user asks a question.

---

## 1. What is an Index?

An index is a data structure that helps LlamaIndex organize and retrieve information.

The general pipeline is:

```text
Documents
    ↓
Nodes
    ↓
Index
    ↓
Retriever / Query Engine
    ↓
LLM
    ↓
Answer
```

For example:

> **User:** What is deadlock?

The system finds the relevant information from the indexed data and provides it to the LLM.

---

## 2. Why do we need Indexes?

Suppose we have:

- 100 PDFs
- 10,000 nodes
- 10,000 embeddings

Searching through all the original documents every time would be inefficient.

An index organizes the information so that retrieval becomes easier. Indexes can organize information in different ways depending on the type of data and retrieval requirement.

---

## 3. Major Index Types

Different index types use different strategies.

| Index | Main Idea | Typical Use |
|---|---|---|
| `VectorStoreIndex` | Semantic similarity using embeddings | RAG |
| `SummaryIndex` | Broad/node-oriented retrieval | Summarization |
| `DocumentSummaryIndex` | Document-level summaries | Finding relevant documents |
| `TreeIndex` | Hierarchical organization | Hierarchical summarization |
| `KeywordTableIndex` | Keyword-based retrieval | Keyword search |
| `KnowledgeGraphIndex` | Entities and relationships | Knowledge graphs |

> **Note:** Some older index classes such as `KeywordTableIndex` and `KnowledgeGraphIndex` are legacy-style APIs in newer LlamaIndex versions. Always check the version-specific documentation before using them in a new project.

---

## 4. VectorStoreIndex

`VectorStoreIndex` is one of the most important indexes for RAG applications. It uses embeddings to represent nodes as vectors.

Pipeline:

```text
Document
   ↓
Nodes
   ↓
Embedding Model
   ↓
Vectors
   ↓
Vector Store
   ↓
Similarity Search
```

Example:

```python
from llama_index.core import Document, VectorStoreIndex

documents = [
    Document(text="Deadlock occurs when processes wait indefinitely."),
    Document(text="Binary search works on sorted arrays.")
]

index = VectorStoreIndex.from_documents(documents)
```

When the user asks:

```text
What is deadlock?
```

the query is converted into an embedding and compared with stored embeddings. The most relevant nodes are retrieved.

---

## 5. SummaryIndex

`SummaryIndex` provides broad/node-oriented access to the indexed nodes. It is useful when the system needs to consider a collection of nodes for summarization or synthesis.

```python
from llama_index.core import Document, SummaryIndex

documents = [
    Document(text="Operating Systems manage computer resources."),
    Document(text="Processes are programs in execution."),
    Document(text="Deadlock occurs when processes wait indefinitely.")
]

index = SummaryIndex.from_documents(documents)
```

**Important:** `SummaryIndex` should not be confused with `DocumentSummaryIndex`.

`SummaryIndex` manages nodes for broad retrieval/synthesis. It does **not** simply mean:

```text
One document → One summary
```

---

## 6. DocumentSummaryIndex

`DocumentSummaryIndex` works at the **document level**. Conceptually:

```text
Document 1 → Summary 1
Document 2 → Summary 2
Document 3 → Summary 3
```

This is useful when you have many documents and want to identify which documents are relevant before retrieving their detailed content.

```python
from llama_index.core import (
    Document,
    DocumentSummaryIndex,
)

documents = [
    Document(
        text="Operating Systems manage hardware and software resources."
    ),
    Document(
        text="Database normalization reduces redundancy."
    ),
]

index = DocumentSummaryIndex.from_documents(documents)
```

An LLM is involved in generating document-level summaries.

---

## 7. TreeIndex

`TreeIndex` organizes information hierarchically. Conceptually:

```text
                 Root
                  |
          Summary of summaries
             /           \
        Summary A       Summary B
        /      \         /      \
      Node1   Node2    Node3   Node4
```

Instead of treating every node independently, information can be organized into multiple levels. This is useful for hierarchical summarization and navigation through larger amounts of information.

```python
from llama_index.core import Document, TreeIndex

documents = [
    Document(text="Operating Systems manage resources."),
    Document(text="Process management handles processes."),
    Document(text="Memory management handles memory."),
]

index = TreeIndex.from_documents(documents)
```

> `TreeIndex` is an older LlamaIndex index API in many current versions. Check the current version documentation before using it in production.

---

## 8. KeywordTableIndex

`KeywordTableIndex` is based on **keywords** rather than semantic embeddings.

For example:

```text
Document:
"Deadlock occurs when processes wait indefinitely."

Keywords:
deadlock
processes
resources
waiting
```

A keyword-based search can use these terms to find relevant nodes.

```python
from llama_index.core import Document, KeywordTableIndex

documents = [
    Document(text="Deadlock occurs when processes wait indefinitely."),
    Document(text="Binary search works on sorted arrays."),
]

index = KeywordTableIndex.from_documents(documents)
```

This approach is different from vector search:

```text
Vector search
"What happens when processes wait forever?"
                ↓
       Semantic similarity
```

```text
Keyword search
"deadlock"
    ↓
Find matching keywords
```

> `KeywordTableIndex` is considered a legacy-style API in newer LlamaIndex versions.

---

## 9. KnowledgeGraphIndex

A knowledge graph represents information using **entities and relationships**.

For example:

```text
Python
   |
   | used_for
   ↓
Machine Learning
   |
   | branch_of
   ↓
Artificial Intelligence
```

Another example:

```text
LlamaIndex
    |
    | used_for
    ↓
RAG
```

Conceptually, information is represented as:

```text
Subject → Relationship → Object
```

For example:

```text
Python → used_for → Machine Learning
```

The older LlamaIndex API used `KnowledgeGraphIndex`. However, graph-related APIs have evolved, so the current LlamaIndex documentation should be checked before using this class in a new application.

---

## 10. VectorStoreIndex vs SummaryIndex

These two are particularly important.

| Feature | VectorStoreIndex | SummaryIndex |
|---|---|---|
| Main purpose | Semantic retrieval | Broad retrieval/synthesis |
| Embeddings | Yes | Not required for basic creation |
| Similarity search | Yes | No |
| Best for | RAG | Summarization |
| Typical retrieval | Top-K relevant nodes | Broad node access |

**VectorStoreIndex**

> Question: *What are the four conditions of deadlock?*

It tries to find the most semantically relevant nodes.

**SummaryIndex**

> Question: *Summarize these notes.*

It can make the collection of nodes available for broader synthesis.

---

## 11. Index vs Retriever vs Query Engine

These concepts are often confused.

```text
                 INDEX
                   ↓
               RETRIEVER
                   ↓
            Relevant Nodes
                   ↓
            QUERY ENGINE
                   ↓
                 LLM
                   ↓
                Answer
```

- **Index** — organizes/stores information.
- **Retriever** — finds relevant information.
- **Query Engine** — coordinates retrieval and response generation.
- **LLM** — generates the final natural-language response.

---

## 12. Persistence

Persistence means saving the index/storage so that it can be loaded later.

**Without persistence:**

```text
Program starts
     ↓
Load documents
     ↓
Create embeddings
     ↓
Build index
     ↓
Query
```

Every time the program starts, the index may need to be rebuilt.

**With persistence:**

```text
FIRST RUN

Documents
   ↓
Embeddings
   ↓
Index
   ↓
SAVE
```

```text
NEXT RUN

LOAD INDEX
   ↓
Query
```

Saving:

```python
index.storage_context.persist(
    persist_dir="./storage"
)
```

Loading later:

```python
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)

storage_context = StorageContext.from_defaults(
    persist_dir="./storage"
)

index = load_index_from_storage(
    storage_context
)
```

---

## 13. LlamaIndex + Chroma

Chroma can be used as the vector store for a `VectorStoreIndex`.

Architecture:

```text
                LlamaIndex
                    |
                    ↓
             VectorStoreIndex
                    |
                    ↓
             ChromaVectorStore
                    |
                    ↓
                  Chroma
                    |
                    ↓
              Persistent Storage
```

**Step 1 — Create a persistent Chroma client:**

```python
import chromadb

chroma_client = chromadb.PersistentClient(
    path="./chroma_data"
)
```

**Step 2 — Create or access a collection:**

```python
chroma_collection = (
    chroma_client.get_or_create_collection(
        name="cs_notes"
    )
)
```

**Step 3 — Connect it to LlamaIndex:**

```python
from llama_index.vector_stores.chroma import (
    ChromaVectorStore,
)

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)
```

**Step 4 — Create the storage context:**

```python
from llama_index.core import StorageContext

storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)
```

**Step 5 — Create the index:**

```python
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)
```

---

## 14. Persistence with Chroma

Chroma's `PersistentClient` allows the vector database to persist on disk:

```python
chroma_client = chromadb.PersistentClient(
    path="./chroma_data"
)
```

The important distinction:

```text
LlamaIndex persistence  ≠  Chroma persistence
```

**LlamaIndex persistence** saves LlamaIndex storage components:

```python
index.storage_context.persist(
    persist_dir="./storage"
)
```

**Chroma persistence** — Chroma manages its own persistent database:

```python
chromadb.PersistentClient(
    path="./chroma_data"
)
```

When using Chroma as your vector store, Chroma becomes the persistent vector storage layer.

---

## 15. Complete RAG Architecture

A practical LlamaIndex RAG system can look like this:

```text
                DATA
                 |
       ┌─────────┴─────────┐
       |                   |
      PDF                MongoDB
       |                   |
       ↓                   ↓
   Documents          Documents
       |                   |
       └─────────┬─────────┘
                 ↓
               Nodes
                 ↓
          Embedding Model
                 ↓
        VectorStoreIndex
                 ↓
        Chroma Vector Store
                 ↓
             Retriever
                 ↓
            Query Engine
                 ↓
               Ollama
                 ↓
              Answer
```

---

## 16. Which Index Should I Use?

A simple decision guide:

| If you need… | Use |
|---|---|
| Semantic search | `VectorStoreIndex` |
| Broad summarization | `SummaryIndex` |
| Document-level summaries | `DocumentSummaryIndex` |
| Hierarchical organization | `TreeIndex` |
| Keyword-based retrieval | Keyword-based approach |
| Entity relationships | Graph-based approach |