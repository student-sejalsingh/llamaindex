from llama_index.core import Document


# Imagine this data came from an API or database
data = {
    "title": "Binary Search",
    "content": """
Binary Search is an efficient searching algorithm.

It works on sorted data by repeatedly dividing
the search space into two halves.

Time Complexity: O(log n)
Space Complexity: O(1)
""",
    "subject": "Data Structures and Algorithms",
    "topic": "Searching",
    "difficulty": "Beginner",
    "source": "computer_science_database"
}


# Convert external data into a LlamaIndex Document
document = Document(
    text=data["content"],
    metadata={
        "title": data["title"],
        "subject": data["subject"],
        "topic": data["topic"],
        "difficulty": data["difficulty"],
        "source": data["source"],
    },
)


# Display the Document
print("\n📄 Custom Document")
print("=" * 60)

print("\n📝 Content:")
print(document.text)

print("\n🏷️ Metadata:")
print(document.metadata)