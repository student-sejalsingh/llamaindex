
from typing import List

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.schema import NodeWithScore, QueryBundle
from llama_index.core.retrievers import BaseRetriever

from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Create documents for different subjects
# --------------------------------------------------

os_documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources.

        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """,
        metadata={"subject": "Operating Systems"},
    ),
    Document(
        text="""
        CPU scheduling determines which process gets CPU time.
        Common algorithms include FCFS, SJF, Round Robin,
        and Priority Scheduling.
        """,
        metadata={"subject": "Operating Systems"},
    ),
]

dbms_documents = [
    Document(
        text="""
        Database normalization reduces data redundancy
        and improves data organization.

        Common normal forms include 1NF, 2NF, 3NF and BCNF.
        """,
        metadata={"subject": "DBMS"},
    ),
    Document(
        text="""
        A primary key uniquely identifies each record
        in a database table. A foreign key represents
        a relationship with another table.
        """,
        metadata={"subject": "DBMS"},
    ),
]

network_documents = [
    Document(
        text="""
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """,
        metadata={"subject": "Computer Networks"},
    ),
    Document(
        text="""
        UDP is a connectionless transport layer protocol.
        It does not guarantee delivery or ordering of packets.
        """,
        metadata={"subject": "Computer Networks"},
    ),
]


# --------------------------------------------------
# 3. Create separate indexes
# --------------------------------------------------

os_index = VectorStoreIndex.from_documents(os_documents)
dbms_index = VectorStoreIndex.from_documents(dbms_documents)
network_index = VectorStoreIndex.from_documents(network_documents)


# --------------------------------------------------
# 4. Create separate retrievers
# --------------------------------------------------

os_retriever = os_index.as_retriever(
    similarity_top_k=2
)

dbms_retriever = dbms_index.as_retriever(
    similarity_top_k=2
)

network_retriever = network_index.as_retriever(
    similarity_top_k=2
)


# --------------------------------------------------
# 5. Define a custom Router Retriever
# --------------------------------------------------

class RouterRetriever(BaseRetriever):

    def __init__(
        self,
        os_retriever,
        dbms_retriever,
        network_retriever,
    ) -> None:

        self.os_retriever = os_retriever
        self.dbms_retriever = dbms_retriever
        self.network_retriever = network_retriever

        super().__init__()

    def _retrieve(
        self,
        query_bundle: QueryBundle,
    ) -> List[NodeWithScore]:

        query = query_bundle.query_str.lower()

        # Route based on simple keyword rules.
        if any(
            word in query
            for word in [
                "deadlock",
                "process",
                "scheduling",
                "cpu",
                "operating system",
            ]
        ):
            print("Selected retriever: Operating Systems")
            return self.os_retriever.retrieve(query_bundle)

        elif any(
            word in query
            for word in [
                "database",
                "normalization",
                "primary key",
                "foreign key",
                "dbms",
                "bcnf",
            ]
        ):
            print("Selected retriever: DBMS")
            return self.dbms_retriever.retrieve(query_bundle)

        elif any(
            word in query
            for word in [
                "tcp",
                "udp",
                "network",
                "protocol",
                "transport layer",
            ]
        ):
            print("Selected retriever: Computer Networks")
            return self.network_retriever.retrieve(query_bundle)

        # Avoid silently searching the wrong subject.
        print("No matching subject was identified.")
        return []


# --------------------------------------------------
# 6. Create the router
# --------------------------------------------------

router = RouterRetriever(
    os_retriever=os_retriever,
    dbms_retriever=dbms_retriever,
    network_retriever=network_retriever,
)


# --------------------------------------------------
# 7. Ask questions
# --------------------------------------------------

while True:

    question = input(
        "\nAsk a question (or type 'exit'): "
    )

    if question.strip().lower() == "exit":
        break

    results = router.retrieve(question)

    print("\n" + "=" * 60)
    print("ROUTER RETRIEVER RESULTS")
    print("=" * 60)

    if not results:
        print("No results returned.")
        continue

    for rank, result in enumerate(results, start=1):

        print(f"\nResult {rank}")
        print("-" * 50)

        print("Score:", result.score)
        print("Metadata:", result.node.metadata)
        print("Content:")
        print(result.node.get_content())
