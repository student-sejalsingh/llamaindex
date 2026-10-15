import chromadb

from llama_index.core import (
    Document,
    VectorStoreIndex,
    StorageContext,
    Settings,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from llama_index.vector_stores.chroma import ChromaVectorStore


# ==================================================
# 1. Configure Embedding Model
# ==================================================

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# ==================================================
# 2. Configure LLM
# ==================================================

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# ==================================================
# 3. Create Documents
# ==================================================

documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources. The four necessary conditions are
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
        Binary search is an efficient searching algorithm
        that works on sorted arrays. It repeatedly divides
        the search space into two halves.
        """,
        metadata={
            "subject": "DSA",
            "topic": "Searching",
        },
    ),

    Document(
        text="""
        TCP is a connection-oriented transport protocol.
        It provides reliable and ordered delivery of data.
        """,
        metadata={
            "subject": "Computer Networks",
            "topic": "TCP",
        },
    ),
]


# ==================================================
# 4. Create Persistent Chroma Client
# ==================================================

chroma_client = chromadb.PersistentClient(
    path="./chroma_data"
)

print("\nChroma client created!")


# ==================================================
# 5. Create / Get Chroma Collection
# ==================================================

chroma_collection = chroma_client.get_or_create_collection(
    name="query_engine_demo"
)

print("Chroma collection ready!")


# ==================================================
# 6. Connect Chroma with LlamaIndex
# ==================================================

vector_store = ChromaVectorStore(
    chroma_collection=chroma_collection
)


storage_context = StorageContext.from_defaults(
    vector_store=vector_store
)

print("Chroma connected to LlamaIndex!")


# ==================================================
# 7. Create VectorStoreIndex
# ==================================================

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

print("VectorStoreIndex created!")


# ==================================================
# 8. Create Query Engine
# ==================================================

query_engine = index.as_query_engine(
    similarity_top_k=2
)

print("Query Engine created!")


# ==================================================
# 9. Ask Questions
# ==================================================

while True:

    question = input(
        "\nAsk a question "
        "(type 'exit' to stop): "
    )

    if question.strip().lower() == "exit":
        break

    try:

        response = query_engine.query(question)

        print("\n" + "=" * 60)
        print("ANSWER")
        print("=" * 60)

        print(response)

        print("\n" + "=" * 60)
        print("SOURCE NODES")
        print("=" * 60)

        for i, source in enumerate(
            response.source_nodes,
            start=1
        ):

            print(f"\n--- Node {i} ---")
            print("Score:", source.score)

            print("Subject:",
                  source.node.metadata.get("subject"))

            print("Topic:",
                  source.node.metadata.get("topic"))

            print("Text:")
            print(source.node.get_content())

    except Exception as error:

        print("\nError:")
        print(error)