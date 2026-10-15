from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.core.retrievers import VectorIndexRetriever

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

        The four necessary conditions for deadlock are
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Deadlock",
        },
    ),

    Document(
        text="""
        A deadlock can occur when multiple processes
        compete for resources and each process waits
        for a resource held by another process.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Deadlock",
        },
    ),

    Document(
        text="""
        Deadlock prevention techniques attempt to ensure
        that at least one of the necessary conditions
        for deadlock cannot occur.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Deadlock Prevention",
        },
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays.

        It repeatedly divides the search space into two halves.
        Its time complexity is O(log n).
        """,
        metadata={
            "subject": "DSA",
            "topic": "Binary Search",
        },
    ),

    Document(
        text="""
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """,
        metadata={
            "subject": "Computer Networks",
            "topic": "TCP",
        },
    ),
]


# --------------------------------------------------
# 4. Create Vector Store Index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("\nVector index created successfully!")


# --------------------------------------------------
# 5. Ask the user for a question
# --------------------------------------------------

question = input("\nAsk a question: ")


# --------------------------------------------------
# 6. Test different Top-K values
# --------------------------------------------------

for k in [1, 3, 5]:

    print("\n" + "=" * 70)
    print(f"TOP-K = {k}")
    print("=" * 70)

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=k,
    )

    retrieved_nodes = retriever.retrieve(question)

    print(f"\nNumber of nodes retrieved: {len(retrieved_nodes)}")

    for i, result in enumerate(retrieved_nodes, start=1):

        print(f"\nNode {i}")
        print("-" * 50)

        print("Score:", result.score)
        print("Metadata:", result.node.metadata)

        print("\nContent:")
        print(result.node.get_content())