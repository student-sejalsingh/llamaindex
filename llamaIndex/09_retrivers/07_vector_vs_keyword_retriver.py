import re
from dataclasses import dataclass

from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# ==================================================
# 1. Configure LlamaIndex
# ==================================================

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# ==================================================
# 2. Create the same documents for both systems
# ==================================================

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

    Document(
        text="""
        Process scheduling determines which process gets
        access to the CPU. Common algorithms include FCFS,
        Shortest Job First, Round Robin, and Priority Scheduling.
        """,
        metadata={
            "subject": "Operating Systems",
            "topic": "Scheduling",
        },
    ),
]


# ==================================================
# 3. VECTOR RETRIEVER
# ==================================================

index = VectorStoreIndex.from_documents(documents)

vector_retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=3,
)


# ==================================================
# 4. BASIC KEYWORD RETRIEVER
# ==================================================

@dataclass
class KeywordResult:
    document: Document
    score: int


def tokenize(text: str) -> set[str]:
    """
    Convert text into lowercase word tokens.
    """
    return set(
        re.findall(r"\b[a-z0-9]+\b", text.lower())
    )


def keyword_retrieve(
    query: str,
    documents: list[Document],
    top_k: int = 3,
) -> list[KeywordResult]:

    query_terms = tokenize(query)

    results = []

    for document in documents:

        document_terms = tokenize(
            document.get_content()
        )

        matched_terms = query_terms & document_terms

        score = len(matched_terms)

        if score > 0:
            results.append(
                KeywordResult(
                    document=document,
                    score=score,
                )
            )

    results.sort(
        key=lambda result: result.score,
        reverse=True,
    )

    return results[:top_k]


# ==================================================
# 5. ASK USER
# ==================================================

question = input(
    "\nEnter your question: "
)


# ==================================================
# 6. VECTOR RETRIEVAL
# ==================================================

vector_results = vector_retriever.retrieve(
    question
)


# ==================================================
# 7. KEYWORD RETRIEVAL
# ==================================================

keyword_results = keyword_retrieve(
    query=question,
    documents=documents,
    top_k=3,
)


# ==================================================
# 8. DISPLAY VECTOR RESULTS
# ==================================================

print("\n")
print("=" * 70)
print("VECTOR / SEMANTIC RETRIEVAL")
print("=" * 70)

if not vector_results:

    print("No vector results found.")

else:

    for rank, result in enumerate(
        vector_results,
        start=1,
    ):

        print(f"\nRank: {rank}")
        print("-" * 60)

        print("Score:", result.score)

        print(
            "Metadata:",
            result.node.metadata
        )

        print(
            "Content:",
            result.node.get_content()
        )


# ==================================================
# 9. DISPLAY KEYWORD RESULTS
# ==================================================

print("\n")
print("=" * 70)
print("KEYWORD RETRIEVAL")
print("=" * 70)

if not keyword_results:

    print("No keyword matches found.")

else:

    for rank, result in enumerate(
        keyword_results,
        start=1,
    ):

        print(f"\nRank: {rank}")
        print("-" * 60)

        print(
            "Keyword Match Score:",
            result.score
        )

        print(
            "Metadata:",
            result.document.metadata
        )

        print(
            "Content:",
            result.document.get_content()
        )