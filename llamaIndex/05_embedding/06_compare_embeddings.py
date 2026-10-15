
from llama_index.embeddings.ollama import OllamaEmbedding
import numpy as np


# --------------------------------------------------
# Step 1: Initialize the embedding model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# Step 2: Create a user query
# --------------------------------------------------

query = "What are the necessary conditions for deadlock?"


# --------------------------------------------------
# Step 3: Create candidate documents / Nodes
# --------------------------------------------------

texts = [
    "Deadlock requires four necessary conditions: "
    "mutual exclusion, hold and wait, no preemption, and circular wait.",

    "Deadlock is a situation where processes wait indefinitely "
    "for resources held by each other.",

    "CPU scheduling determines which process gets the CPU next.",

    "Normalization in DBMS reduces data redundancy and "
    "improves database design.",

    "Binary search efficiently searches for an element "
    "in a sorted array."
]


# --------------------------------------------------
# Step 4: Generate query embedding
# --------------------------------------------------

query_embedding = embed_model.get_query_embedding(query)

query_vector = np.array(query_embedding)


# --------------------------------------------------
# Step 5: Define cosine similarity
# --------------------------------------------------

def cosine_similarity(vector_a, vector_b):

    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    return dot_product / (magnitude_a * magnitude_b)


# --------------------------------------------------
# Step 6: Calculate similarity
# --------------------------------------------------

results = []

for text in texts:

    text_embedding = embed_model.get_text_embedding(text)

    text_vector = np.array(text_embedding)

    similarity = cosine_similarity(
        query_vector,
        text_vector
    )

    results.append({
        "text": text,
        "similarity": similarity
    })


# --------------------------------------------------
# Step 7: Sort by similarity
# --------------------------------------------------

results.sort(
    key=lambda x: x["similarity"],
    reverse=True
)


# --------------------------------------------------
# Step 8: Display results
# --------------------------------------------------

print("\n" + "=" * 70)
print("SEMANTIC SEARCH RESULTS")
print("=" * 70)

print("\nQuery:")
print(query)

print("\nRanked Results:")

for rank, result in enumerate(results, start=1):

    print("\n" + "-" * 70)

    print(f"Rank: {rank}")

    print(
        f"Similarity: "
        f"{result['similarity']:.4f}"
    )

    print("Text:")
    print(result["text"])
