from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# --------------------------------------------------
# 1. Configure embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Configure LLM
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# --------------------------------------------------
# 3. Create documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.
        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm.
        It works on sorted arrays by repeatedly dividing
        the search space into two halves.
        """
    ),

    Document(
        text="""
        TCP is a connection-oriented transport protocol.
        It provides reliable and ordered delivery of data.
        """
    ),
]


# --------------------------------------------------
# 4. Create VectorStoreIndex
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("\nVectorStoreIndex created!")


# ==================================================
# PART 1 — RETRIEVER
# ==================================================

print("\n" + "=" * 60)
print("PART 1: RETRIEVER")
print("=" * 60)


# Create a retriever directly from the index
retriever = index.as_retriever(
    similarity_top_k=2
)


question = input("\nEnter your question: ")


# Retrieve relevant nodes
retrieved_nodes = retriever.retrieve(question)


print("\nRetrieved Nodes:")

for i, node in enumerate(retrieved_nodes, start=1):

    print("\n" + "-" * 50)
    print(f"Node {i}")
    print("-" * 50)

    print("Score:", node.score)
    print("Text:")
    print(node.text)


# ==================================================
# PART 2 — QUERY ENGINE
# ==================================================

print("\n" + "=" * 60)
print("PART 2: QUERY ENGINE")
print("=" * 60)


# Create Query Engine
query_engine = index.as_query_engine(
    similarity_top_k=2
)


# Ask the same question
response = query_engine.query(question)


print("\nFinal Answer:")
print(response)