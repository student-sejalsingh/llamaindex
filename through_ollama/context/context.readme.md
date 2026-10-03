# LlamaIndex Context and Conversation Memory

## What is Context?

`Context` is the short-term memory of an `AgentWorkflow`. It stores conversation history and workflow state. It is managed by the LlamaIndex application, not by the LLM itself.

```python
from llama_index.core.workflow import Context

ctx = Context(agent)
```

An LLM is stateless: it only knows what the application includes in the current request. The application uses `Context` to include relevant earlier messages, tool results, variables, and execution state.

## Why Reuse the Same Context?

Without a shared context, each `run()` starts a new conversation:

```python
await agent.run("My name is Logan")
await agent.run("What is my name?")
```

The second call may not know the name. Reusing one context preserves the conversation:

```python
ctx = Context(agent)

await agent.run("My name is Logan", ctx=ctx)
await agent.run("What is my name?", ctx=ctx)
```

The second response can then be:

```text
Your name is Logan.
```

## How Context Works

```text
User query
	|
	v
agent.run(query, ctx=ctx)
	|
	v
Read previous context and build the prompt
	|
	v
Call the LLM
	|
	v
Store the response and updated workflow state
```

The context lifecycle is:

```text
Context(agent) -> empty memory -> run 1 -> stored conversation
									  -> run 2 -> previous conversation is reused
```

## Example in This Folder

The agent in `starter.py` uses Ollama and sets an 8,000-token context window:

```python
from llama_index.llms.ollama import Ollama
from llama_index.core.agent.workflow import FunctionAgent

agent = FunctionAgent(
	llm=Ollama(
		model="qwen3:0.6b",
		request_timeout=360.0,
		context_window=8000,
	),
	system_prompt=(
		"You are a helpful AI assistant. "
		"You can answer general questions. "
		"Use the multiply tool only when the user asks for multiplication."
	),
)
```

Create the context once and reuse it for the entire session:

```python
import asyncio

from llama_index.core.workflow import Context
from starter import agent


async def main():
	ctx = Context(agent)

	first_response = await agent.run("My name is Logan", ctx=ctx)
	print(first_response)

	second_response = await agent.run("What is my name?", ctx=ctx)
	print(second_response)


if __name__ == "__main__":
	asyncio.run(main())
```

For an interactive conversation, keep the same `ctx` inside the loop:

```python
ctx = Context(agent)

while True:
	query = input("> ")
	if query.lower() in {"exit", "quit"}:
		break

	response = await agent.run(query, ctx=ctx)
	print(response)
```

## What Context Stores

- Previous user messages
- Assistant responses
- Tool outputs
- Workflow state
- Variables
- Agent execution state

## Context vs. Context Window

| Context | Context window |
| --- | --- |
| Conversation and workflow memory | Maximum tokens processed in one request |
| Managed by LlamaIndex or the application | Defined by the model or client configuration |
| Can be reused across multiple runs | Limits how much history can be sent to the model |

The context window is not permanent memory. Typical model limits include 8K, 32K, or 128K tokens. When a conversation becomes too large, an application may remove old messages, summarize them, or retrieve only relevant history.

## LLM Memory vs. Application Memory

```text
Conversation history
	|
	v
Application or LlamaIndex Context
	|
	v
Prompt construction
	|
	v
LLM response
	|
	v
Save the new response in Context
```

The LLM does not independently remember a previous request. Chat applications provide the appearance of memory by storing conversation data and sending the appropriate history with each new request.

## Short-Term and Long-Term Memory

`Context` is useful for short-term, in-session memory. It is not a replacement for durable storage. For long-term memory, store important information outside the active context and retrieve it when needed:

```text
Conversation -> embeddings -> vector database -> retriever -> relevant memories -> LLM
```

Common vector database choices include ChromaDB, FAISS, Pinecone, and Qdrant. This retrieval pattern is commonly called retrieval-augmented generation (RAG).

## Common Mistakes

### Creating a new context for every request

This discards the previous conversation:

```python
ctx = Context(agent)  # Do not recreate this for every message.
```

Create it once per conversation or session instead.

### Using an overly restrictive system prompt

This prompt prevents general conversation:

```text
You are a helpful assistant that can multiply two numbers.
```

A user asking their name may receive a request for two numbers. Prefer a prompt that allows general questions and describes when tools should be used:

```text
You are a helpful AI assistant. Use the multiply tool only when needed.
```

### Expecting the LLM to remember automatically

The application must pass prior messages through `Context`, a database, or another memory mechanism. The model alone does not retain them between requests.

## Key Takeaways

- `Context` is short-term conversation and workflow memory.
- The LLM is stateless unless the application supplies previous information.
- Reuse the same `Context` for multi-turn conversations.
- `context_window` limits the amount of text the model can process in one request.
- Long conversations need summarization, selective retrieval, or both.
- A larger context window lets a model read more text; it does not make the model more intelligent.

> LLM = brain; Context = short-term memory; vector database = long-term memory; retriever = librarian; LlamaIndex = the manager that builds the final prompt.
