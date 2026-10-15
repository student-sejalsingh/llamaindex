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
# 3. Take User Query
# --------------------------------------------------

query = input("\nAsk a question: ")

query_embedding = embed_model.get_query_embedding(query)


# --------------------------------------------------
# 4. Choose Metadata Filter
# --------------------------------------------------

print("\nAvailable Subjects:")
print("1. Operating Systems")
print("2. Data Structures")
print("3. DBMS")

choice = input("\nChoose subject number: ")


subject_map = {
    "1": "Operating Systems",
    "2": "Data Structures",
    "3": "DBMS"
}

selected_subject = subject_map.get(choice)


if selected_subject is None:
    print("\nInvalid choice.")
    exit()


# --------------------------------------------------
# 5. Vector Search + Metadata Filter
# --------------------------------------------------

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5,

    where={
        "subject": selected_subject
    },

    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)


# --------------------------------------------------
# 6. Display Results
# --------------------------------------------------

print("\n" + "=" * 70)
print("FILTERED VECTOR SEARCH RESULTS")
print("=" * 70)

print("\nQuery:")
print(query)

print("\nSubject Filter:")
print(selected_subject)


for i, document in enumerate(results["documents"][0]):

    print("\n" + "-" * 70)

    print(f"Rank: {i + 1}")

    print("\nText:")
    print(document)

    print("\nMetadata:")
    print(results["metadatas"][0][i])

    print("\nDistance:")
    print(results["distances"][0][i])