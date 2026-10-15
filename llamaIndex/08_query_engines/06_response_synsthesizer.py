from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
    get_response_synthesizer,
)

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

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


# --------------------------------------------------
# 4. Create VectorStoreIndex
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("\nVectorStoreIndex created!")


# --------------------------------------------------
# 5. Create Retriever
# --------------------------------------------------

retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=2,
)

print("Retriever created!")


# --------------------------------------------------
# 6. Create Response Synthesizer
# --------------------------------------------------

response_synthesizer = get_response_synthesizer()

print("Response Synthesizer created!")


# --------------------------------------------------
# 7. Create Query Engine
# --------------------------------------------------

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)

print("Query Engine created!")


# --------------------------------------------------
# 8. Ask question
# --------------------------------------------------

question = input("\nAsk a question: ")

response = query_engine.query(question)


# --------------------------------------------------
# 9. Display final answer
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(response)


# --------------------------------------------------
# 10. Display source nodes
# --------------------------------------------------

print("\n" + "=" * 60)
print("SOURCE NODES")
print("=" * 60)

for i, source in enumerate(response.source_nodes, start=1):

    print(f"\n--- Node {i} ---")
    print("Score:", source.score)
    print("Text:")
    print(source.node.get_content())