import chromadb

from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Load Embedding Model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Connect to ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="cs_notes"
)


# --------------------------------------------------
# 3. User Query
# --------------------------------------------------

query = input("\nAsk a question: ")


# --------------------------------------------------
# 4. Create Query Embedding
# --------------------------------------------------

query_embedding = embed_model.get_query_embedding(
    query
)


# --------------------------------------------------
# 5. Try Different Top-K Values
# --------------------------------------------------

k_values = [1, 3, 5]


for k in k_values:

    print("\n" + "=" * 70)
    print(f"TOP-K = {k}")
    print("=" * 70)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )


    # --------------------------------------------------
    # 6. Display Results
    # --------------------------------------------------

    for rank, document in enumerate(
        results["documents"][0],
        start=1
    ):

        print("\n" + "-" * 70)

        print(f"Rank: {rank}")

        print("\nDocument ID:")
        print(results["ids"][0][rank - 1])

        print("\nText:")
        print(document)

        print("\nDistance:")
        print(results["distances"][0][rank - 1])

        print("\nMetadata:")
        print(results["metadatas"][0][rank - 1])