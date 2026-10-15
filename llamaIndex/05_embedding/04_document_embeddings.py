
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# Step 1: Load Documents
# --------------------------------------------------

documents = SimpleDirectoryReader(
    input_dir="../03_documents/data/03_txt",
    recursive=True,
    required_exts=[".txt"],
).load_data()

print("\nDocuments Loaded:", len(documents))


# --------------------------------------------------
# Step 2: Convert Documents into Nodes
# --------------------------------------------------

splitter = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50,
)

nodes = splitter.get_nodes_from_documents(documents)

print("Total Nodes:", len(nodes))


# --------------------------------------------------
# Step 3: Initialize Embedding Model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# Step 4: Generate Embeddings for Nodes
# --------------------------------------------------

print("\nGenerating embeddings...")

for i, node in enumerate(nodes[:10], start=1):

    embedding = embed_model.get_text_embedding(
        node.text
    )

    print("\n" + "=" * 60)
    print(f"Node {i}")
    print("=" * 60)

    print("\nNode ID:")
    print(node.node_id)

    print("\nNode Text:")
    print(node.text[:300])

    print("\nEmbedding Dimension:")
    print(len(embedding))

    print("\nFirst 5 Values:")
    print(embedding[:5])