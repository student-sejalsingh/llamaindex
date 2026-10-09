# Module 1 – Large Language Models (LLMs)

## 📖 Overview

This module introduces the basics of working with Large Language Models (LLMs) in **LlamaIndex**. It covers how to connect to an LLM, generate responses, stream outputs, and make asynchronous requests.

The examples in this module use **Ollama** as the local LLM provider, but the same concepts apply to OpenAI, Gemini, Anthropic, and other supported providers.

---

# Learning Objectives

After completing this module, you should be able to:

- Understand what an LLM is in LlamaIndex.
- Connect to a local LLM using Ollama.
- Generate text using `complete()`.
- Create conversations using `chat()`.
- Stream responses in real time.
- Make asynchronous LLM requests.
- Understand when to use each method.

---

# Folder Structure

```
01_llms/
│
├── 01_basic_chat.py
├── 02_completion.py
├── 03_streaming.py
├── 04_async.py
└── README.md
```

---

# Examples

## 1. Basic Chat

**File**

```
01_basic_chat.py
```

### Purpose

Demonstrates how to create a conversation with an LLM using `chat()`.

### Key Concepts

- ChatMessage
- system role
- user role
- assistant response

Use this when building:

- Chatbots
- AI Assistants
- Agent Systems

---

## 2. Completion

**File**

```
02_completion.py
```

### Purpose

Shows how to generate text from a single prompt using `complete()`.

### Key Concepts

- Single Prompt
- CompletionResponse
- response.text

Use this when building:

- Blog generators
- Code generators
- Summarizers
- Text rewriting tools

---

## 3. Streaming

**File**

```
03_streaming.py
```

### Purpose

Streams the response token by token instead of waiting for the complete answer.

### Key Concepts

- stream_complete()
- stream_chat()
- chunk.delta
- flush=True

Benefits

- Better user experience
- Real-time output
- Faster perceived response

---

## 4. Async

**File**

```
04_async.py
```

### Purpose

Runs multiple LLM requests concurrently using Python's asyncio.

### Key Concepts

- async
- await
- acomplete()
- asyncio.gather()

Benefits

- Better performance
- Multiple requests at once
- Used heavily in agents and workflows

---

# chat() vs complete()

| Feature | chat() | complete() |
|----------|--------|------------|
| Input | Conversation | Single Prompt |
| Roles | ✅ Yes | ❌ No |
| Memory | ✅ Yes | ❌ No |
| Best For | Chatbots | Text Generation |

---

# Streaming vs Normal Response

Normal

```
Request
   ↓
Wait
   ↓
Full Response
```

Streaming

```
Request
   ↓
Token 1
Token 2
Token 3
...
```

Streaming improves the user experience because the response appears immediately.

---

# Sync vs Async

Synchronous

```
Task 1
 ↓
Task 2
 ↓
Task 3
```

Asynchronous

```
Task 1 ───┐
Task 2 ───┼── Run Together
Task 3 ───┘
```

Async is useful when multiple requests can run concurrently.

---

# Important Methods

| Method | Description |
|----------|-------------|
| chat() | Chat conversation |
| complete() | Text completion |
| stream_chat() | Stream chat response |
| stream_complete() | Stream completion response |
| achat() | Async chat |
| acomplete() | Async completion |

---

# Key Takeaways

- `chat()` is used for conversations.
- `complete()` is used for single prompts.
- Streaming provides responses token by token.
- Async allows multiple LLM requests to run concurrently.
- LlamaIndex provides a unified interface for different LLM providers.

---

# Next Module

➡️ Module 2 – Prompt Templates

Topics include:

- PromptTemplate
- ChatPromptTemplate
- Template Variables
- Dynamic Prompts
- Prompt Engineering