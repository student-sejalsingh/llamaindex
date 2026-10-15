from llama_index.embeddings.ollama import OllamaEmbedding
import numpy as np


# --------------------------------------------------
# 1. Create Embedding Model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Our Documents
# --------------------------------------------------

documents = [
    "Deadlock occurs when processes wait indefinitely for resources.",
    "Binary search works efficiently on sorted arrays.",
    "Normalization reduces redundancy in databases."
]


# --------------------------------------------------
# 3. Convert Documents into Vectors
# --------------------------------------------------

embeddings = []

for document in documents:
    embedding = embed_model.get_text_embedding(document)
    embeddings.append(embedding)


# --------------------------------------------------
# 4. Store Vectors in Memory
# --------------------------------------------------

vector_store = []

for document, embedding in zip(documents, embeddings):

    vector_store.append({
        "text": document,
        "embedding": embedding
    })


# --------------------------------------------------
# 5. Display Vector Store
# --------------------------------------------------

print("\n" + "=" * 70)
print("VECTOR STORE")
print("=" * 70)

print("\nNumber of stored documents:", len(vector_store))

for i, item in enumerate(vector_store, start=1):

    print("\n" + "-" * 70)

    print(f"Document {i}:")
    print(item["text"])

    print("\nEmbedding Dimension:")
    print(len(item["embedding"]))

    print("\nFirst 5 Vector Values:")
    print(item["embedding"][:5])