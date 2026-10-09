# Human-in-the-Loop Workflow Example

This project demonstrates the **Human-in-the-Loop (HITL)** pattern using the **Workflows** library. The workflow pauses execution, waits for human input, and resumes once the input is provided.

It is the simplest implementation of the official Human-in-the-Loop example from the Workflows documentation.

---

# Workflow Overview

```text
          workflow.run()
                │
                ▼
          StartEvent
                │
                ▼
          ask() Step
                │
                ▼
     InputRequiredEvent
                │
                ▼
    handler.stream_events()
                │
                ▼
       User Enters Input
                │
                ▼
    HumanResponseEvent
                │
                ▼
         answer() Step
                │
                ▼
          StopEvent
                │
                ▼
         Final Result
```

---

# What This Example Demonstrates

This example teaches the core Human-in-the-Loop workflow pattern:

1. Start a workflow.
2. Pause execution when user input is required.
3. Notify the application that input is needed.
4. Accept the user's response.
5. Resume the workflow.
6. Finish execution and return the result.

Instead of calling `input()` directly inside the workflow, the workflow emits an `InputRequiredEvent`. The application decides how to collect the user's response and sends it back using a `HumanResponseEvent`.

This makes the same workflow usable in:

* Terminal applications
* Web applications
* Mobile applications
* Chatbots
* APIs
* WebSocket-based systems

---

# Code Explanation

## Imports

```python
from workflows import Workflow, step
from workflows.events import (
    StartEvent,
    StopEvent,
    InputRequiredEvent,
    HumanResponseEvent
)
```

### Workflow

The base class used to define workflow logic.

### step

Marks a function as a workflow step.

### StartEvent

Automatically generated when the workflow starts.

### InputRequiredEvent

Signals that the workflow needs input from a human before continuing.

### HumanResponseEvent

Carries the user's response back into the workflow.

### StopEvent

Ends the workflow and returns the final result.

---

## Step 1 — Ask for Input

```python
@step
async def ask(self, ev: StartEvent) -> InputRequiredEvent:
    return InputRequiredEvent(prefix="Enter a number: ")
```

When the workflow begins, it receives a `StartEvent`.

Instead of continuing immediately, it returns an `InputRequiredEvent`, telling the application that human input is required.

At this point, the workflow pauses.

---

## Step 2 — Receive Human Response

```python
@step
async def answer(self, ev: HumanResponseEvent) -> StopEvent:
    return StopEvent(result=ev.response)
```

This step executes only after a `HumanResponseEvent` is received.

The user's response is stored in:

```python
ev.response
```

The workflow then returns a `StopEvent`, ending execution.

---

## Running the Workflow

```python
workflow = NumberWorkflow()

handler = workflow.run()
```

Calling `workflow.run()` starts the workflow and returns a **handler**.

The handler controls the running workflow.

It can:

* Stream events
* Send new events
* Cancel execution
* Wait for completion

---

## Listening for Events

```python
async for event in handler.stream_events():
```

The application listens for events emitted by the workflow.

When an `InputRequiredEvent` appears, the application knows that user input is required.

---

## Asking the User

```python
response = input(event.prefix)
```

In this example, the terminal is used to collect input.

In a real application, this could be replaced with:

* A web form
* A chatbot message
* A mobile application
* A dialog box
* A WebSocket message

---

## Sending the Response

```python
await handler.send_event(
    HumanResponseEvent(response=response)
)
```

The application sends the user's response back to the workflow.

The workflow automatically resumes execution from the waiting step.

---

## Waiting for Completion

```python
final_result = await handler
```

This waits until the workflow reaches a `StopEvent`.

The result stored inside the `StopEvent` is returned.

---

# Execution Sequence

```text
workflow.run()
      │
      ▼
StartEvent
      │
      ▼
ask()
      │
      ▼
InputRequiredEvent
      │
      ▼
Application receives event
      │
      ▼
User enters value
      │
      ▼
HumanResponseEvent
      │
      ▼
answer()
      │
      ▼
StopEvent
      │
      ▼
Workflow Complete
```

---

# Expected Output

```
Enter a number:
```

Example input:

```
25
```

Final result:

```
25
```

---

# Why Use Human-in-the-Loop?

Human-in-the-Loop allows workflows to safely pause before performing actions that require user confirmation.

Common use cases include:

* Sending emails
* Deleting files
* Approving payments
* Database updates
* API requests
* Booking tickets
* Publishing content

Instead of executing these actions automatically, the workflow waits for explicit user approval.

---

# Key Concepts Learned

* Workflow
* Step
* StartEvent
* InputRequiredEvent
* HumanResponseEvent
* StopEvent
* Handler
* Event Streaming
* Pause and Resume
* Human-in-the-Loop

---

# Next Steps

After understanding this example, you can extend it to build more advanced workflows, such as:

* Email approval workflows
* Document approval systems
* Multi-step forms
* AI agents requiring human confirmation
* Multi-agent workflows
* Long-running workflows with pause and resume support
