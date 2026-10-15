import chromadb

from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Load the Embedding Model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Connect to Existing ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="cs_notes"
)


# --------------------------------------------------
# 3. Take a User Query
# --------------------------------------------------

query = input("\nAsk a question about your notes: ")


# --------------------------------------------------
# 4. Convert Query into an Embedding
# --------------------------------------------------

query_embedding = embed_model.get_query_embedding(
    query
)

print("\nQuery embedding dimension:")
print(len(query_embedding))


# --------------------------------------------------
# 5. Search ChromaDB
# --------------------------------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)


# --------------------------------------------------
# 6. Display Search Results
# --------------------------------------------------

print("\n" + "=" * 70)
print("VECTOR SEARCH RESULTS")
print("=" * 70)

for i, document in enumerate(results["documents"][0]):

    print(f"\nResult {i + 1}")
    print("-" * 50)

    print("Document ID:")
    print(results["ids"][0][i])

    print("\nRelevant Text:")
    print(document)

    print("\nMetadata:")
    print(results["metadatas"][0][i])

    print("\nDistance:")
    print(results["distances"][0][i])