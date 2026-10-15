from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

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
        Deadlock occurs when processes wait indefinitely
        for resources. Four necessary conditions are
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
        """
    ),

    Document(
        text="""
        Binary search works on sorted arrays.
        It repeatedly divides the search space into
        two halves.
        """
    ),

    Document(
        text="""
        TCP is a connection-oriented protocol.
        It provides reliable and ordered delivery.
        """
    ),
]


# --------------------------------------------------
# 4. Create VectorStoreIndex
# --------------------------------------------------

index = VectorStoreIndex.from_documents(
    documents
)

print("\n1. VectorStoreIndex created")
print("Index type:", type(index))


# --------------------------------------------------
# 5. Create Query Engine from the index
# --------------------------------------------------

query_engine = index.as_query_engine(
    similarity_top_k=2
)

print("\n2. Query Engine created")
print("Query Engine type:", type(query_engine))


# --------------------------------------------------
# 6. Ask a question
# --------------------------------------------------

question = input("\nAsk a question: ")

response = query_engine.query(question)


# --------------------------------------------------
# 7. Display answer
# --------------------------------------------------

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(response)


# --------------------------------------------------
# 8. Display retrieved source nodes
# --------------------------------------------------

print("\nRetrieved Nodes:")

for i, node in enumerate(response.source_nodes, start=1):

    print("\n" + "=" * 60)
    print(f"Node {i}")
    print("=" * 60)

    print("Score:", node.score)
    print("Text:")
    print(node.text)