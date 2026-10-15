
from llama_index.core import (
    Document,
    Settings,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.retrievers.bm25 import BM25Retriever

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# --------------------------------------------------
# 1. Configure local models
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# --------------------------------------------------
# 2. Create sample documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources.

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

        TCP uses acknowledgements and retransmissions to
        support reliable data delivery.
        """,
        metadata={
            "subject": "Computer Networks",
            "topic": "TCP",
        },
    ),

    Document(
        text="""
        UDP is a connectionless transport layer protocol.
        It does not guarantee delivery or ordering of packets.
        It is commonly used in applications where low latency
        is important.
        """,
        metadata={
            "subject": "Computer Networks",
            "topic": "UDP",
        },
    ),

    Document(
        text="""
        Database normalization organizes relational tables
        to reduce redundancy and improve data integrity.

        Common normal forms include 1NF, 2NF, 3NF and BCNF.
        """,
        metadata={
            "subject": "DBMS",
            "topic": "Normalization",
        },
    ),
]


# --------------------------------------------------
# 3. Split documents into nodes
# --------------------------------------------------

splitter = SentenceSplitter(
    chunk_size=200,
    chunk_overlap=20,
)

nodes = splitter.get_nodes_from_documents(documents)

print("Total nodes:", len(nodes))


# --------------------------------------------------
# 4. Create a vector index
# --------------------------------------------------

index = VectorStoreIndex(nodes)

print("Vector index created successfully!")


# --------------------------------------------------
# 5. Create a vector retriever
# --------------------------------------------------

vector_retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,
)


# --------------------------------------------------
# 6. Create a BM25 keyword retriever
# --------------------------------------------------

bm25_retriever = BM25Retriever.from_defaults(
    nodes=nodes,
    similarity_top_k=3,
)


# --------------------------------------------------
# 7. Combine both retrievers
# --------------------------------------------------

fusion_retriever = QueryFusionRetriever(
    retrievers=[
        vector_retriever,
        bm25_retriever,
    ],
    similarity_top_k=3,
    num_queries=1,
    mode="reciprocal_rerank",
    use_async=False,
)

print("Fusion retriever created successfully!")


# --------------------------------------------------
# 8. Retrieve and fuse results
# --------------------------------------------------

while True:

    question = input(
        "\nAsk a question (or type 'exit'): "
    )

    if question.strip().lower() == "exit":
        break

    results = fusion_retriever.retrieve(question)

    print("\n" + "=" * 65)
    print("FUSION RETRIEVAL RESULTS")
    print("=" * 65)

    if not results:
        print("No results retrieved.")
        continue

    for rank, result in enumerate(results, start=1):

        print(f"\nRank: {rank}")
        print("-" * 55)

        print("Fusion Score:", result.score)
        print("Metadata:", result.node.metadata)

        print("\nContent:")
        print(result.node.get_content())

