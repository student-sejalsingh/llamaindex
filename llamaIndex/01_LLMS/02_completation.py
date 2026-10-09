from llama_index.llms.ollama import Ollama

# Initialize the Ollama LLM
llm = Ollama(
    model="qwen3:0.6b",      # Change to your installed model if needed
    request_timeout=120.0,
)

# Prompt
# prompt = """
# Explain Binary Search in simple words.
# Also provide a Python example.
# """
# prompt = "Write a Python function to check if a number is prime."
user_input = input("Enter your prompt: ")
prompt = user_input
# Generate completion
response = llm.complete(prompt)

# Print the response
print("\n🤖 AI Response:\n")
print(response.text)