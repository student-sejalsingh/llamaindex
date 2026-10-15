# Module 03 — Documents

## 📌 Overview

A `Document` is one of the basic building blocks in LlamaIndex.

It represents a piece of content that LlamaIndex can process and eventually use in applications such as:

* RAG systems
* Question-answering systems
* Chatbots
* Knowledge bases
* AI agents

The original data does not have to come from one specific place.

It can come from:

* PDF files
* Markdown files
* TXT files
* HTML/web pages
* Databases
* APIs
* User uploads
* Cloud storage
* Other external systems

The general idea is:

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

1. What a LlamaIndex `Document` is.
2. How to create a `Document` manually.
3. How to load documents from a directory.
4. How PDF files are ingested.
5. How web pages can become Documents.
6. How Markdown files are loaded.
7. What metadata is.
8. The difference between automatic and custom metadata.
9. How external data can be converted into a `Document`.
10. Why Documents are important for RAG.

---

# 📁 Folder Structure

```text
03_documents/
│
├── data/
│   ├── 01_pdf/
│   │   ├── os_notes.pdf
│   │   └── dbms.pdf
│   │
│   ├── 02_md/
│   │   ├── merge_sort.md
│   │   └── normalization.md
│   │
│   ├── 03_txt/
│   │   ├── deadlock.txt
│   │   └── tcp_udp.txt
│   │
│   └── 04_html/
│       └── binary_search.html
│
├── 01_document.py
├── 02_simple_directory_reader.py
├── 03_pdf_reader.py
├── 04_web_page_reader.py
├── 05_markdown_reader.py
├── 06_metadata.py
├── 07_custom_document.py
└── README.md
```

---

# 1. What is a Document?

A LlamaIndex `Document` is a standardized representation of content.

Conceptually:

```text
Document
│
├── text
│
├── metadata
│
└── other document information
```

For example:

```python
from llama_index.core import Document

document = Document(
    text="Binary Search is a searching algorithm.",
    metadata={
        "subject": "DSA",
        "topic": "Searching"
    }
)
```

The actual content is stored in:

```python
document.text
```

Metadata is available through:

```python
document.metadata
```

---

# 2. `01_document.py`

This file demonstrates how to manually create a Document.

```python
from llama_index.core import Document

document = Document(
    text="Binary Search is an efficient searching algorithm.",
    metadata={
        "subject": "DSA",
        "topic": "Searching",
        "difficulty": "Beginner"
    }
)
```

### Important point

This approach is useful for:

* Learning
* Small examples
* Custom data
* Data coming from APIs or databases

In real applications, we usually don't manually type all the content.

---

# 3. `02_simple_directory_reader.py`

`SimpleDirectoryReader` is used to load files from a directory.

Example:

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(
    input_dir="data",
    recursive=True
).load_data()
```

If the directory contains:

```text
data/
├── PDF
├── Markdown
├── TXT
└── HTML
```

the reader loads the supported files and converts them into Documents.

Conceptually:

```text
Files
 ↓
SimpleDirectoryReader
 ↓
Documents
```

### Why `recursive=True`?

Our dataset contains subdirectories:

```text
data/
├── 01_pdf/
├── 02_md/
├── 03_txt/
└── 04_html/
```

`recursive=True` allows the reader to search inside those subdirectories.

---

# 4. `03_pdf_reader.py`

This file focuses on PDF ingestion.

Install the optional PDF reader dependencies before running the example:

```bash
pip install llama-index-readers-file pymupdf
```

Example:

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import PyMuPDFReader

documents = SimpleDirectoryReader(
    input_dir="data/01_pdf",
    required_exts=[".pdf"],
    file_extractor={".pdf": PyMuPDFReader()},
).load_data()
```

Passing a PDF reader explicitly is important when the optional PDF reader
integration is not installed. Without it, `SimpleDirectoryReader` may treat a
PDF as a generic text file and return compressed PDF bytes instead of extracted
text.

This allows us to focus specifically on PDF files.

### Important distinction

`SimpleDirectoryReader` can already load supported PDF files.

We are studying PDF loading separately so that we understand how PDF ingestion works and what problems can appear later.

For example:

* Normal text PDFs
* Scanned PDFs
* OCR requirements
* Tables
* Images
* Page-level processing

---

# 5. `04_web_page_reader.py`

LlamaIndex can also ingest information from web pages.

Example:

```python
from llama_index.readers.web import SimpleWebPageReader

url = "https://en.wikipedia.org/wiki/Binary_search_algorithm"

documents = SimpleWebPageReader(
    html_to_text=True
).load_data([url])
```

The general flow is:

```text
Website
   ↓
Web Reader
   ↓
Extracted Text
   ↓
Document
```

### Real-world usage

The URL could come dynamically from:

* A database
* User input
* An API
* A list of trusted websites
* A scheduled ingestion process

It does not have to be hard-coded.

---

# 6. `05_markdown_reader.py`

Markdown files can also be loaded into Documents.

Example:

```python
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader(
    input_dir="data/02_md",
    required_exts=[".md"]
).load_data()
```

For example:

```text
merge_sort.md
       ↓
Markdown reader
       ↓
Document
```

Markdown is useful for storing:

* Technical documentation
* Notes
* Tutorials
* README files
* Structured knowledge

---

# 7. `06_metadata.py`

Metadata is information **about the content**.

For example:

```text
Document
│
├── Content
│
└── Metadata
     ├── file_name
     ├── file_path
     ├── file_type
     ├── subject
     ├── topic
     └── difficulty
```

## Automatic Metadata

When files are loaded, the reader can automatically provide information such as:

```python
document.metadata
```

Possible fields include:

```text
file_name
file_path
file_type
file_size
creation_date
modification_date
```

