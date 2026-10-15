from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.prompts import PromptTemplate
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
        text="Round Robin assigns each process a fixed time "
             "quantum and is commonly used in time-sharing systems."
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
# 5. Retrieve relevant nodes
# --------------------------------------------------

question = "Explain CPU scheduling algorithms."

nodes = retriever.retrieve(question)


# --------------------------------------------------
# 6. Create custom prompt
# --------------------------------------------------

custom_prompt = PromptTemplate(
    """
You are a Computer Science teacher.

Use ONLY the information provided in the context.

Explain the answer in simple language.

Give the answer in this format:

1. Definition
2. Important algorithms
3. Short explanation of each algorithm
4. Simple conclusion

Context:
{context_str}

Question:
{query_str}

Answer:
"""
)


# --------------------------------------------------
# 7. Create Response Synthesizer
# --------------------------------------------------

response_synthesizer = get_response_synthesizer(
    response_mode=ResponseMode.COMPACT,
    text_qa_template=custom_prompt,
)


# --------------------------------------------------
# 8. Generate answer
# --------------------------------------------------

response = response_synthesizer.synthesize(
    query=question,
    nodes=nodes,
)


# --------------------------------------------------
# 9. Display answer
# --------------------------------------------------

print("\n========== CUSTOM PROMPT RESPONSE ==========")
print(response)