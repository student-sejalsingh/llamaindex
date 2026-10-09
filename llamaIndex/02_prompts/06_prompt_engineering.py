from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Prompt Engineering Template
template = PromptTemplate(
"""
You are an experienced Computer Science professor.

Explain the topic: {topic}

Follow these rules:

1. Use simple language.
2. Explain step by step.
3. Give one real-world example.
4. Provide a Python example.
5. Keep the answer under 300 words.
"""
)

prompt = template.format(
    topic="Binary Search"
)

print("Generated Prompt:\n")
print(prompt)

print("\n" + "=" * 60)

response = llm.complete(prompt)

print("\n🤖 AI Response:\n")
print(response.text)