import chromadb


# --------------------------------------------------
# 1. Create a ChromaDB Client
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_data"
)


# --------------------------------------------------
# 2. Create a Collection
# --------------------------------------------------

collection = client.get_or_create_collection(
    name="computer_science_notes"
)


# --------------------------------------------------
# 3. Add Documents and Embeddings
# --------------------------------------------------

collection.add(
    ids=["doc1", "doc2", "doc3"],

    documents=[
        "Deadlock occurs when processes wait indefinitely for resources.",
        "Binary search works efficiently on sorted arrays.",
        "Normalization reduces redundancy in databases."
    ],

    embeddings=[
        [0.1, 0.2, 0.3, 0.4],
        [0.5, 0.6, 0.7, 0.8],
        [0.9, 0.1, 0.2, 0.3]
    ],

    metadatas=[
        {"subject": "Operating Systems", "topic": "Deadlock"},
        {"subject": "DSA", "topic": "Searching"},
        {"subject": "DBMS", "topic": "Normalization"}
    ]
)


# --------------------------------------------------
# 4. Display Collection Information
# --------------------------------------------------

print("\nCollection Name:")
print(collection.name)

print("\nTotal Stored Documents:")
print(collection.count())


# --------------------------------------------------
# 5. Retrieve Stored Documents
# --------------------------------------------------

results = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

print("\nStored Data:")

for i, doc_id in enumerate(results["ids"]):
    print("\n" + "=" * 50)
    print("ID:", doc_id)
    print("Document:", results["documents"][i])
    print("Metadata:", results["metadatas"][i])
    print("Embedding:", results["embeddings"][i])