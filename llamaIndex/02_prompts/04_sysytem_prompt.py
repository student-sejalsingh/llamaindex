from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Conversation
messages = [
    ChatMessage(
        role="system",
        content=(
            "You are an experienced Computer Science professor. "
            "Explain concepts in simple language with real-life examples."
        ),
    ),
    ChatMessage(
        role="user",
        content="Explain Binary Search."
    ),
]

response = llm.chat(messages)

print("\n🤖 AI Response:\n")
print(response.message.content)