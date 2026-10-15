import chromadb

from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    Settings,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.ollama import Ollama


# --------------------------------------------------
# 1. Configure embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Configure LLM
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# --------------------------------------------------
# 3. Create Chroma persistent client
# --------------------------------------------------

chroma_client = chromadb.PersistentClient(
    path="./chroma_data"
)


# --------------------------------------------------
# 4. Create / get Chroma collection
# --------------------------------------------------

chroma_collection = chroma_client.get_or_create_collection(
    name="cs_notes"
)


# --------------------------------------------------
# 5. Connect Chroma with LlamaIndex
# --------------------------------------------------

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)


storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)


# --------------------------------------------------
# 6. Create documents
# --------------------------------------------------

documents = [
    Document(
        text="Deadlock occurs when processes wait indefinitely "
             "for resources."
    ),
    Document(
        text="Binary search is an efficient searching algorithm "
             "that works on sorted arrays."
    ),
    Document(
        text="Database normalization reduces redundancy "
             "and improves database design."
    ),
]


# --------------------------------------------------
# 7. Create VectorStoreIndex
# --------------------------------------------------

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)


print("\nIndex created with Chroma!")


# --------------------------------------------------
# 8. Create query engine
# --------------------------------------------------

query_engine = index.as_query_engine(
    similarity_top_k=2
)


# --------------------------------------------------
# 9. Ask question
# --------------------------------------------------

question = input("\nAsk a question: ")

response = query_engine.query(question)

print("\nAnswer:")
print(response)