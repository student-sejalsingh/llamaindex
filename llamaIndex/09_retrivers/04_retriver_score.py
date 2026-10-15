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

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# --------------------------------------------------
# 2. Create documents
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
        Deadlock can occur when multiple processes compete
        for resources and each process waits for a resource
        held by another process.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Deadlock",
        },
    ),

    Document(
        text="""
        Deadlock prevention attempts to ensure that at least
        one of the necessary conditions for deadlock cannot
        occur.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Deadlock Prevention",
        },
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays. It repeatedly divides
        the search space into two halves.
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
# 3. Create vector index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)


# --------------------------------------------------
# 4. Create retriever
# --------------------------------------------------

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
)


# --------------------------------------------------
# 5. Ask question
# --------------------------------------------------

question = input("\nAsk a question: ")


# --------------------------------------------------
# 6. Retrieve nodes
# --------------------------------------------------

results = retriever.retrieve(question)


# --------------------------------------------------
# 7. Display scores
# --------------------------------------------------

print("\n" + "=" * 70)
print("RETRIEVAL RESULTS WITH SCORES")
print("=" * 70)

for i, result in enumerate(results, start=1):

    print(f"\nRank: {i}")
    print("-" * 70)

    print("Score:", result.score)

    print("Metadata:")
    print(result.node.metadata)

    print("\nContent:")
    print(result.node.get_content())