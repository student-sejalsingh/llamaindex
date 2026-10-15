from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.response_synthesizers import get_response_synthesizer
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
    request_timeout=120.0
)


# --------------------------------------------------
# 2. Create documents
# --------------------------------------------------

documents = [
    Document(
        text="Deadlock is a situation where processes wait indefinitely "
             "for resources held by each other."
    ),
    Document(
        text="The four necessary conditions for deadlock are mutual "
             "exclusion, hold and wait, no preemption, and circular wait."
    ),
    Document(
        text="Deadlock can be handled using prevention, avoidance, "
             "detection, and recovery techniques."
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
    similarity_top_k=2
)

question = "What are the conditions for deadlock?"

nodes = retriever.retrieve(question)


# --------------------------------------------------
# 5. Create Response Synthesizer
# --------------------------------------------------

response_synthesizer = get_response_synthesizer()


# --------------------------------------------------
# 6. Generate response
# --------------------------------------------------

response = response_synthesizer.synthesize(
    query=question,
    nodes=nodes
)


# --------------------------------------------------
# 7. Print final answer
# --------------------------------------------------

print("\n========== FINAL ANSWER ==========")
print(response)