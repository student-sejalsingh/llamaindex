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
        text="Deadlock is a situation where processes wait "
             "indefinitely for resources."
    ),
    Document(
        text="The four necessary conditions for deadlock are "
             "mutual exclusion, hold and wait, no preemption, "
             "and circular wait."
    ),
    Document(
        text="Deadlock can be handled using prevention, "
             "avoidance, detection, and recovery."
    ),
]


# --------------------------------------------------
# 3. Create index and retriever
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)

retriever = index.as_retriever(
    similarity_top_k=3
)

question = "What is deadlock and what are its conditions?"

nodes = retriever.retrieve(question)


# --------------------------------------------------
# 4. Try different response modes
# --------------------------------------------------

modes = [
    ResponseMode.COMPACT,
    ResponseMode.REFINE,
    ResponseMode.TREE_SUMMARIZE,
]


for mode in modes:

    print("\n" + "=" * 60)
    print(f"RESPONSE MODE: {mode}")
    print("=" * 60)

    response_synthesizer = get_response_synthesizer(
        response_mode=mode
    )

    response = response_synthesizer.synthesize(
        query=question,
        nodes=nodes,
    )

    print(response)