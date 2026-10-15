from llama_index.core import Document, KnowledgeGraphIndex
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure LLM
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

# --------------------------------------------------
# 2. Create Documents
# --------------------------------------------------

documents = [
    Document(
        text="""
        Python is a programming language.
        Python is widely used for machine learning.
        Machine learning is a branch of artificial intelligence.
        """
    ),

    Document(
        text="""
        LlamaIndex is a framework for building
        applications using large language models.
        LlamaIndex is commonly used for RAG applications.
        RAG combines retrieval with generation.
        """
    ),
]


# --------------------------------------------------
# 3. Create Knowledge Graph Index
# --------------------------------------------------

index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=5,
)


# --------------------------------------------------
# 4. Display Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("KNOWLEDGE GRAPH INDEX")
print("=" * 60)

print("\nIndex created successfully!")

print("\nIndex Type:")
print(type(index))