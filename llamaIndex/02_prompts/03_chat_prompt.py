from llama_index.core.prompts import ChatPromptTemplate
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Create a chat prompt template
chat_template = ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role="system",
            content="You are a helpful Computer Science teacher."
        ),
        ChatMessage(
            role="user",
            content="Explain {topic} in simple words with an example."
        )
    ]
)

# Fill the template
messages = chat_template.format_messages(
    topic="Binary Search"
)

print("Generated Messages:\n")

for msg in messages:
    print(f"{msg.role}: {msg.content}")

print("\n" + "=" * 60)

# Send to LLM
response = llm.chat(messages)

print("\n🤖 AI Response:\n")
print(response.message.content)