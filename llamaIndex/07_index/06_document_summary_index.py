from llama_index.core import Document, DocumentSummaryIndex
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding



# --------------------------------------------------
# 1. Configure LLM
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0
)

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)



# --------------------------------------------------
# 2. Create Documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Operating Systems manage computer hardware and software
        resources. They manage processes, memory, storage,
        and input/output devices.
        """,
        metadata={"subject": "Operating Systems"}
    ),

    Document(
        text="""
        Database normalization organizes relational database tables
        to reduce redundancy and improve data integrity.
        Normal forms include 1NF, 2NF, 3NF and BCNF.
        """,
        metadata={"subject": "DBMS"}
    ),

    Document(
        text="""
        Computer Networks allow computers to communicate with each
        other. Important concepts include the OSI model, TCP/IP,
        routing, switching, and network protocols.
        """,
        metadata={"subject": "Computer Networks"}
    )
]


# --------------------------------------------------
# 3. Create Document Summary Index
# --------------------------------------------------

index = DocumentSummaryIndex.from_documents(
    documents
)


# --------------------------------------------------
# 4. Display Index Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("DOCUMENT SUMMARY INDEX")
print("=" * 60)

print("\nIndex created successfully!")
print(index)
print("\nIndex Type:")
print(type(index))