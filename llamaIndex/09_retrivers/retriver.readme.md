# LlamaIndex – Module 09: Retrievers

This module focuses on **Retrievers** in LlamaIndex — how to find the most relevant information from an index before passing it to later stages of a RAG pipeline.

---

## 📁 Folder Structure

```text
09_retrievers/
│
├── 01_basic_retriever.py
├── 02_vector_index_retriever.py
├── 03_similarity_top_k.py
├── 04_retriever_scores.py
├── 05_metadata_filter_retriever.py
├── 06_keyword_retriever.py
├── 07_vector_vs_keyword_retrieval.py
├── 08_custom_retriever.py
├── 09_retriever_with_chroma.py
├── 10_fusion_retriever.py
├── 11_router_retriever.py
├── 12_retriever_pipeline.py
│
└── README.md
```

---

## 1. What is a Retriever?

A Retriever finds the pieces of information that are most relevant to a user's query.

For example:

```text
Question:
"What is deadlock in Operating System?"

             ↓

        Retriever
             ↓
 ┌─────────────────────────┐
 │ Relevant Node 1         │
 │ Relevant Node 2         │
 │ Relevant Node 3         │
 └─────────────────────────┘
```

The retriever does not necessarily generate the final answer. Its main job is:

```text
Query → Relevant Nodes
```

---

## 2. Retriever in RAG

A typical RAG system looks like:

```text
User Question
      ↓
    Query
      ↓
   Retriever
      ↓
Relevant Documents / Nodes
      ↓
Response Synthesizer
      ↓
     LLM
      ↓
Final Answer
```

So the retriever is the **information-finding component** of RAG.

---

## 3. Retriever vs Query Engine

This is one of the most important distinctions.

| Retriever | Query Engine |
|---|---|
| Finds relevant nodes | Handles the complete question-answer process |
| Returns nodes | Usually returns a response |
| Does not necessarily call LLM | Can use an LLM |
| Focuses on retrieval | Combines retrieval + response synthesis |

Example:

```python
nodes = retriever.retrieve(question)
```

The result is retrieved nodes. Whereas:

```python
response = query_engine.query(question)
```

The result is normally a generated response.

---

## 4. Files in This Module

### 01 — Basic Retriever

**File:** `01_basic_retriever.py`

Introduces the basic retrieval process.

```text
Documents
   ↓
VectorStoreIndex
   ↓
Retriever
   ↓
Relevant Nodes
```

Important concept:

```python
retriever.retrieve(question)
```

---

## 5. Vector Index Retriever

**File:** `02_vector_index_retriever.py`

Introduces the explicit `VectorIndexRetriever`.

```python
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2
)
```

Compared with:

```python
index.as_retriever()
```

`as_retriever()` is a convenient way to create a retriever, while explicitly creating `VectorIndexRetriever` gives you more direct control over its configuration.

---

## 6. Similarity Top-K

**File:** `03_similarity_top_k.py`

`similarity_top_k` controls how many top results the retriever should return.

```python
retriever = index.as_retriever(
    similarity_top_k=3
)
```

Conceptually:

```text
Query
 ↓
Similarity Search
 ↓
Rank results
 ↓
Top 3
```

> **Important:** `top_k=3` does **not** mean "3% similarity". It means: *return up to the 3 highest-ranked results.*

Higher k gives more context but can also introduce less relevant information.

---

## 7. Retriever Scores

**File:** `04_retriever_scores.py`

Retrievers can return a score along with a node.

```python
for result in results:
    print(result.score)
```

You might see:

```text
Score: 0.82
Score: 0.76
Score: 0.61
```

> **Important:** Don't automatically interpret `0.82` as "82% relevance". The meaning and direction of scores depend on the retrieval backend and similarity/distance metric.

---

## 8. Metadata Filtering

**File:** `05_metadata_filter_retriever.py`

Documents can contain metadata:

```python
Document(
    text="Deadlock occurs when...",
    metadata={
        "subject": "OS",
        "topic": "Deadlock"
    }
)
```

Metadata can help restrict retrieval:

```text
Question
   ↓
Metadata Filter
   ↓
Only OS documents
   ↓
Vector Retrieval
   ↓
Relevant Nodes
```

This becomes especially useful in large knowledge bases.

---

## 9. Keyword Retrieval

**File:** `06_keyword_retriever.py`

This file demonstrates a simple keyword-based retrieval approach.

```text
Query:
"TCP protocol"

Document:
"TCP is a reliable transport protocol."
```

The system looks for matching terms. A simple keyword system can be represented as:

```text
Query Terms
     ↓
Find matching words
     ↓
Calculate overlap
     ↓
Rank documents
```

**Advantages**

- Simple
- Fast
- Easy to understand
- Useful for exact terms

**Limitation**

Keyword matching may fail when the query uses different wording. For example:

```text
Query:
"How does the processor choose the next task?"

Document:
"CPU scheduling determines which process runs next."
```

The meaning is similar, but exact keyword overlap may be weak.

---

## 10. Vector vs Keyword Retrieval

**File:** `07_vector_vs_keyword_retrieval.py`

This file compares the two approaches.

**Keyword Retrieval** looks primarily at exact terms.

```text
"CPU scheduling"
        ↓
Find documents containing similar words
```

**Vector Retrieval** looks at semantic similarity.

```text
"How does the processor decide which task runs?"
                    ↓
              Embedding
                    ↓
          Semantic similarity
                    ↓
       CPU scheduling document
```

### Comparison

