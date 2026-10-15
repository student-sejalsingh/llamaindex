from typing import List

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.retrievers import BaseRetriever, VectorIndexRetriever
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Create documents
# --------------------------------------------------

documents = [
    Document(
        text="Deadlock occurs when processes wait indefinitely for resources.",
        metadata={"subject": "OS"},
    ),
    Document(
        text="CPU scheduling determines which process gets the CPU next.",
        metadata={"subject": "OS"},
    ),
    Document(
        text="Normalization reduces redundancy in relational databases.",
        metadata={"subject": "DBMS"},
    ),
    Document(
        text="A primary key uniquely identifies a record in a table.",
        metadata={"subject": "DBMS"},
    ),
    Document(
        text="TCP provides reliable and connection-oriented communication.",
        metadata={"subject": "CN"},
    ),
    Document(
        text="UDP is a connectionless transport layer protocol.",
        metadata={"subject": "CN"},
    ),
]


# --------------------------------------------------
# 3. Create Vector Index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)


# --------------------------------------------------
# 4. Create base vector retriever
# --------------------------------------------------

vector_retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=5,
)


# --------------------------------------------------
# 5. Create Retriever Pipeline
# --------------------------------------------------

class RetrieverPipeline(BaseRetriever):

    def __init__(
        self,
        retriever: VectorIndexRetriever,
        top_k: int = 3,
    ) -> None:

        self.retriever = retriever
        self.top_k = top_k

        super().__init__()


    def _retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:

        # Step 1: Retrieve candidates
        results = self.retriever.retrieve(query_bundle)

        print("\nStep 1: Retrieved candidates")
        print(f"Candidates found: {len(results)}")


        # Step 2: Remove duplicate nodes
        unique_results = []
        seen = set()

        for result in results:

            node_id = result.node.node_id

            if node_id not in seen:
                seen.add(node_id)
                unique_results.append(result)


        print(
            f"Step 2: After duplicate removal: "
            f"{len(unique_results)}"
        )


        # Step 3: Keep only top-k results
        final_results = unique_results[:self.top_k]

        print(
            f"Step 3: Final results: "
            f"{len(final_results)}"
        )

        return final_results


# --------------------------------------------------
# 6. Create pipeline
# --------------------------------------------------

pipeline = RetrieverPipeline(
    retriever=vector_retriever,
    top_k=3,
)


# --------------------------------------------------
# 7. Query
# --------------------------------------------------

question = "How does CPU scheduling work?"

results = pipeline.retrieve(question)


# --------------------------------------------------
# 8. Display results
# --------------------------------------------------

print("\n========== FINAL RESULTS ==========")

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print(f"Score: {result.score}")
    print(f"Subject: {result.node.metadata.get('subject')}")
    print(f"Text: {result.node.get_content()}")