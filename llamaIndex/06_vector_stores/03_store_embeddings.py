import chromadb

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Load Documents
# --------------------------------------------------

documents = SimpleDirectoryReader(
    input_dir="../03_documents/data/03_txt",
    recursive=True,
    required_exts=[".txt"],
).load_data()

print("\nDocuments Loaded:", len(documents))


# --------------------------------------------------
# 2. Convert Documents into Nodes
# --------------------------------------------------

splitter = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

nodes = splitter.get_nodes_from_documents(documents)

print("Total Nodes:", len(nodes))


# --------------------------------------------------
# 3. Create Embedding Model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 4. Create ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_data"
)

collection = client.get_or_create_collection(
    name="cs_notes"
)


# --------------------------------------------------
# 5. Generate Embeddings and Store Them
# --------------------------------------------------

print("\nGenerating embeddings and storing them...")

for i, node in enumerate(nodes):

    embedding = embed_model.get_text_embedding(
        node.text
    )

    collection.upsert(
        ids=[node.node_id],

        documents=[node.text],

        embeddings=[embedding],

        metadatas=[node.metadata]
    )

    print(f"Stored Node {i + 1}/{len(nodes)}")


# --------------------------------------------------
# 6. Display Collection Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("CHROMADB INFORMATION")
print("=" * 60)

print("\nCollection Name:")
print(collection.name)

print("\nTotal Vectors Stored:")
print(collection.count())