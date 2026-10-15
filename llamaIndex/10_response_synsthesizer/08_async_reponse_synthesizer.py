import asyncio

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
        text="TCP is a connection-oriented transport layer protocol."
    ),
    Document(
        text="TCP provides reliable delivery using acknowledgements "
             "and retransmissions."
    ),
    Document(
        text="TCP uses flow control to prevent receiver overload."
    ),
    Document(
        text="TCP uses congestion control to manage network congestion."
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
# 6. Async main function
# --------------------------------------------------

async def main():

    question = "What are the important features of TCP?"

    # Async retrieval
    nodes = await retriever.aretrieve(question)

    print("\nRetrieved nodes:", len(nodes))

    # Async response synthesis
    response = await response_synthesizer.asynthesize(
        query=question,
        nodes=nodes,
    )

    print("\n========== ASYNC RESPONSE ==========")
    print(response)


# --------------------------------------------------
# 7. Run async program
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())