
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# Step 1: Initialize the embedding model
# --------------------------------------------------

embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# Step 2: Create different texts
# --------------------------------------------------

texts = [
    "Binary Search is a searching algorithm.",

    """
    Binary Search is an efficient searching algorithm.
    It works on sorted arrays by repeatedly dividing
    the search space into two halves.
    """,

    """
    Deadlock is a situation in an operating system
    where processes wait indefinitely for resources
    held by each other.
    """
]


# --------------------------------------------------
# Step 3: Generate embeddings
# --------------------------------------------------

for i, text in enumerate(texts, start=1):

    embedding = embed_model.get_text_embedding(text)

    print("\n" + "=" * 60)
    print(f"Text {i}")
    print("=" * 60)

    print("Text:")
    print(text.strip())

    print("\nEmbedding Dimension:")
    print(len(embedding))

    print("\nFirst 5 Values:")
    print(embedding[:5])
