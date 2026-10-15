
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# Step 1: Initialize the embedding model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# Step 2: Create a user query
# --------------------------------------------------

query = input("Enter your query: ")


# --------------------------------------------------
# Step 3: Convert the query into an embedding
# --------------------------------------------------

query_embedding = embed_model.get_query_embedding(query)


# --------------------------------------------------
# Step 4: Display the result
# --------------------------------------------------

print("\n" + "=" * 60)
print("QUERY EMBEDDING")
print("=" * 60)

print("\nUser Query:")
print(query)

print("\nEmbedding Dimension:")
print(len(query_embedding))

print("\nFirst 10 Values:")
print(query_embedding[:10])

