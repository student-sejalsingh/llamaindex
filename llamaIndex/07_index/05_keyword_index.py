from llama_index.core import Document, KeywordTableIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings



# --------------------------------------------------
# 1. Create Documents
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)
documents = [
    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources held by other processes.
        The four necessary conditions are mutual exclusion,
        hold and wait, no preemption, and circular wait.
        """
    ),

    Document(
        text="""
        Binary search is an efficient searching algorithm.
        It works on sorted arrays and repeatedly divides
        the search space into two halves.
        """
    ),

    Document(
        text="""
        Database normalization reduces data redundancy.
        Important concepts include functional dependencies,
        candidate keys, and normal forms.
        """
    ),
]


# --------------------------------------------------
# 2. Create Keyword Index
# --------------------------------------------------

index = KeywordTableIndex.from_documents(
    documents
)


# --------------------------------------------------
# 3. Display Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("KEYWORD INDEX")
print("=" * 60)

print("\nIndex created successfully!")

print("\nIndex Type:")
print(type(index))