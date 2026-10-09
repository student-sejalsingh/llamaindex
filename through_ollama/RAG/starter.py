from llama_index.core import (
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import asyncio
import os

# Settings control global defaults
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(
    model="qwen3:4b",
    # is faster but less accurate, and can handle less context on the cpu if you have a gpu, you can use model="qwen3:4b" for better performance
    # model="qwen3:4b", is slower but more accurate, and can handle more context if you have a gpu, you can use model="qwen3:4b" for better performance
    request_timeout=360.0,
    # Manually set the context window to limit memory usage
    context_window=8000,
)

# Load the saved index when available; build it on the first run.
if os.path.exists("storage/index_store.json"):
    print("Loading persisted index...")
    # Load the index saved by starter.py
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    # Load the index from storage
    index = load_index_from_storage(
        # here we use the storage context to load the index from the persisted storage and we also specify the embedding model to use for the index
        # here we are using indexing that is normaally used for semantic search and retrieval of documents based on the query provided by the user
        # embedding model is huggingface embedding model that is used to convert the text into vector representation for semantic search
        storage_context,
        # 
        embed_model=Settings.embed_model,
    )
else:
    print("Building and saving index...")
    # Load documents from the "data" directory
    documents = SimpleDirectoryReader("data").load_data()
    # Create a vector store index from the loaded documents
    index = VectorStoreIndex.from_documents(documents)
    # Persist the index to disk for future use
    index.storage_context.persist("storage")

query_engine = index.as_query_engine(
    llm=Settings.llm,
    # Use the same LLM for querying
    streaming=True,  # Enable streaming responses
)


def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a * b


async def search_documents(query: str) -> str:
    """Useful for answering natural language questions about an personal essay written by Paul Graham."""
    response = await query_engine.aquery(query)
    return str(response)


# Create an enhanced workflow with both tools
agent = AgentWorkflow.from_tools_or_functions(
    [multiply, search_documents],
    llm=Settings.llm,
    system_prompt="""You are a helpful assistant that can perform calculations
    and search through documents to answer questions.""",
)


# Now we can ask questions about the documents or do calculations
async def main():
    response = await agent.run(
        "What did the author do in college? Also, what's 7 * 8?"
    )
    print(response)


# Run the agent
if __name__ == "__main__":
    asyncio.run(main())