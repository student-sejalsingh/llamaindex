from llama_index.core import Document, TreeIndex
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
        Operating Systems manage the hardware and software
        resources of a computer. They manage processes,
        memory, storage, and input/output devices.
        """
    ),

    Document(
        text="""
        Process management is responsible for creating,
        scheduling, and terminating processes. The operating
        system also manages communication between processes.
        """
    ),

    Document(
        text="""
        Memory management controls the allocation and
        deallocation of memory. It keeps track of which
        parts of memory are being used.
        """
    ),

    Document(
        text="""
        Deadlock occurs when processes wait indefinitely
        for resources held by other processes. The four
        necessary conditions are mutual exclusion, hold
        and wait, no preemption, and circular wait.
        """
    ),
]


# --------------------------------------------------
# 3. Create Tree Index
# --------------------------------------------------

index = TreeIndex.from_documents(
    documents
)


# --------------------------------------------------
# 4. Display Information
# --------------------------------------------------

print("\n" + "=" * 60)
print("TREE INDEX")
print("=" * 60)

print("\nIndex created successfully!")

print("\nIndex Type:")
print(type(index))