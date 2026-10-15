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
# 2. Keep chunk size fixed
# --------------------------------------------------

chunk_size = 300

# Test different overlap values
overlap_values = [0, 20, 50, 100]


# --------------------------------------------------
# 3. Compare overlap values
# --------------------------------------------------

for overlap in overlap_values:

    print("\n" + "=" * 70)
    print(f"🔹 CHUNK SIZE: {chunk_size}")
    print(f"🔹 CHUNK OVERLAP: {overlap}")
    print("=" * 70)

    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )

    nodes = splitter.get_nodes_from_documents(documents)

    print("📦 Total Nodes:", len(nodes))

    # Display first two nodes
    for i, node in enumerate(nodes[:2]):

        print("\n" + "-" * 60)
        print(f"Node {i + 1}")
        print("-" * 60)

        print(node.text[:500])