# Human-in-the-Loop Approval Workflow

This example demonstrates how to pause a workflow while waiting for human input,
save its state, and resume it later.

The workflow asks whether a request should be approved. It pauses at the
approval step, stores its context in a JSON file, and resumes after the user
enters `yes` or `no`.

## Project structure

```text
agent/
├── main.py
├── database/
│   └── fake_db.py
└── workflow/
    └── approval_workflow.py
```

## How it works

1. `main.py` creates an `ApprovalWorkflow`.
2. `workflow.run()` starts the workflow.
3. The `ask()` step emits an `InputRequiredEvent`.
4. `main.py` detects that event and saves the workflow context.
5. The current handler is cancelled to simulate a paused workflow.
6. The user enters an approval response later.
7. The saved context is loaded and restored.
8. A `HumanResponseEvent` resumes the workflow.
9. The `answer()` step returns either `Request Approved` or `Request Rejected`.

```text
StartEvent
    |
    v
ask()
    |
    v
InputRequiredEvent
    |
    v
Save context and cancel run
    |
    v
Restore context
    |
    v
HumanResponseEvent
    |
    v
answer()
    |
    v
StopEvent
```

## Requirements

- Python 3.10 or newer
- The `workflows` package

Install the dependency if it is not already installed:

```powershell
pip install workflows
```

## Run the example

Open PowerShell in this directory:

```powershell
cd C:\Users\PC\Desktop\sejal_work\LlamaIndex-final\through_ollama\human_in_loop\agent
```

Then run:

```powershell
python main.py
```

The program first asks you to press Enter to simulate returning to the
application later. It then asks:

```text
Enter your response (yes/no):
```

Use `yes` to approve the request. Any other response is treated as a
rejection.

Example output:

```text
Starting workflow...

Step 1: ask() executed
Workflow paused.
Message: Do you approve this request? (yes/no):

Workflow context saved.
Workflow cancelled.

Workflow restored.

Step 2: answer() executed

Workflow Finished
-------------------------
Final Result: Request Approved
```

## Workflow context storage

`database/fake_db.py` provides a small file-based storage helper. The workflow
context is written to:

```text
storage/workflow_state.json
```

This is only a demonstration database. It uses one file for the workflow
state and does not provide production features such as multiple records,
concurrency control, authentication, or cleanup.

## Important classes and events

- `ApprovalWorkflow`: Defines the workflow steps.
- `ask()`: Pauses the workflow by returning `InputRequiredEvent`.
- `answer()`: Processes `HumanResponseEvent` and ends the workflow.
- `FakeDB`: Saves and loads the serialized workflow context.
- `Context`: Converts workflow state to and from a serializable dictionary.
- `InputRequiredEvent`: Signals that human input is needed.
- `HumanResponseEvent`: Carries the human response back to the workflow.
- `StopEvent`: Ends the workflow with the final result.

## Adapting this example

In a real application, replace the terminal `input()` calls with a user
interface or API endpoint. The same pattern can support approval flows for:

- Sending emails
- Publishing content
- Updating records
- Approving payments
- Calling external services
