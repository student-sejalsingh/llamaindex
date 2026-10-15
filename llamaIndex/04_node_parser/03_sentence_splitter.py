from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


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
# 2. Create SentenceSplitter
# --------------------------------------------------

splitter = SentenceSplitter(
    chunk_size=400,
    chunk_overlap=100,
)


# --------------------------------------------------
# 3. Convert Documents → Nodes
# --------------------------------------------------

nodes = splitter.get_nodes_from_documents(documents)


print("📦 Total Nodes:", len(nodes))


# --------------------------------------------------
# 4. Display the Nodes
# --------------------------------------------------

for i, node in enumerate(nodes[:10]):

    print("\n" + "=" * 70)
    print(f"📦 NODE {i + 1}")
    print("=" * 70)

    print("\n📝 Text:")
    print(node.text)

    print("\n📏 Characters:", len(node.text))

    print("\n🏷️ Metadata:")
    print(node.metadata)