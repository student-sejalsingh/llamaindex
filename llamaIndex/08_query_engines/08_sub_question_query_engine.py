from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)
from llama_index.core.tools import QueryEngineTool

from llama_index.core.query_engine import (
    SubQuestionQueryEngine,
)
from llama_index.core.question_gen import LLMQuestionGenerator

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
# 3. Operating Systems documents
# ==================================================

os_documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources. The four necessary conditions are
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
        """
    ),

    Document(
        text="""
        Process scheduling determines which process gets
        access to the CPU. Common scheduling algorithms
        include FCFS, SJF, Priority Scheduling, and Round Robin.
        """
    ),
]


# ==================================================
# 4. Computer Networks documents
# ==================================================

network_documents = [
    Document(
        text="""
        TCP is a connection-oriented transport protocol.
        It provides reliable and ordered delivery of data.
        It uses acknowledgements, sequence numbers, and
        retransmission to provide reliability.
        """
    ),

    Document(
        text="""
        UDP is a connectionless transport protocol.
        It does not guarantee delivery or ordering.
        Because it has less overhead, it is generally
        faster and is useful for applications such as
        streaming and online gaming.
        """
    ),
]


# ==================================================
# 5. Create indexes
# ==================================================

os_index = VectorStoreIndex.from_documents(
    os_documents
)

network_index = VectorStoreIndex.from_documents(
    network_documents
)

print("\nIndexes created!")


# ==================================================
# 6. Create query engines
# ==================================================

os_query_engine = os_index.as_query_engine()

network_query_engine = network_index.as_query_engine()


# ==================================================
# 7. Give names to the query engines
# ==================================================

query_engine_tools = [
    QueryEngineTool.from_defaults(
        query_engine=os_query_engine,
        name="operating_systems",
        description=(
            "Useful for questions about operating systems, "
            "processes, scheduling, and deadlock."
        ),
    ),
    QueryEngineTool.from_defaults(
        query_engine=network_query_engine,
        name="computer_networks",
        description=(
            "Useful for questions about computer networks, "
            "TCP, UDP, reliability, and network protocols."
        ),
    ),
]


# ==================================================
# 8. Create SubQuestionQueryEngine
# ==================================================

query_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=query_engine_tools,
    question_gen=LLMQuestionGenerator.from_defaults(
        llm=Settings.llm
    ),
    use_async=False,
)

print("SubQuestionQueryEngine created!")


# ==================================================
# 9. Ask a complex question
# ==================================================

question = input(
    "\nAsk a complex question: "
)


# ==================================================
# 10. Query
# ==================================================

response = query_engine.query(
    question
)


# ==================================================
# 11. Display final answer
# ==================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(response)