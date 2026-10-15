# Module 08 — Query Engine

## 📌 Overview

A **Query Engine** is the component in LlamaIndex that manages the complete question-answering process.

It takes a user's question, retrieves relevant information from an index, sends the retrieved information to the LLM, and produces the final answer.

The basic workflow is:

```text
User Query
    ↓
Retriever
    ↓
Retrieved Nodes
    ↓
Postprocessor
    ↓
Response Synthesizer
    ↓
LLM
    ↓
Final Answer
```

The main idea is:

> **Retriever retrieves, Query Engine orchestrates, and the LLM generates the answer.**

---

## 📂 Module Structure

```text
08_query_engine/
│
├── 01_basic_query_engine.py
├── 02_query_engine_with_vector_index.py
├── 03_retriever_vs_query_engine.py
├── 04_retriever_query_engine.py
├── 05_postprocessor.py
├── 06_response_synthesizer.py
├── 07_query_engine_with_chroma.py
├── 08_sub_question_query_engine.py
├── 09_router_query_engine.py
├── 10_knowledge_graph_query_engine.py
├── 11_streaming_query_engine.py
├── 12_custom_prompt_query_engine.py
│
└── README.md
```

---

## 🎯 Learning Objectives

After completing this module, you should understand:

- What a Query Engine is
- How a Query Engine works internally
- Difference between Retriever and Query Engine
- How to create a Query Engine from an index
- How `similarity_top_k` works
- What a `RetrieverQueryEngine` is
- What Postprocessors do
- What a Response Synthesizer does
- How to use Query Engine with ChromaDB
- What SubQuestion Query Engine is
- What Router Query Engine is
- What Knowledge Graph Query Engine is
- How streaming responses work
- How to customize the Query Engine prompt

---

## 1. Basic Query Engine

**File:** `01_basic_query_engine.py`

The simplest way to create a Query Engine is:

```python
query_engine = index.as_query_engine()
```

Then ask a question:

```python
response = query_engine.query("What is deadlock?")
```

The complete idea is:

```text
Documents
    ↓
VectorStoreIndex
    ↓
Query Engine
    ↓
Question
    ↓
Answer
```

The Query Engine hides many internal components from us.

---

## 2. Query Engine with Vector Index

**File:** `02_query_engine_with_vector_index.py`

Here we use:

```python
index = VectorStoreIndex.from_documents(documents)
```

and:

```python
query_engine = index.as_query_engine(
    similarity_top_k=2
)
```

### What is `similarity_top_k`?

It controls how many relevant nodes should be retrieved. For example, `similarity_top_k=2` means:

```text
Question
   ↓
Vector Search
   ↓
Top 2 relevant nodes
   ↓
LLM
   ↓
Answer
```

If `similarity_top_k=5`, then up to 5 relevant nodes can be retrieved.

---

## 3. Retriever vs Query Engine

**File:** `03_retriever_vs_query_engine.py`

This file demonstrates an important distinction.

### Retriever

A Retriever finds relevant information.

```python
retriever = index.as_retriever(
    similarity_top_k=2
)

nodes = retriever.retrieve(question)
```

Its job is:

```text
Question
    ↓
Retriever
    ↓
Relevant Nodes
```

It does not necessarily generate the final natural-language answer.

### Query Engine

A Query Engine manages the complete process:

```text
Question
    ↓
Retriever
    ↓
Relevant Nodes
    ↓
Response Synthesis
    ↓
LLM
    ↓
Final Answer
```

### Easy way to remember

```text
Retriever    = Find
Query Engine = Find + Process + Answer
```

---

## 4. Retriever Query Engine

**File:** `04_retriever_query_engine.py`

Instead of allowing LlamaIndex to automatically create the components, we explicitly construct them.

```python
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2
)
```

Then create a response synthesizer:

```python
response_synthesizer = get_response_synthesizer()
```

Then combine them:

```python
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer
)
```

The architecture becomes:

```text
                    ┌──────────────┐
Question ─────────→ │  Retriever   │
                    └──────┬───────┘
                           ↓
                    Retrieved Nodes
                           ↓
                 Response Synthesizer
                           ↓
                          LLM
                           ↓
                       Answer
```

This approach gives more control over the individual components.

---

## 5. Postprocessor

**File:** `05_postprocessor.py`

A Postprocessor operates on retrieved nodes **before** they are passed to the response generation stage.

```python
SimilarityPostprocessor(
    similarity_cutoff=0.5
)
```

The workflow becomes:

