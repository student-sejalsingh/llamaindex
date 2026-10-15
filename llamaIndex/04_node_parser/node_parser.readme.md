# Module 04 — Nodes & Node Parsers

## 📌 Overview

In Module 03, we learned how LlamaIndex converts different data sources such as PDF, Markdown, TXT, and HTML into **Documents**.

In this module, we learn how a large Document is divided into smaller pieces called **Nodes**.

Nodes are very important in RAG systems because the LLM usually does not need the entire document. Instead, relevant pieces of information are retrieved and provided to the LLM.

The basic pipeline is:

```text
Data Source
     ↓
  Document
     ↓
    Nodes
     ↓
 Embeddings
     ↓
 Vector Store
     ↓
  Retriever
     ↓
    LLM
```

---

# 🎯 Learning Objectives

After completing this module, you should understand:

* What is a Node?
* Difference between Document and Node
* How to create Nodes
* What is a Node Parser?
* How `SentenceSplitter` works
* What is `chunk_size`?
* What is `chunk_overlap`?
* Difference between `SentenceSplitter` and `TokenTextSplitter`
* How metadata is inherited by Nodes
* What are Node relationships?
* Why chunking is important for RAG

---

# 📁 Folder Structure

```text
04_node_parser/
│
├── 01_document_vs_node.py
├── 02_basic_node.py
├── 03_sentence_splitter.py
├── 04_chunk_size.py
├── 05_chunk_overlap.py
├── 06_token_text_splitter.py
├── 07_metadata_inheritance.py
└── README.md
```

---

# 1️⃣ Document vs Node

## Document

A Document represents a larger piece of content.

For example:

```text
deadlock.pdf
```

The entire PDF can become a Document.

```text
Document
│
├── text
├── metadata
└── other information
```

## Node

A Node represents a smaller piece of that Document.

For example:

```text
deadlock.pdf
      ↓
Document
      ↓
 ┌─────────┐
 │ Node 1  │
 ├─────────┤
 │ Node 2  │
 ├─────────┤
 │ Node 3  │
 ├─────────┤
 │ Node 4  │
 └─────────┘
```

### Why do we need Nodes?

Suppose a PDF contains 100 pages.

A user asks:

> What are the four necessary conditions for deadlock?

We don't want to send the entire 100-page PDF to the LLM.

Instead:

```text
100-page PDF
     ↓
   Nodes
     ↓
Retrieve relevant Nodes
     ↓
   LLM
     ↓
Answer
```

This makes RAG more efficient and relevant.

---

# 2️⃣ Node Structure

A Node can be thought of as:

```text
Node
│
├── text
├── metadata
├── node_id
└── relationships
```

### `text`

Contains the actual chunk of information.

Example:

```text
"Deadlock occurs when processes wait indefinitely
for resources held by other processes."
```

### `metadata`

Contains information describing the Node.

Example:

```python
{
    "subject": "Operating Systems",
    "topic": "Deadlock",
    "source": "deadlock.pdf"
}
```

### `node_id`

Every Node has a unique identifier.

Example:

```text
node_id = "abc123..."
```

This allows LlamaIndex to distinguish one Node from another.

### `relationships`

Relationships describe how a Node is connected to other Nodes or its source Document.

For example:

```text
Document
   │
   ├── Node 1
   │      │
   │      └── NEXT → Node 2
   │
   ├── Node 2
   │      │
   │      └── NEXT → Node 3
   │
   └── Node 3
```

Relationships help preserve the structure and context between pieces of information.

---

# 3️⃣ Node Parser

A **Node Parser** converts Documents into smaller Nodes.

```text
Document
    ↓
Node Parser
    ↓
Node 1
Node 2
Node 3
Node 4
```

LlamaIndex provides different node parsers.

Examples:

```text
SentenceSplitter
TokenTextSplitter
SemanticSplitter
```

In this module we mainly use:

```python
SentenceSplitter
```

---

# 4️⃣ SentenceSplitter

`SentenceSplitter` divides a Document into chunks while trying to preserve meaningful text boundaries such as sentences and paragraphs.

