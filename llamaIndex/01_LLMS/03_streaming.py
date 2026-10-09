from llama_index.llms.ollama import Ollama

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Prompt
prompt = "Explain Machine Learning in simple words."

# Stream the response
response = llm.stream_complete(prompt)

print("\n🤖 AI Response:\n")

# Print each chunk as it arrives
for chunk in response:
    print(chunk.delta, end="", flush=True)

print()