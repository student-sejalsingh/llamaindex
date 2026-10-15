from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


# --------------------------------------------------
# 1. Load PDF documents
# --------------------------------------------------

documents = SimpleDirectoryReader(
    input_dir="../03_documents/data/03_txt",
    recursive=True,
    required_exts=[".txt"],
).load_data()


print("\n📚 Documents Loaded:", len(documents))


# --------------------------------------------------
# 2. Test different chunk sizes
# --------------------------------------------------

chunk_sizes = [100, 200, 500, 1000]


for chunk_size in chunk_sizes:

    print("\n" + "=" * 70)
    print(f"🔹 CHUNK SIZE: {chunk_size}")
    print("=" * 70)

    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=20,
    )

    nodes = splitter.get_nodes_from_documents(documents)

    print("📦 Total Nodes:", len(nodes))

    # Show first 3 nodes
    for i, node in enumerate(nodes[:3]):

        print("\n" + "-" * 60)
        print(f"Node {i + 1}")
        print("-" * 60)

        print(node.text[:300])