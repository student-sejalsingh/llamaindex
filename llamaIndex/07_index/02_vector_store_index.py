from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure Embedding Model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Create Documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources held by each other.
        """
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays.
        """
    ),

    Document(
        text="""
        Database normalization reduces data redundancy
        and improves database design.
        """
    )
]


# --------------------------------------------------
# 3. Create VectorStoreIndex
# --------------------------------------------------

index = VectorStoreIndex.from_documents(
    documents
)


# --------------------------------------------------
# 4. Display Index Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("VECTOR STORE INDEX")
print("=" * 60)

print("\nIndex created successfully!")

print("\nIndex Type:")
print(type(index))


# --------------------------------------------------
# 5. Display Internal Vector Store Information
# --------------------------------------------------

print("\nVector Store:")
print(index._vector_store)