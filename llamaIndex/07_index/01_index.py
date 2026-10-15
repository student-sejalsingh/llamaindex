from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure the Embedding Model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Create Documents
# --------------------------------------------------

documents = [
    Document(
        text="Deadlock occurs when processes wait indefinitely for resources."
    ),
    Document(
        text="Binary search works efficiently on sorted arrays."
    ),
    Document(
        input_path="../03_documents/data/03_txt/operating_systems.txt",
        recursive=True,
        required_exts=[".txt"],


    )
]


# --------------------------------------------------
# 3. Create an Index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(
    documents
)


# --------------------------------------------------
# 4. Display Information
# --------------------------------------------------

print("\nIndex created successfully!")

print("\nIndex type:")
print(type(index))