```text
Question
    ↓
Retriever
    ↓
Candidate Nodes
    ↓
Postprocessor
    ↓
Filtered/Reranked Nodes
    ↓
Response Synthesizer
    ↓
LLM
    ↓
Answer
```

For example, the retriever returns:

```text
Node A → score 0.82
Node B → score 0.71
Node C → score 0.32
Node D → score 0.20
```

With a similarity cutoff of 0.5, after filtering:

```text
Node A → 0.82
Node B → 0.71
```

> The exact meaning and scale of scores depend on the retrieval method and similarity metric.

---

## 6. Response Synthesizer

**File:** `06_response_synthesizer.py`

The Response Synthesizer is responsible for using the retrieved information to produce the final response.

```text
User Question
      +
Retrieved Nodes
      ↓
Response Synthesizer
      ↓
LLM
      ↓
Final Response
```

Example:

```python
response_synthesizer = get_response_synthesizer()
```

It can be combined with a Retriever and Query Engine.

---

## 7. Query Engine with ChromaDB

**File:** `07_query_engine_with_chroma.py`

Here we connect:

```text
LlamaIndex
     ↓
VectorStoreIndex
     ↓
ChromaDB
     ↓
Query Engine
```

Chroma is used as the persistent vector store.

```python
chroma_client = chromadb.PersistentClient(
    path="./chroma_data"
)
```

Then:

```python
chroma_collection = chroma_client.get_or_create_collection(
    name="query_engine_demo"
)
```

LlamaIndex connects to it through:

```python
vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)
```

Then:

```python
storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)
```

Finally:

```python
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context
)
```

This gives us:

```text
Documents
    ↓
Nodes
    ↓
Embeddings
    ↓
ChromaDB
    ↓
VectorStoreIndex
    ↓
Query Engine
    ↓
Answer
```

---

## 8. SubQuestion Query Engine

**File:** `08_sub_question_query_engine.py`

A normal Query Engine works well for simple questions. But some questions are complex. For example:

```text
"Compare deadlock in Operating Systems
with reliability mechanisms in TCP."
```

This question contains multiple concepts. A SubQuestion Query Engine can conceptually break the question into smaller questions:

```text
Original Question
       ↓
 ┌─────┴─────┐
 ↓           ↓
Subquestion  Subquestion
   1             2
 ↓               ↓
OS Engine    Network Engine
   ↓               ↓
Answer 1       Answer 2
       \         /
        \       /
         ↓     ↓
       Combined
        Answer
```

This is useful for:

- Research questions
- Comparisons
- Multi-domain questions
- Questions requiring multiple sources

---

## 9. Router Query Engine

**File:** `09_router_query_engine.py`

A Router Query Engine chooses the appropriate Query Engine for a question.

Suppose we have:

- Operating Systems Index
- DBMS Index
- Computer Networks Index

The router decides where the question should go:

```text
"What is deadlock?"       → Router → Operating Systems Query Engine
"What is normalization?"  → Router → DBMS Query Engine
"What is TCP?"            → Router → Computer Networks Query Engine
```

Architecture:

```text
                     User Query
                         ↓
                       Router
                    ↙    ↓    ↘
                   ↓     ↓     ↓
                  OS    DBMS  Network
                Engine Engine Engine
                   ↓     ↓     ↓
                   └─────┼─────┘
                         ↓
                      Answer
```

### Router vs SubQuestion

This distinction is important.

- **Router:** *"Which engine should answer this question?"*
- **SubQuestion:** *"What smaller questions should I ask to answer this complex question?"*

---

## 10. Knowledge Graph Query Engine

**File:** `10_knowledge_graph_query_engine.py`

Knowledge Graph based querying focuses on **relationships between entities**.

```text
Python
   │
   └── used_for ──→ Machine Learning
                         │
                         └── branch_of ──→ Artificial Intelligence
```

Instead of only asking *"What text is semantically similar?"*, we can reason through relationships:

```text
Python
  ↓
Machine Learning
  ↓
Artificial Intelligence
```

This can be useful for:

- Relationship-based questions
- Multi-hop reasoning
- Entity relationships
- Knowledge graphs

> **Important:** Some older Knowledge Graph APIs in LlamaIndex are legacy-style APIs. If you use this file with a newer LlamaIndex version and encounter an API error, check the current LlamaIndex documentation before changing your environment.

---

## 11. Streaming Query Engine

**File:** `11_streaming_query_engine.py`

Normally:

```text
Question
    ↓
LLM generates complete answer
    ↓
Answer displayed
```

With streaming:

```text
Question
    ↓
LLM
    ↓
"Deadlock..."
" occurs..."
" when..."
" processes..."
       ↓
Displayed continuously
```

