from llama_index.core import (
    Document,
    KnowledgeGraphIndex,
    Settings,
)

from llama_index.core.query_engine import (
    KnowledgeGraphQueryEngine,
)

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


# ==================================================
# 1. Configure LLM
# ==================================================

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

# ==================================================
# 2. Create documents
# ==================================================

documents = [
    Document(
        text="""
        Python is a programming language.
        Python is widely used for machine learning.
        Machine learning is a branch of artificial intelligence.
        Artificial intelligence is a field of computer science.
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


# ==================================================
# 3. Create Knowledge Graph Index
# ==================================================

index = KnowledgeGraphIndex.from_documents(
    documents,
    max_triplets_per_chunk=5,
)

print("\nKnowledge Graph Index created!")


# ==================================================
# 4. Create Knowledge Graph Query Engine
# ==================================================

query_engine = index.as_query_engine(
    include_text=True,
)

print("Knowledge Graph Query Engine created!")


# ==================================================
# 5. Ask a question
# ==================================================

question = input(
    "\nAsk a question about the knowledge graph: "
)


# ==================================================
# 6. Query
# ==================================================

response = query_engine.query(
    question
)


# ==================================================
# 7. Display answer
# ==================================================

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)

print(response)