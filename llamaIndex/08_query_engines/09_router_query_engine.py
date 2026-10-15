from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


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
# 3. Operating Systems Documents
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
        include FCFS, SJF, Priority Scheduling,
        and Round Robin.
        """
    ),
]


# ==================================================
# 4. DBMS Documents
# ==================================================

dbms_documents = [
    Document(
        text="""
        Database normalization is the process of organizing
        data to reduce redundancy and improve data integrity.
        Normal forms include 1NF, 2NF, 3NF, and BCNF.
        """
    ),

    Document(
        text="""
        A primary key uniquely identifies each record
        in a relational database table.
        """
    ),
]


# ==================================================
# 5. Computer Networks Documents
# ==================================================

network_documents = [
    Document(
        text="""
        TCP is a connection-oriented transport protocol.
        It provides reliable and ordered delivery of data.
        """
    ),

    Document(
        text="""
        UDP is a connectionless transport protocol.
        It does not guarantee reliable delivery but has
        lower overhead than TCP.
        """
    ),
]


# ==================================================
# 6. Create Indexes
# ==================================================

os_index = VectorStoreIndex.from_documents(
    os_documents
)

dbms_index = VectorStoreIndex.from_documents(
    dbms_documents
)

network_index = VectorStoreIndex.from_documents(
    network_documents
)

print("\nIndexes created!")


# ==================================================
# 7. Create Query Engines
# ==================================================

os_query_engine = os_index.as_query_engine()

dbms_query_engine = dbms_index.as_query_engine()

network_query_engine = network_index.as_query_engine()


# ==================================================
# 8. Convert Query Engines into Tools
# ==================================================

os_tool = QueryEngineTool.from_defaults(
    query_engine=os_query_engine,
    description=(
        "Use this tool for questions about "
        "Operating Systems, processes, scheduling, "
        "deadlock, and memory management."
    ),
)


dbms_tool = QueryEngineTool.from_defaults(
    query_engine=dbms_query_engine,
    description=(
        "Use this tool for questions about "
        "databases, normalization, keys, tables, "
        "SQL, and DBMS concepts."
    ),
)


network_tool = QueryEngineTool.from_defaults(
    query_engine=network_query_engine,
    description=(
        "Use this tool for questions about "
        "Computer Networks, TCP, UDP, protocols, "
        "and network communication."
    ),
)


# ==================================================
# 9. Create Router Query Engine
# ==================================================

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        os_tool,
        dbms_tool,
        network_tool,
    ],
)

print("RouterQueryEngine created!")


# ==================================================
# 10. Ask Question
# ==================================================

question = input(
    "\nAsk a question: "
)


# ==================================================
# 11. Query Router
# ==================================================

response = query_engine.query(
    question
)


# ==================================================
# 12. Display Answer
# ==================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(response)