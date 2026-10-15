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
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.
        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm.
        It works on sorted arrays by repeatedly dividing
        the search space into two halves.
        """
    ),

    Document(
        text="""
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """
    ),
]


# --------------------------------------------------
# 4. Create Vector Store Index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)


# --------------------------------------------------
# 5. Create Retriever
# --------------------------------------------------

retriever = index.as_retriever(
    similarity_top_k=2
)


# --------------------------------------------------
# 6. Ask a question
# --------------------------------------------------

question = input("\nAsk a question: ")


# --------------------------------------------------
# 7. Retrieve relevant nodes
# --------------------------------------------------

nodes = retriever.retrieve(question)


# --------------------------------------------------
# 8. Display retrieved nodes
# --------------------------------------------------

print("\n" + "=" * 60)
print("RETRIEVED NODES")
print("=" * 60)

for i, node in enumerate(nodes, start=1):

    print(f"\nNode {i}")
    print("-" * 60)

    print("Score:", node.score)

    print("Content:")
    print(node.node.get_content())