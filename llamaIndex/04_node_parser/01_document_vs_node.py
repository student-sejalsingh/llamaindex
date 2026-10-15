from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


# Load your actual text files
documents = SimpleDirectoryReader(
    input_dir="../03_documents/data/03_txt",
    recursive=True,
    required_exts=[".txt"],
).load_data()


print("\n📚 Documents:", len(documents))


# Create splitter
splitter = SentenceSplitter(
    chunk_size=100,
    chunk_overlap=20,
)


# Convert Documents → Nodes
nodes = splitter.get_nodes_from_documents(documents)


print("\n📦 Total Nodes:", len(nodes))


# Display nodes
for i, node in enumerate(nodes[:10]):

    print("\n" + "=" * 70)
    print(f"Node {i + 1}")
    print("=" * 70)

    print(node.text[:500])


# from llama_index.core import Document
# from llama_index.core.node_parser import SentenceSplitter


# # Create a sample Document
# document = Document(
#     text="""
# Binary Search is an efficient searching algorithm.

# It works on sorted arrays.

# The algorithm compares the target with the middle element.

# If the target is smaller, it searches the left half.

# If the target is larger, it searches the right half.

# The process continues until the element is found.

# The time complexity of Binary Search is O(log n).
# """
# )


# print("\n📄 DOCUMENT")
# print("=" * 60)

# print(document.text)


# # Create a text splitter
# splitter = SentenceSplitter(
#     chunk_size=100,
#     chunk_overlap=20,
# )


# # Convert Document → Nodes
# nodes = splitter.get_nodes_from_documents([document])


# print("\n\n📦 NODES")
# print("=" * 60)

# print("Total Nodes:", len(nodes))


# for i, node in enumerate(nodes):

#     print("\n" + "-" * 60)
#     print(f"Node {i + 1}")
#     print("-" * 60)

#     print(node.text)