from typing import Any, Sequence

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.schema import NodeWithScore
from llama_index.core.llms import ChatMessage
from llama_index.core.base.llms.types import ChatResponse
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
# 5. Custom Response Synthesizer
# --------------------------------------------------

class MyResponseSynthesizer(BaseSynthesizer):

    def _get_prompts(self):
        return {}

    def _update_prompts(self, prompts):
        pass

    def _get_prompt_modules(self):
        return {}

    def synthesize(
        self,
        query,
        nodes: Sequence[NodeWithScore],
        additional_source_nodes=None,
        **kwargs: Any,
    ):

        # Combine retrieved nodes
        context = "\n\n".join(
            node.node.get_content()
            for node in nodes
        )

        # Create our own prompt
        prompt = f"""
You are a Computer Science teacher.

Answer the question using only the
provided context.

Explain the answer in simple language.

Context:
{context}

Question:
{query}

Answer:
"""

        # Ask the LLM
        response = Settings.llm.complete(prompt)

        return response


# --------------------------------------------------
# 6. Create custom synthesizer
# --------------------------------------------------

response_synthesizer = MyResponseSynthesizer()


# --------------------------------------------------
# 7. Retrieve nodes
# --------------------------------------------------

question = "What is CPU scheduling?"

nodes = retriever.retrieve(question)


# --------------------------------------------------
# 8. Generate response
# --------------------------------------------------

response = response_synthesizer.synthesize(
    query=question,
    nodes=nodes,
)


# --------------------------------------------------
# 9. Display response
# --------------------------------------------------

print("\n========== CUSTOM RESPONSE ==========")
print(response)