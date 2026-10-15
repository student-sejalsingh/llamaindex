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
# 2. Create documents with metadata
# --------------------------------------------------

documents = [
    Document(
        text="""
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.

        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Deadlock",
        },
    ),

    Document(
        text="""
        Process scheduling determines which process
        gets access to the CPU.
        Common scheduling algorithms include FCFS,
        SJF, Round Robin, and Priority Scheduling.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Scheduling",
        },
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays.

        It repeatedly divides the search space into two halves.
        """,
        metadata={
            "subject": "DSA",
            "topic": "Searching",
        },
    ),

    Document(
        text="""
        Database normalization reduces redundancy and
        helps organize data efficiently.

        Normal forms include 1NF, 2NF, 3NF and BCNF.
        """,
        metadata={
            "subject": "DBMS",
            "topic": "Normalization",
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
# 3. Create Vector Store Index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("\nVector index created successfully!")


# --------------------------------------------------
# 4. Ask user for a question
# --------------------------------------------------

question = input("\nAsk a question: ")


# --------------------------------------------------
# 5. Choose a subject filter
# --------------------------------------------------

subject = input(
    "\nEnter subject filter "
    "(Operating Systems / DSA / DBMS / Computer Networks): "
)


# --------------------------------------------------
# 6. Create metadata filter
# --------------------------------------------------

filters = {
    "subject": subject
}


# --------------------------------------------------
# 7. Create Retriever
# --------------------------------------------------

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,
    filters=filters,
)


# --------------------------------------------------
# 8. Retrieve nodes
# --------------------------------------------------

retrieved_nodes = retriever.retrieve(question)


# --------------------------------------------------
# 9. Display results
# --------------------------------------------------

print("\n" + "=" * 70)
print("FILTERED RETRIEVAL RESULTS")
print("=" * 70)

print("\nQuestion:", question)
print("Subject Filter:", subject)

if not retrieved_nodes:
    print("\nNo matching nodes found.")

for i, result in enumerate(retrieved_nodes, start=1):

    print(f"\nNode {i}")
    print("-" * 60)

    print("Score:", result.score)

    print("Metadata:")
    print(result.node.metadata)

    print("\nContent:")
    print(result.node.get_content())