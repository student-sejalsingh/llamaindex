from llama_index.core import Document

# Create a document manually
document = Document(
    text="""
Binary Search is an efficient searching algorithm.

It works on sorted arrays.

Time Complexity: O(log n)
""",
    metadata={
        "author": "Sejal",
        "category": "DSA",
        "difficulty": "Easy"
    },
)

print(document)