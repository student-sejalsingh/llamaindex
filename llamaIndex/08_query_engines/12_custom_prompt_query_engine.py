
from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
    PromptTemplate,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# 1. Configure the local embedding model
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

# 2. Configure the local LLM
Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# 3. Prepare some study notes
documents = [
    Document(
        text="""
        Deadlock is a situation in an operating system
        where processes wait indefinitely for resources.

        The four necessary conditions for deadlock are
        mutual exclusion, hold and wait, no preemption,
        and circular wait.
        """
    ),
    Document(
        text="""
        Binary search is an efficient searching algorithm
        that works on sorted arrays.

        It repeatedly divides the search space into
        two halves. Its time complexity is O(log n).
        """
    ),
    Document(
        text="""
        TCP is a connection-oriented transport layer protocol.
        It provides reliable and ordered delivery of data.
        """
    ),
]


# 4. Create the vector index
index = VectorStoreIndex.from_documents(documents)


# 5. Define our custom prompt
custom_prompt = PromptTemplate(
    """
    You are a friendly Computer Science teacher.

    Answer the student's question using ONLY the
    information provided in the context below.

    Follow these rules:
    1. Explain in simple English.
    2. Use bullet points when helpful.
    3. Give an example if the context supports one.
    4. If the answer is not available in the context,
       clearly say that the notes do not contain the answer.
    5. Do not invent facts.

    Context:
    ---------------------
    {context_str}
    ---------------------

    Student's question: {query_str}

    Answer:
    """
)


# 6. Create the Query Engine with our custom prompt
query_engine = index.as_query_engine(
    similarity_top_k=2,
    text_qa_template=custom_prompt,
)


# 7. Ask questions
while True:
    question = input(
        "\nAsk a Computer Science question (or type 'exit'): "
    )

    if question.strip().lower() == "exit":
        break

    response = query_engine.query(question)

    print("\nAnswer:")
    print(response)

    print("\nRetrieved sources:")

    for i, source in enumerate(response.source_nodes, start=1):
        print(f"\nSource {i}:")
        print(source.node.get_content())

        print("Score:", source.score)

