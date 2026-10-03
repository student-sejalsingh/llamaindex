from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import FunctionAgent

agent = FunctionAgent(
    # tools=[multiply],
    llm=Ollama(
        model="qwen3:4b",
        request_timeout=360.0,
        # Manually set the context window to limit memory usage
        context_window=8000,
    ),
  system_prompt=" You are a helpful AI assistant.You can answer general questions.Use the multiply tool only when the user asks for multiplication.Remember the conversation context."
    # system_prompt="You are a helpful assistant that can multiply two numbers.",
)
4