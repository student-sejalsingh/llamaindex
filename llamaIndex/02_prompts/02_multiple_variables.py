from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Create a prompt template with multiple variables
template = PromptTemplate(
"""
You are an expert teacher.

Generate notes for the following:

Subject: {subject}
Topic: {topic}
Difficulty: {difficulty}

Explain in simple language and provide examples.
"""
)

# Fill the template
prompt = template.format(
    subject="Computer Science",
    topic="Binary Search",
    difficulty="Beginner"
)

print("Generated Prompt:\n")
print(prompt)

print("\n" + "=" * 60)

# Send to LLM
response = llm.complete(prompt)

print("\n🤖 AI Response:\n")
print(response.text)