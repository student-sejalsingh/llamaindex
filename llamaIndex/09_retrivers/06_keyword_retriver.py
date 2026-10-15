
import re
from dataclasses import dataclass


# --------------------------------------------------
# 1. Define our documents
# --------------------------------------------------

documents = [
    {
        "id": 1,
        "text": """
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.
        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """,
        "metadata": {
            "subject": "Operating Systems",
            "topic": "Deadlock",
        },
    },
    {
        "id": 2,
        "text": """
        Binary search is an efficient searching algorithm
        that works on sorted arrays. It repeatedly divides
        the search space into two halves.
        """,
        "metadata": {
            "subject": "DSA",
            "topic": "Binary Search",
        },
    },
    {
        "id": 3,
        "text": """
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """,
        "metadata": {
            "subject": "Computer Networks",
            "topic": "TCP",
        },
    },
    {
        "id": 4,
        "text": """
        Process scheduling determines which process gets
        access to the CPU. Common algorithms include FCFS,
        Shortest Job First, Round Robin, and Priority Scheduling.
        """,
        "metadata": {
            "subject": "Operating Systems",
            "topic": "Scheduling",
        },
    },
]


# --------------------------------------------------
# 2. Tokenize text into words
# --------------------------------------------------

def tokenize(text: str) -> list[str]:
    """
    Convert text to lowercase words.
    """
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


# --------------------------------------------------
# 3. Implement a basic keyword retriever
# --------------------------------------------------

@dataclass
class RetrievalResult:
    document: dict
    score: int


class KeywordRetriever:

    def __init__(self, documents: list[dict]):
        self.documents = documents

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[RetrievalResult]:

        query_terms = set(tokenize(query))

        if not query_terms:
            return []

        results = []

        for document in self.documents:

            document_terms = set(
                tokenize(document["text"])
            )

            # Count query terms present in the document.
            matched_terms = query_terms & document_terms
            score = len(matched_terms)

            if score > 0:
                results.append(
                    RetrievalResult(
                        document=document,
                        score=score,
                    )
                )

        # Highest keyword-match count first.
        results.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return results[:top_k]


# --------------------------------------------------
# 4. Create the retriever
# --------------------------------------------------

retriever = KeywordRetriever(documents)


# --------------------------------------------------
# 5. Search interactively
# --------------------------------------------------

while True:

    query = input(
        "\nEnter keywords or a question (or 'exit'): "
    )

    if query.strip().lower() == "exit":
        break

    results = retriever.retrieve(
        query=query,
        top_k=3,
    )

    print("\n" + "=" * 60)
    print("KEYWORD RETRIEVAL RESULTS")
    print("=" * 60)

    if not results:
        print("No matching documents found.")
        continue

    for rank, result in enumerate(results, start=1):

        document = result.document

        print(f"\nRank: {rank}")
        print("Keyword Match Score:", result.score)
        print("Metadata:", document["metadata"])
        print("\nContent:")
        print(document["text"].strip())
