from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter


# --------------------------------------------------
# 1. Load your PDF documents
# --------------------------------------------------

documents = SimpleDirectoryReader(
    input_dir="../03_documents/data/03_txt",
    recursive=True,
    required_exts=[".txt"],
).load_data()


print("\n📚 Documents Loaded:", len(documents))


# --------------------------------------------------
# 2. Create TokenTextSplitter
# --------------------------------------------------

splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
)


# --------------------------------------------------
# 3. Convert Documents → Nodes
# --------------------------------------------------

nodes = splitter.get_nodes_from_documents(documents)


print("\n📦 Total Nodes:", len(nodes))


# --------------------------------------------------
# 4. Display first few Nodes
# --------------------------------------------------

for i, node in enumerate(nodes[:5]):

    print("\n" + "=" * 70)
    print(f"📦 NODE {i + 1}")
    print("=" * 70)

    print("\n📝 Text:")
    print(node.text)

    print("\n📏 Approximate characters:", len(node.text))

    print("\n🏷️ Metadata:")
    print(node.metadata)