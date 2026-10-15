from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


# --------------------------------------------------
# 1. Create a Document
# --------------------------------------------------

document = Document(
    text="""
Binary Search is an efficient searching algorithm.

It works on sorted arrays.

The algorithm compares the target element
with the middle element of the array.

If the target is smaller than the middle element,
the search continues in the left half.

If the target is larger than the middle element,
the search continues in the right half.

The process continues until the target is found
or the search range becomes empty.

The time complexity of Binary Search is O(log n).
"""
)


# --------------------------------------------------
# 2. Create a text splitter
# --------------------------------------------------

splitter = SentenceSplitter(
    chunk_size=100,
    chunk_overlap=20,
)


# --------------------------------------------------
# 3. Convert Document → Nodes
# --------------------------------------------------

nodes = splitter.get_nodes_from_documents([document])


# --------------------------------------------------
# 4. Display Node information
# --------------------------------------------------

print("\n📦 Total Nodes:", len(nodes))


for i, node in enumerate(nodes):

    print("\n" + "=" * 70)
    print(f"NODE {i + 1}")
    print("=" * 70)

    print("\n🆔 Node ID:")
    print(node.node_id)

    print("\n📝 Node Text:")
    print(node.text)

    print("\n🏷️ Metadata:")
    print(node.metadata)

    print("\n📊 Node Type:")
    print(type(node))