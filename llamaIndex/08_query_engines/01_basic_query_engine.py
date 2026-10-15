from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# --------------------------------------------------
# 1. Configure the embedding model
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)


# --------------------------------------------------
# 2. Configure the LLM
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0
)


# --------------------------------------------------
# 3. Create some documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.
        There are four necessary conditions for deadlock:
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
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
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """
    ),
]


# --------------------------------------------------
# 4. Create the index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

print("\nIndex created successfully!")


# --------------------------------------------------
# 5. Convert the index into a Query Engine
# --------------------------------------------------

query_engine = index.as_query_engine()

print("Query Engine created successfully!")


# --------------------------------------------------
# 6. Ask a question
# --------------------------------------------------

question = input("\nAsk a question: ")

response = query_engine.query(question)


# --------------------------------------------------
# 7. Display the answer
# --------------------------------------------------

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(response)