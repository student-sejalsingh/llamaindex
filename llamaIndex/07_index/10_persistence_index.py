from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)

from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Create documents
# --------------------------------------------------

documents = [
    Document(
        text="Deadlock occurs when processes wait indefinitely "
             "for resources."
    ),
    Document(
        text="Binary search works efficiently on sorted arrays."
    ),
    Document(
        text="Database normalization reduces data redundancy."
    ),
]


# --------------------------------------------------
# 3. Create index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("Index created!")


# --------------------------------------------------
# 4. Persist index
# --------------------------------------------------

index.storage_context.persist(
    persist_dir="./storage"
)

print("Index saved to ./storage")


# --------------------------------------------------
# 5. Create query engine
# --------------------------------------------------

query_engine = index.as_query_engine()

response = query_engine.query(
    "What is deadlock?"
)

print("\nAnswer:")
print(response)