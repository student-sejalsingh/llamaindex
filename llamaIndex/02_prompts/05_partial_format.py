from llama_index.core import PromptTemplate
from llama_index.llms.ollama import Ollama

# Initialize LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)

# Original template
template = PromptTemplate(
"""
You are an expert {teacher_type}.

Teach the following topic.

Class: {class_name}

Topic: {topic}

Explain with simple examples.
"""
)

# Partially fill the teacher type
partial_template = template.partial_format(
    teacher_type="Computer Science Teacher"
)

# Fill the remaining variables
prompt = partial_template.format(
    class_name="B.Tech",
    topic="Binary Search"
)

print("Generated Prompt:\n")
print(prompt)

print("\n" + "=" * 60)

response = llm.complete(prompt)

print("\n🤖 AI Response:\n")
print(response.text)