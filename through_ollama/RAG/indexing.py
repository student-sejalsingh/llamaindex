# Load the index saved by starter.py
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
Settings.llm = Ollama(
    model="qwen3:4b",
    request_timeout=360.0,
    context_window=8000,
)

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(
    storage_context,
    embed_model=Settings.embed_model,
)
query_engine = index.as_query_engine(
    llm=Settings.llm,
    streaming=True,  # Enable streaming responses
)