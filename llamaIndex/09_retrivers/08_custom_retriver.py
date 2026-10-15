
from typing import List

from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.retrievers import (
    BaseRetriever,
    VectorIndexRetriever,
)

from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure the embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Create sample documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources. The four necessary conditions are
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
        """,
        metadata={"subject": "Operating Systems"},
    ),
    Document(
        text="""
        Binary search is an efficient algorithm that searches
        sorted arrays by repeatedly dividing the search space
        into two halves.
        """,
        metadata={"subject": "DSA"},
    ),
    Document(
        text="""
        TCP is a connection-oriented transport protocol
        that provides reliable and ordered delivery of data.
        """,
        metadata={"subject": "Computer Networks"},
    ),
]


# --------------------------------------------------
# 3. Create the vector index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("Vector index created successfully!")


# --------------------------------------------------
# 4. Define our custom retriever
# --------------------------------------------------

class CustomRetriever(BaseRetriever):

    def __init__(
        self,
        vector_retriever: VectorIndexRetriever,
        min_score: float = 0.0,
    ) -> None:

        self._vector_retriever = vector_retriever
        self._min_score = min_score

        super().__init__()

    def _retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:

        # Use the existing vector retriever
        nodes = self._vector_retriever.retrieve(
            query_bundle
        )

        # Keep only results that pass our score rule
        filtered_nodes = [
            node
            for node in nodes
            if node.score is not None
            and node.score >= self._min_score
        ]

        return filtered_nodes


# --------------------------------------------------
# 5. Create the underlying vector retriever
# --------------------------------------------------

vector_retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,
)


# --------------------------------------------------
# 6. Wrap it with our custom retriever
# --------------------------------------------------

custom_retriever = CustomRetriever(
    vector_retriever=vector_retriever,
    min_score=0.0,
)


# --------------------------------------------------
# 7. Retrieve information
# --------------------------------------------------

while True:

    question = input(
        "\nAsk a question (or type 'exit'): "
    )

    if question.strip().lower() == "exit":
        break

    results = custom_retriever.retrieve(question)

    print("\n" + "=" * 60)
    print("CUSTOM RETRIEVER RESULTS")
    print("=" * 60)

    if not results:
        print("No nodes passed the filtering rule.")
        continue

    for rank, result in enumerate(results, start=1):

        print(f"\nNode {rank}")
        print("-" * 60)

        print("Score:", result.score)
        print("Metadata:", result.node.metadata)
        print("Content:")
        print(result.node.get_content())