Example:

```python
from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = splitter.get_nodes_from_documents(documents)
```

The result is:

```text
Document
   ↓
SentenceSplitter
   ↓
Node 1
Node 2
Node 3
...
```

---

# 5️⃣ Chunk Size

`chunk_size` controls approximately how much content should be placed into each Node.

Example:

```python
SentenceSplitter(
    chunk_size=100
)
```

versus:

```python
SentenceSplitter(
    chunk_size=500
)
```

Generally:

```text
Small chunk size
      ↓
More Nodes
      ↓
More granular information
```

Whereas:

```text
Large chunk size
      ↓
Fewer Nodes
      ↓
More context per Node
```

### Important

`chunk_size` should not be interpreted as an exact number of characters.

For LlamaIndex's text splitters, it is primarily related to **tokens**, while the splitter also tries to respect natural text boundaries.

---

# 6️⃣ Chunk Overlap

Chunk overlap means that some content is repeated between neighboring Nodes.

Without overlap:

```text
Node 1:
A B C D E

Node 2:
F G H I J
```

With overlap:

```text
Node 1:
A B C D E

Node 2:
D E F G H
```

Here:

```text
D E
```

is shared between the two Nodes.

---

## Why use overlap?

Suppose an important sentence is near the boundary:

```text
Node 1:
"Deadlock requires four necessary conditions..."

Node 2:
"These conditions are mutual exclusion,
hold and wait..."
```

Without overlap, related information may be split.

With overlap:

```text
Node 1
   ↓
shared context
   ↓
Node 2
```

This helps preserve context.

---

# 7️⃣ Experimenting with Chunk Overlap

We tested:

```python
chunk_size = 300

overlap_values = [
    0,
    20,
    50,
    100
]
```

Example results from the PDF dataset:

```text
Overlap    Nodes
----------------
0          84
20         85
50         93
100        116
```

This demonstrates that increasing overlap can increase the number of Nodes.

Why?

Because more content is repeated between neighboring chunks.

---

# 8️⃣ Is More Overlap Always Better?

No.

There is a trade-off.

### Too little overlap

```text
Less repeated context
        ↓
Potentially broken context
```

### Too much overlap

```text
More repeated content
        ↓
More Nodes
        ↓
More embeddings
        ↓
More storage
        ↓
Potentially redundant retrieval
```

Therefore:

> The goal is not maximum overlap. The goal is useful context preservation.

---

# 9️⃣ TokenTextSplitter

Another splitter available in LlamaIndex is:

```python
TokenTextSplitter
```

Example:

```python
from llama_index.core.node_parser import TokenTextSplitter

splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = splitter.get_nodes_from_documents(documents)
```

### SentenceSplitter vs TokenTextSplitter

| Feature              | SentenceSplitter           | TokenTextSplitter                   |
| -------------------- | -------------------------- | ----------------------------------- |
| Main idea            | Natural text boundaries    | Token-based splitting               |
| Sentence awareness   | Yes                        | Less focused on sentence boundaries |
| Context preservation | Good                       | More direct token control           |
| Useful for           | Documents, notes, articles | Precise token-based chunking        |

For normal CS notes and technical documents, `SentenceSplitter` is a good starting point.

---

# 🔟 Metadata Inheritance

Documents can contain metadata:

```python
document = Document(
    text="Binary Search is an efficient searching algorithm.",
    metadata={
        "subject": "Data Structures",
        "topic": "Searching",
        "difficulty": "Beginner"
    }
)
```

When the Document is converted into Nodes, this metadata can be inherited by the Nodes.

```text
Document
│
├── subject: Data Structures
├── topic: Searching
└── difficulty: Beginner
        ↓
     Split
        ↓
 ┌─────────────┐
 │   Node 1    │
 │ subject     │
 │ topic       │
 │ difficulty  │
 └─────────────┘

 ┌─────────────┐
 │   Node 2    │
 │ subject     │
 │ topic       │
 │ difficulty  │
 └─────────────┘
```

This becomes very useful during retrieval.

---

# 1️⃣1️⃣ Why Metadata Matters in RAG

