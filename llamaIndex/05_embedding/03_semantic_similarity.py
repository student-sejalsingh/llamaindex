
from llama_index.embeddings.ollama import OllamaEmbedding
import numpy as np


# --------------------------------------------------
# Step 1: Initialize the embedding model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# Step 2: Create sentences
# --------------------------------------------------

text1 = "Binary search works on sorted arrays."

text2 = "Binary search is used to efficiently find elements in sorted data."

text3 = "The weather is very pleasant today."


# --------------------------------------------------
# Step 3: Generate embeddings
# --------------------------------------------------

embedding1 = embed_model.get_text_embedding(text1)
embedding2 = embed_model.get_text_embedding(text2)
embedding3 = embed_model.get_text_embedding(text3)


# Convert lists to NumPy arrays
vector1 = np.array(embedding1)
vector2 = np.array(embedding2)
vector3 = np.array(embedding3)


# --------------------------------------------------
# Step 4: Define Cosine Similarity
# --------------------------------------------------

def cosine_similarity(vector_a, vector_b):
    """
    Calculate cosine similarity between two vectors.
    """

    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    similarity = dot_product / (magnitude_a * magnitude_b)

    return similarity


# --------------------------------------------------
# Step 5: Calculate similarities
# --------------------------------------------------

similarity_1_2 = cosine_similarity(vector1, vector2)
similarity_1_3 = cosine_similarity(vector1, vector3)


# --------------------------------------------------
# Step 6: Display results
# --------------------------------------------------

print("\n" + "=" * 60)
print("SEMANTIC SIMILARITY")
print("=" * 60)

print("\nText 1:")
print(text1)

print("\nText 2:")
print(text2)

print("\nText 3:")
print(text3)


print("\n" + "-" * 60)

print("\nSimilarity between Text 1 and Text 2:")
print(round(similarity_1_2, 4))

print("\nSimilarity between Text 1 and Text 3:")
print(round(similarity_1_3, 4))

