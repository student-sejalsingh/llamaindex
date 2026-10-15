
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.retrievers import VectorIndexRetriever

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# 1. Configure the embedding model
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

# 2. Configure the LLM
Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# 3. Create sample documents
documents = [
    Document(
        text="""
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.

        The four necessary conditions for deadlock are
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
        """,
        metadata={"subject": "Operating Systems", "topic": "Deadlock"},
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays.

        It repeatedly divides the search space into two halves.
        Its time complexity is O(log n).
        """,
        metadata={"subject": "DSA", "topic": "Binary Search"},
    ),

    Document(
        text="""
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """,
        metadata={"subject": "Computer Networks", "topic": "TCP"},
    ),
]


# 4. Build the vector index
index = VectorStoreIndex.from_documents(documents)

print("Vector index created successfully!")


# 5. Create the retriever explicitly
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2,
)


# 6. Accept a question
question = input("\nAsk a question: ")


# 7. Retrieve relevant nodes
retrieved_nodes = retriever.retrieve(question)


# 8. Display the results
print("\n" + "=" * 60)
print("RETRIEVAL RESULTS")
print("=" * 60)

if not retrieved_nodes:
    print("No relevant nodes were retrieved.")

for i, result in enumerate(retrieved_nodes, start=1):
    print(f"\nNode {i}")
    print("-" * 60)

    print("Score:", result.score)
    print("Metadata:", result.node.metadata)
    print("Content:")
    print(result.node.get_content())