Suppose your database contains educational content:

```python
{
    "state": "Bihar",
    "district": "Saran",
    "class": "2",
    "subject": "Numeracy",
    "language": "Hindi"
}
```

Each Node can retain this information.

Later, the system can perform filtering such as:

```text
State = Bihar
Class = 2
Subject = Numeracy
Language = Hindi
```

This can make retrieval much more precise.

---

# 1️⃣2️⃣ Node Relationships

Nodes can also have relationships with other Nodes or their source Document.

Conceptually:

```text
Document
    │
    │ SOURCE
    ↓
 Node 1
    │
    │ NEXT
    ↓
 Node 2
    │
    │ NEXT
    ↓
 Node 3
```

Common relationship concepts include:

```text
SOURCE
PREVIOUS
NEXT
PARENT
CHILD
```

Relationships help LlamaIndex maintain connections between pieces of information.

---

# 1️⃣3️⃣ Complete RAG Pipeline

We have now reached an important point in understanding RAG.

```text
                DATA
                 │
                 ↓
        ┌─────────────────┐
        │    Document     │
        └─────────────────┘
                 │
                 ↓
        ┌─────────────────┐
        │   Node Parser   │
        └─────────────────┘
                 │
                 ↓
        ┌─────────────────┐
        │      Nodes      │
        └─────────────────┘
                 │
                 ↓
        ┌─────────────────┐
        │   Embeddings    │
        └─────────────────┘
                 │
                 ↓
        ┌─────────────────┐
        │  Vector Store   │
        └─────────────────┘
                 │
                 ↓
             Retriever
                 │
                 ↓
               LLM
                 │
                 ↓
              Answer
```

The next module will explain **Embeddings**.

---

# 🧠 Key Concepts to Remember

### Document

```text
Large source of information
```

### Node

```text
Smaller piece of a Document
```

### Node Parser

```text
Document → Nodes
```

### Chunk Size

```text
Controls approximate amount of content per chunk
```

### Chunk Overlap

```text
Shares some content between neighboring chunks
```

### Metadata

```text
Information describing the content
```

### Relationships

```text
Connections between Nodes/Documents
```

---

# 📝 Practice Tasks

Try the following experiments.

### Task 1

Change:

```python
chunk_size=100
```

to:

```python
chunk_size=500
```

Compare the number of Nodes.

---

### Task 2

Try:

```python
chunk_overlap=0
```

and:

```python
chunk_overlap=100
```

Compare the Nodes.

---

### Task 3

Print Node IDs:

```python
for node in nodes[:5]:
    print(node.node_id)
```

Notice that each Node has a different ID.

---

### Task 4

Print metadata:

```python
for node in nodes[:5]:
    print(node.metadata)
```

Observe how Document metadata appears on Nodes.

---

### Task 5

Inspect relationships:

```python
for node in nodes[:5]:
    print(node.relationships)
```

Observe how Nodes are connected to their source and neighboring Nodes.

---

# ✅ Module 04 Completion Checklist

```text
01_document_vs_node.py       ✅
02_basic_node.py             ✅
03_sentence_splitter.py      ✅
04_chunk_size.py             ✅
05_chunk_overlap.py          ✅
06_token_text_splitter.py    ✅
07_metadata_inheritance.py   ✅
README.md                    ✅
```

---

# 🚀 What's Next?

## Module 05 — Embeddings

In the next module we will answer:

> How does a computer understand the meaning of a Node?

For example:

```text
"How do I find an element in a sorted array?"
```

and:

```text
"Explain binary search."
```

contain different words but have similar meaning.

Embeddings convert text into numerical vectors:

```text
Text
 ↓
Embedding Model
 ↓
[0.12, -0.43, 0.87, ...]
```

Then we can compare vectors to find semantically similar content.

The next pipeline becomes:

```text
Document
   ↓
Nodes
   ↓
Embeddings        ← NEXT MODULE
   ↓
Vector Store
   ↓
Retriever
   ↓
LLM
```

**Module 05: Embeddings → turning text meaning into vectors.**
