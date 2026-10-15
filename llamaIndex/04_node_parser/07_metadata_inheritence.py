from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter


# --------------------------------------------------
# 1. Create a Document with custom metadata
# --------------------------------------------------

document = Document(
    text="""
Binary Search is an efficient searching algorithm.

It works on sorted arrays.

The algorithm compares the target with the middle element.

If the target is smaller, search the left half.

If the target is larger, search the right half.

The time complexity of Binary Search is O(log n).
""",
    metadata={
        "subject": "Data Structures and Algorithms",
        "topic": "Searching",
        "difficulty": "Beginner",
        "source": "CS Notes",
    },
)


# --------------------------------------------------
# 2. Display Document metadata
# --------------------------------------------------

print("\n📄 DOCUMENT METADATA")
print("=" * 60)

print(document.metadata)


# --------------------------------------------------
# 3. Split Document into Nodes
# --------------------------------------------------

splitter = SentenceSplitter(
    chunk_size=100,
    chunk_overlap=20,
)

nodes = splitter.get_nodes_from_documents([document])


# --------------------------------------------------
# 4. Check Node metadata
# --------------------------------------------------

print("\n📦 TOTAL NODES:", len(nodes))


for i, node in enumerate(nodes):

    print("\n" + "=" * 60)
    print(f"NODE {i + 1}")
    print("=" * 60)

    print("\n📝 Text:")
    print(node.text)

    print("\n🏷️ Node Metadata:")
    print(node.metadata)