Example:

```python
query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=2
)
```

Then:

```python
response = query_engine.query(question)

response.print_response_stream()
```

> **Important:** Streaming does not change the basic retrieval process. It mainly changes how the generated response is delivered to the user.

```text
Retrieval
    ↓
Same
    ↓
LLM generation
    ↓
Streaming output
```

This is especially useful for:

- Chatbots
- Interactive assistants
- Long responses
- Better perceived responsiveness

---

## 12. Custom Prompt Query Engine

**File:** `12_custom_prompt_query_engine.py`

A Query Engine can use a custom prompt to control how the LLM generates the answer.

```python
custom_prompt = PromptTemplate(
    """
    You are a friendly Computer Science teacher.

    Answer the student's question using ONLY
    the information provided in the context.

    Explain in simple English.

    Context:
    {context_str}

    Student's question:
    {query_str}

    Answer:
    """
)
```

Then:

```python
query_engine = index.as_query_engine(
    similarity_top_k=2,
    text_qa_template=custom_prompt
)
```

The workflow becomes:

```text
User Question
      ↓
Retriever
      ↓
Relevant Nodes
      ↓
Custom Prompt
 ┌────┼─────────────┐
 ↓    ↓             ↓
Rules Context    Question
 └────┼─────────────┘
      ↓
     LLM
      ↓
 Final Answer
```

### Why use a custom prompt?

You can specify:

- Answer style
- Language
- Level of explanation
- Formatting
- Restrictions
- Whether to use only retrieved context
- Whether to provide examples

For example:

- *"You are a Computer Science teacher."*
- *"Explain in simple English."*
- *"Use bullet points."*
- *"Do not invent information."*
- *"Say when the answer is not present in the context."*

---

## 🔄 Complete Query Engine Architecture

After completing this module, the overall architecture should look like:

```text
                         User Query
                              │
                              ↓
                       ┌─────────────┐
                       │ Query Engine│
                       └──────┬──────┘
                              │
                              ↓
                         ┌─────────┐
                         │Retriever│
                         └────┬────┘
                              │
                              ↓
                       Retrieved Nodes
                              │
                              ↓
                       ┌─────────────┐
                       │Postprocessor│
                       └──────┬──────┘
                              │
                              ↓
                       Filtered Nodes
                              │
                              ↓
                    ┌──────────────────┐
                    │Response          │
                    │Synthesizer       │
                    └────────┬─────────┘
                             │
                             ↓
                            LLM
                             │
                             ↓
                       Final Answer
```

---

## 🧠 Important Concepts

### Index

An Index organizes information so that it can be retrieved efficiently.

Examples: `VectorStoreIndex`, `SummaryIndex`, `DocumentSummaryIndex`, `TreeIndex`, `KeywordTableIndex`, `KnowledgeGraphIndex`

### Retriever

The Retriever finds relevant Nodes.

```text
Query → Retriever → Relevant Nodes
```

### Query Engine

The Query Engine coordinates the complete question-answering process.

```text
Query
 ↓
Retrieve
 ↓
Process
 ↓
Synthesize
 ↓
LLM
 ↓
Answer
```

### Postprocessor

Processes retrieved nodes before final response generation.

```text
Retrieved Nodes → Postprocessor → Better/Filtered Nodes
```

### Response Synthesizer

Uses the query and retrieved information to construct the final response.

```text
Query + Retrieved Nodes → Response Synthesizer → LLM → Answer
```

---

## ⚖️ Important Differences

| Component | Main Responsibility |
|---|---|
| Index | Organizes information |
| Retriever | Finds relevant Nodes |
| Postprocessor | Filters/reranks retrieved Nodes |
| Response Synthesizer | Helps construct the final response |
| Query Engine | Orchestrates the complete QA process |
| LLM | Generates the natural-language answer |

---

## 🔥 Query Engine Types

| Query Engine | Main Purpose |
|---|---|
| Query Engine | General question answering |
| `RetrieverQueryEngine` | Custom retrieval pipeline |
| `SubQuestionQueryEngine` | Break complex questions into subquestions |
| `RouterQueryEngine` | Select the appropriate query engine |
| Knowledge Graph Query Engine | Relationship/graph-based querying |

---

## 🌍 Real-World Applications

### 1. PDF Chatbot

```text
PDF
 ↓
Documents
 ↓
Nodes
 ↓
Embeddings
 ↓
Vector Store
 ↓
Retriever
 ↓
Query Engine
 ↓
LLM
 ↓
Answer
```