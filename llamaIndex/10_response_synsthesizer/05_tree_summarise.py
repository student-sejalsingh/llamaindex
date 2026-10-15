from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.response_synthesizers import (
    get_response_synthesizer,
    ResponseMode,
)
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
        text="Deadlock occurs when processes wait indefinitely "
             "for resources held by other processes."
    ),
    Document(
        text="The four necessary conditions are mutual exclusion, "
             "hold and wait, no preemption, and circular wait."
    ),
    Document(
        text="Deadlock prevention attempts to ensure that at least "
             "one necessary condition cannot occur."
    ),
    Document(
        text="Deadlock avoidance makes decisions based on whether "
             "granting a resource request can keep the system safe."
    ),
    Document(
        text="Deadlock detection allows the system to identify "
             "deadlocks after they occur."
    ),
]


# --------------------------------------------------
# 3. Create index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)


# --------------------------------------------------
# 4. Retrieve relevant nodes
# --------------------------------------------------

retriever = index.as_retriever(
    similarity_top_k=5
)

question = "Explain deadlock and its handling techniques."

nodes = retriever.retrieve(question)


# --------------------------------------------------
# 5. Create TREE_SUMMARIZE synthesizer
# --------------------------------------------------

response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.TREE_SUMMARIZE
)


# --------------------------------------------------
# 6. Generate response
# --------------------------------------------------

response = response_synthesizer.synthesize(
    query=question,
    nodes=nodes,
)


# --------------------------------------------------
# 7. Display final response
# --------------------------------------------------

print("\n========== TREE SUMMARIZE RESPONSE ==========")
print(response)