The exact fields depend on the reader and source.

## Custom Metadata

Your application can also add its own metadata.

Example:

```python
metadata={
    "subject": "Operating Systems",
    "topic": "Deadlock",
    "semester": "5",
    "exam": "GATE",
    "difficulty": "Intermediate"
}
```

### Why is metadata useful?

Suppose you have 10,000 documents.

Instead of searching everything blindly, you can use metadata to narrow the search.

For example:

```text
exam = GATE
subject = Operating Systems
```

Then semantic retrieval can focus on the relevant content.

---

# 8. `07_custom_document.py`

Not all data comes from files.

In real applications, data can come from:

```text
Database
API
JSON
User Upload
Cloud Storage
Another Application
```

We can convert that data into a LlamaIndex Document.

For example:

```python
from llama_index.core import Document

data = {
    "title": "Binary Search",
    "content": "Binary Search works on sorted data.",
    "subject": "DSA",
    "topic": "Searching"
}

document = Document(
    text=data["content"],
    metadata={
        "title": data["title"],
        "subject": data["subject"],
        "topic": data["topic"],
        "source": "database"
    }
)
```

The important idea is:

```text
External Data
     ↓
Convert to Document
     ↓
LlamaIndex Pipeline
```

---

# 🌍 Real-World Data Sources

In a production application, data does not necessarily live on your laptop.

It can come from:

```text
PDF
TXT
Markdown
HTML
     │
     ├── Local Files
     │
     ├── S3
     ├── Google Drive
     ├── Database
     ├── API
     ├── Website
     ├── User Upload
     └── Cloud Storage
```

Different sources can eventually be normalized into:

```text
Document
```

This gives LlamaIndex a common representation of the content.

---

# 🏗️ Real-World RAG Architecture

Suppose we build a knowledge system for an education platform.

Data could come from:

```text
Government Website
       +
Teacher PDF Upload
       +
Database
       +
Cloud Storage
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
       LLM
       ↓
     Answer
```

The important point is that **Document is the bridge between the original data source and the rest of the LlamaIndex pipeline.**

---

# 🔑 Important Concepts

## Document vs File

A file is an object stored somewhere:

```text
os_notes.pdf
```

A Document is the representation of its content inside LlamaIndex:

```text
PDF
 ↓
Document
```

---

## Automatic Metadata vs Custom Metadata

```text
Automatic Metadata
        ↓
Information discovered from the source

Custom Metadata
        ↓
Information added by your application
```

Example:

```text
file_name = os_notes.pdf       ← automatic

subject = Operating Systems   ← custom
semester = 5                  ← custom
exam = GATE                   ← custom
```

---

# 🧠 Key Mental Model

Remember this:

```text
             DATA SOURCES
                  │
      ┌───────────┼───────────┐
      ↓           ↓           ↓
    Files       Website    Database
      ↓           ↓           ↓
      └───────────┼───────────┘
                  ↓
              DOCUMENT
                  ↓
                NODES
                  ↓
              EMBEDDINGS
                  ↓
            VECTOR STORE
                  ↓
              RETRIEVER
                  ↓
                 LLM
```

---

# ❓ Common Questions

### 1. Do I always need to create `Document` manually?

No.

For normal files, a reader can create Documents automatically.

```python
documents = SimpleDirectoryReader("data").load_data()
```

Manual Documents are useful when your data comes from APIs, databases, or custom sources.

---

### 2. Is a Document the same as a PDF?

No.

A PDF is a source file.

A Document is LlamaIndex's representation of the content.

---

### 3. Does every Document need custom metadata?

No.

Readers can provide basic metadata automatically.

Custom metadata is useful when your application needs additional information for organization, filtering, or retrieval.

---

### 4. Does `SimpleDirectoryReader` only read PDFs?

No.

It supports multiple common file types.

That's why it is useful for general directory ingestion.

---

### 5. What happens after Documents?

Documents are generally processed further into Nodes/chunks.

```text
Document
   ↓
Nodes
   ↓
Embeddings
   ↓
Vector Store
```

---

# 🧪 Practice Tasks

Before moving to the next module, try these:

### Task 1

Add another PDF to:

```text
data/01_pdf/
```

Run:

```text
03_pdf_reader.py
```

and observe the result.

### Task 2

Add another Markdown file to:

```text
data/02_md/
```

Run:

```text
05_markdown_reader.py
```

### Task 3

Run:

```text
02_simple_directory_reader.py
```

and compare the documents produced from:

```text
PDF
Markdown
TXT
HTML
```

### Task 4

Create a custom Document representing a database record.

For example:

```python
data = {
    "title": "TCP",
    "content": "TCP is a connection-oriented protocol.",
    "subject": "Computer Networks"
}
```

Convert it into a LlamaIndex Document.

---

# 🎯 Module 03 Summary

The main lesson of this module is:

> **LlamaIndex needs a common representation of your content, and `Document` provides that representation.**

Your data can originate from many places:

```text
PDF
TXT
Markdown
HTML
Website
API
Database
Cloud Storage
User Upload
```

but the ingestion layer can eventually turn that information into:

```text
Document
```

Then the next stage is:

```text
Document
    ↓
    ?
```

The missing piece is **Nodes**.

---

# 🚀 Next Module — Nodes & Text Splitters

In Module 04, we will learn:

* What is a Node?
* Why can't we simply embed an entire PDF?
* Document vs Node
* Chunking
* `SentenceSplitter`
* `TokenTextSplitter`
* Chunk size
* Chunk overlap
* Metadata inheritance
* How chunking affects RAG retrieval

The most important question will be:

> **If my PDF contains 50 pages, how does LlamaIndex turn that huge Document into useful pieces that the retriever can actually search?**
