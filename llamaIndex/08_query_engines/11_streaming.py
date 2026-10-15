from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# ==================================================
# 1. Configure embedding model
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
# 3. Create documents
# ==================================================

documents = [
    Document(
        text="""
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.
        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays. It repeatedly divides
        the search space into two halves.
        """
    ),

    Document(
        text="""
        TCP is a connection-oriented transport protocol.
        It provides reliable and ordered delivery of data.
        """
    ),
]


# ==================================================
# 4. Create VectorStoreIndex
# ==================================================

index = VectorStoreIndex.from_documents(
    documents
)

print("\nIndex created!")


# ==================================================
# 5. Create streaming Query Engine
# ==================================================

query_engine = index.as_query_engine(
    streaming=True,
    similarity_top_k=2,
)

print("Streaming Query Engine created!")


# ==================================================
# 6. Ask question
# ==================================================

question = input(
    "\nAsk a question: "
)


# ==================================================
# 7. Query
# ==================================================

response = query_engine.query(
    question
)


# ==================================================
# 8. Stream the response
# ==================================================

print("\nAnswer:\n")

response.print_response_stream()