from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

# Initialize the Ollama LLM
llm = Ollama(
    model="qwen3:0.6b",      # Replace with your installed model
    request_timeout=120.0,
)

# Create a conversation
messages = [
    ChatMessage(
        role="system",
        content="You are a helpful AI assistant."
    ),
    ChatMessage(
        role="user",
        # content="What is LlamaIndex? Explain in simple words."
        # content="Explain binary search with an example."
        content="Write a Python function to check whether a number is prime."
        
    ),
]

# Send the conversation to the LLM
response = llm.chat(messages)

# Print the response
print("\n🤖 AI Response:\n")
print(response.message.content)
