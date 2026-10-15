from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.response_synthesizers import (
    get_response_synthesizer,
    ResponseMode,
)
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# --------------------------------------------------
# 1. Configure models
# --------------------------------------------------

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# --------------------------------------------------
# 2. Create documents
# --------------------------------------------------

documents = [
    Document(
        text="CPU scheduling determines which ready process "
             "should receive the CPU next."
    ),
    Document(
        text="FCFS scheduling executes processes in the order "
             "in which they arrive."
    ),
    Document(
        text="SJF scheduling selects the process with the "
             "shortest expected CPU burst."
    ),
    Document(
        text="Round Robin gives each process a fixed time quantum "
             "and is commonly used in time-sharing systems."
    ),
]


# --------------------------------------------------
# 3. Create index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)


# --------------------------------------------------
# 4. Create retriever
# --------------------------------------------------

retriever = index.as_retriever(
    similarity_top_k=3
)


# --------------------------------------------------
# 5. Create response synthesizer
# --------------------------------------------------

response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT
)


# --------------------------------------------------
# 6. Combine retriever + synthesizer
# --------------------------------------------------

query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
)


# --------------------------------------------------
# 7. Ask question
# --------------------------------------------------

question = "Explain CPU scheduling algorithms."

response = query_engine.query(question)


# --------------------------------------------------
# 8. Display answer
# --------------------------------------------------

print("\n========== FINAL ANSWER ==========")
print(response)