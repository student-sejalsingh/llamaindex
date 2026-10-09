# Module 02 – Prompt Templates & Prompt Engineering

## 📖 Overview

This module introduces **Prompt Templates** and **Prompt Engineering** in LlamaIndex.

A prompt is the instruction given to a Large Language Model (LLM). Instead of writing prompts manually every time, LlamaIndex provides reusable template classes that make prompts dynamic, maintainable, and easier to manage.

By the end of this module, you will understand how to create reusable prompts, chat prompts, system prompts, and apply prompt engineering techniques to improve LLM responses.

---

# 🎯 Learning Objectives

After completing this module, you should be able to:

- Create reusable prompts using `PromptTemplate`
- Pass single and multiple variables
- Build chat prompts using `ChatPromptTemplate`
- Understand the role of system prompts
- Use `partial_format()` for reusable prompt configurations
- Apply prompt engineering techniques
- Know when to use each type of prompt

---

# 📂 Folder Structure

```
02_prompts/
│
├── 01_prompt_template.py
├── 02_multiple_variables.py
├── 03_chat_prompt.py
├── 04_system_prompt.py
├── 05_partial_format.py
├── 06_prompt_engineering.py
└── README.md
```

---

# Lessons

---

## 1. PromptTemplate

**File**

```
01_prompt_template.py
```

### Purpose

Creates reusable prompts with placeholders.

### Example

```python
template = PromptTemplate(
"""
Explain {topic} in simple language.
"""
)

prompt = template.format(
    topic="Binary Search"
)
```

### Use Cases

- Text generation
- Blog writing
- Summarization
- Report generation

---

## 2. Multiple Variables

**File**

```
02_multiple_variables.py
```

### Purpose

Uses multiple placeholders inside one prompt.

### Example

```python
template = PromptTemplate(
"""
Subject : {subject}

Topic : {topic}

Difficulty : {difficulty}
"""
)
```

### Use Cases

- Worksheet Generator
- Resume Analyzer
- Email Generator
- Question Paper Generator

---

## 3. ChatPromptTemplate

**File**

```
03_chat_prompt.py
```

### Purpose

Creates reusable **chat messages** instead of plain text prompts.

### Example

```python
ChatPromptTemplate(
    message_templates=[
        ChatMessage(
            role="system",
            content="You are a teacher."
        ),
        ChatMessage(
            role="user",
            content="Explain {topic}"
        )
    ]
)
```

### Returns

A list of `ChatMessage` objects.

### Use Cases

- Chatbots
- AI Assistants
- Agents
- Customer Support

---

## 4. System Prompt

**File**

```
04_system_prompt.py
```

### Purpose

Defines the role, behavior, tone, and rules of the AI.

### Example

```
You are an experienced Computer Science professor.

Explain concepts using simple language.
```

### Controls

- Personality
- Tone
- Rules
- Output Style

### Use Cases

- Education Bots
- Medical Assistant
- Agriculture Assistant
- Coding Assistant

---

## 5. Partial Formatting

**File**

```
05_partial_format.py
```

### Purpose

Fills some variables now and the remaining variables later.

### Example

```python
partial = template.partial_format(
    teacher_type="NCERT Teacher"
)

prompt = partial.format(
    class_name="2",
    topic="Addition"
)
```

### Benefits

- Reusable templates
- Cleaner code
- Avoid repeated values

---

## 6. Prompt Engineering

**File**

```
06_prompt_engineering.py
```

### Purpose

Design prompts that produce better LLM responses.

### Techniques

- Zero-shot Prompting
- One-shot Prompting
- Few-shot Prompting
- Role Prompting
- Constraint Prompting
- Step-by-step Prompting

### Example

```
You are a Computer Science professor.

Explain Binary Search.

Rules:

- Use simple language.
- Give one example.
- Provide Python code.
- Keep under 300 words.
```

---

# PromptTemplate vs ChatPromptTemplate

| Feature | PromptTemplate | ChatPromptTemplate |
|----------|----------------|--------------------|
| Returns | String | List of ChatMessage |
| Used With | complete() | chat() |
| Conversation | ❌ No | ✅ Yes |
| Best For | Text Generation | Chatbots & Agents |

---

# format() vs partial_format()

| format() | partial_format() |
|-----------|------------------|
| Fill all variables | Fill some variables |
| One-step formatting | Two-step formatting |
| Simple prompts | Reusable large applications |

---

# Prompt Engineering vs PromptTemplate

| Prompt Engineering | PromptTemplate |
|--------------------|----------------|
| A concept and skill | A LlamaIndex class |
| Focuses on writing effective prompts | Makes prompts reusable |
| Works with any LLM | Part of LlamaIndex |
| Decides **what** to ask | Helps generate the prompt |

---

# Real-World Examples

## FLN Platform

Variables

- Class
- Subject
- Topic
- Difficulty

System Prompt

```
You are an NCERT teacher.

Generate worksheets following NEP 2020.
```

---

## KrishiDarshan Chatbot

Variables

- Context
- Question

System Prompt

```
You are an agriculture expert.

Answer only from the provided context.

Respond in Hindi.
```

---

## Resume Analyzer

Variables

- Resume
- Job Description

System Prompt

```
You are an HR Manager.

Analyze the resume and provide ATS score.
```

---

## Coding Assistant

Variables

- Programming Language
- Problem Statement

System Prompt

```
You are an expert Python developer.

Write clean and well-documented code.
```

---

# Key Takeaways

- A prompt tells the LLM what to do.
- `PromptTemplate` creates reusable prompts.
- `ChatPromptTemplate` creates reusable chat conversations.
- A system prompt controls the AI's behavior.
- `partial_format()` is useful when some prompt values remain constant.
- Prompt engineering is the skill of designing better prompts.
- Better prompts usually lead to better AI responses.

---

# Summary Diagram

```
                 Prompt Engineering
                         │
                         ▼
             Design Good Instructions
                         │
      ┌──────────────────┴──────────────────┐
      │                                     │
      ▼                                     ▼
 PromptTemplate                    ChatPromptTemplate
      │                                     │
      ▼                                     ▼
 String Prompt                  List of Chat Messages
      │                                     │
      ▼                                     ▼
 complete()                         chat()
      │                                     │
      └──────────────────┬──────────────────┘
                         ▼
                         LLM
                         ▼
                    AI Response
```

---

# Next Module

➡️ **Module 03 – Documents**

Topics include:

- Document
- SimpleDirectoryReader
- PDF Loader
- Web Page Loader
- Markdown Loader
- Document Metadata