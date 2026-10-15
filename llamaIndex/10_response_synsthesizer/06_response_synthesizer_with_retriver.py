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
        text="A process is a program in execution. "
             "The operating system manages processes and "
             "allocates CPU resources to them."
    ),
    Document(
        text="CPU scheduling determines which ready process "
             "should be allocated the CPU next."
    ),
    Document(
        text="Common CPU scheduling algorithms include FCFS, "
             "SJF, Round Robin, and Priority Scheduling."
    ),
    Document(
        text="Round Robin scheduling assigns each process "
             "a fixed time quantum and provides fair CPU sharing."
    ),
]


# --------------------------------------------------
# 3. Create Vector Index
# --------------------------------------------------

index = VectorStoreIndex.from_documents(documents)


# --------------------------------------------------
# 4. Create Retriever
# --------------------------------------------------

retriever = index.as_retriever(
    similarity_top_k=3
)


# --------------------------------------------------
# 5. Create Response Synthesizer
# --------------------------------------------------

response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT
)


# --------------------------------------------------
# 6. Ask question
# --------------------------------------------------

question = "What is CPU scheduling and what are its algorithms?"


# --------------------------------------------------
# 7. Retrieve relevant nodes
# --------------------------------------------------

nodes = retriever.retrieve(question)

print("\n========== RETRIEVED NODES ==========")

for i, node in enumerate(nodes, start=1):
    print(f"\nNode {i}")
    print(node.node.get_content())


# --------------------------------------------------
# 8. Synthesize final answer
# --------------------------------------------------

response = response_synthesizer.synthesize(
    query=question,
    nodes=nodes,
)


# --------------------------------------------------
# 9. Display final answer
# --------------------------------------------------

print("\n========== FINAL ANSWER ==========")
print(response)