| Feature | Keyword | Vector |
|---|---|---|
| Exact terms | Good | Good |
| Semantic meaning | Limited | Strong |
| Synonyms | Limited | Better |
| Simple implementation | Very easy | More complex |
| Embedding required | No | Yes |

---

## 11. Custom Retriever

**File:** `08_custom_retriever.py`

LlamaIndex allows you to create your own retriever by extending `BaseRetriever`.

The important method is `_retrieve()`.

```text
BaseRetriever
      ↓
Your CustomRetriever
      ↓
Your retrieval logic
```

A custom retriever can:

- Combine multiple retrievers
- Apply custom filtering
- Add business rules
- Route queries
- Modify ranking
- Integrate external retrieval systems

---

## 12. Retriever with Chroma

**File:** `09_retriever_with_chroma.py`

This file connects retrieval with ChromaDB. The architecture becomes:

```text
Documents
    ↓
Embeddings
    ↓
ChromaDB
    ↓
VectorStore
    ↓
VectorIndexRetriever
    ↓
Relevant Nodes
```

A persistent Chroma database can be created using:

```python
chromadb.PersistentClient(
    path="./chroma_data"
)
```

This allows the vector data to persist between program runs.

---

## 13. Fusion Retriever

**File:** `10_fusion_retriever.py`

Sometimes one retrieval strategy isn't enough. We can combine:

```text
Vector Retrieval
       +
BM25 Retrieval
       ↓
Fusion
       ↓
Better ranked results
```

- **Vector Retrieval** — good at understanding semantic meaning.
- **BM25** — good at keyword and term-based matching.

Combining them can provide better coverage.

### Reciprocal Rank Fusion

The example uses:

```python
mode="reciprocal_rerank"
```

The basic idea is to combine the rankings produced by multiple retrievers. Conceptually:

```text
Vector Retriever
    ↓
A → rank 1
B → rank 2
C → rank 3


BM25 Retriever
    ↓
B → rank 1
A → rank 2
D → rank 3


        ↓

      Fusion

        ↓

Combined ranking
```

An important advantage is that the systems don't have to produce directly comparable raw scores.

---

## 14. Router Retriever

**File:** `11_router_retriever.py`

A router chooses which retriever should handle a query.

```text
Question:
"What is deadlock?"

        ↓

     Router
        ↓
   OS Retriever
        ↓
Relevant OS Nodes
```

Another query:

```text
"Explain normalization"

        ↓

     Router
        ↓
  DBMS Retriever
        ↓
Relevant DBMS Nodes
```

The example uses simple keyword-based routing:

```text
deadlock      → OS
normalization → DBMS
TCP           → Computer Networks
```

This is an educational implementation of the routing idea.

---

## 15. Retriever Pipeline

**File:** `12_retriever_pipeline.py`

A retrieval pipeline combines multiple retrieval steps. The example follows:

```text
User Query
     ↓
Vector Retriever
     ↓
Retrieve Candidates
     ↓
Remove Duplicates
     ↓
Top-K Selection
     ↓
Final Retrieved Nodes
```

The important idea is that retrieval doesn't have to be a single operation. A real system can have:

```text
Query
  ↓
Query Processing
  ↓
Router
  ↓
Vector + BM25
  ↓
Metadata Filtering
  ↓
Reranking
  ↓
Top-K
  ↓
Response Synthesizer
```

---

## 16. Important LlamaIndex Classes

During this module you will encounter:

| Class | Purpose |
|---|---|
| `BaseRetriever` | Base class for implementing custom retrievers |
| `VectorIndexRetriever` | Retrieves nodes using vector similarity from an index |
| `QueryFusionRetriever` | Combines results from multiple retrievers |
| `BM25Retriever` | Provides BM25-based retrieval |
| `NodeWithScore` | Represents a retrieved node together with its score |
| `QueryBundle` | Contains the query information passed through the retrieval process |

---

## 17. Complete Retrieval Architecture

After completing this module, you should understand this architecture:

```text
                    USER QUERY
                        │
                        ▼
                  ┌───────────┐
                  │  Router   │
                  └─────┬─────┘
                        │
             ┌──────────┼──────────┐
             ▼          ▼          ▼
            OS         DBMS        CN
        Retriever    Retriever   Retriever
             │          │          │
             └──────────┼──────────┘
                        ▼
                Candidate Results
                        │
                        ▼
               ┌────────────────┐
               │ Fusion / Filter│
               └───────┬────────┘
                       ▼
                   Top-K Nodes
                       │
                       ▼
              Response Synthesizer
```

The last two components belong to later modules.

---

## 18. Key Concepts to Remember

| Concept | Meaning |
|---|---|
| **Retriever** | Finds relevant information (`Query → Nodes`) |
| **Top-K** | Controls the number of retrieved results (`similarity_top_k=3`) |
| **Vector Retrieval** | Uses embeddings and semantic similarity |
| **Keyword Retrieval** | Uses terms appearing in the documents |
| **BM25** | A stronger traditional lexical retrieval method based on term statistics |
| **Custom Retriever** | Allows you to implement your own retrieval logic |
| **Fusion** | Combines multiple retrieval strategies |
| **Router** | Chooses an appropriate retriever |
| **Pipeline** | Connects multiple retrieval stages |

---

## 19. Retriever vs Full RAG

At the end of Module 09:

```text
                 RETRIEVAL
                    │
                    ▼
User Query → Retriever → Relevant Nodes
```

A complete RAG system continues:

```text
User Query
     ↓
Retriever
     ↓
Relevant Nodes
     ↓
Response Synthesizer
     ↓
LLM
     ↓
Final Answer
```