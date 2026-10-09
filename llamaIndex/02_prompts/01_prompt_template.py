from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Create a reusable prompt template
template = PromptTemplate(
    """
You are a helpful AI tutor.

Explain the following topic in simple language.

Topic: {topic}
"""
)

# Fill the template with a value
prompt = template.format(
    topic="Binary Search"
)

print("Generated Prompt:\n")
print(prompt)

print("\n" + "=" * 50)

# Send prompt to LLM
response = llm.complete(prompt)

print("\n🤖 AI Response:\n")
print(response.text)