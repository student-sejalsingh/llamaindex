from llama_index.embeddings.ollama import OllamaEmbedding


# Step 1: Initialize the embedding model
embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# Step 2: Prepare some text
text = """
Binary Search is a searching algorithm.
It works on sorted arrays by repeatedly
dividing the search space into two halves.
"""


# Step 3: Convert the text into an embedding
embedding = embed_model.get_text_embedding(text)


# Step 4: Display the results
print("\nOriginal Text:")
print(text)

print("\nEmbedding:")
print(embedding)

print("\nEmbedding Dimension:")
print(len(embedding))

print("\nFirst 10 Values:")
print(embedding[:10])