import asyncio
import json

from workflows import Context
from workflows.events import (
    InputRequiredEvent,
    HumanResponseEvent,
)

from workflow.approval_workflow import ApprovalWorkflow
from database.fake_db import FakeDB


async def main():
    # Create workflow
    workflow = ApprovalWorkflow()

    # Create fake database
    db = FakeDB()

    print("Starting workflow...\n")

    # Start workflow
    handler = workflow.run()

    # Listen for workflow events
    async for event in handler.stream_events():

        if isinstance(event, InputRequiredEvent):

            print(f"Workflow paused.")
            print(f"Message: {event.prefix}\n")

            # Save workflow context
            ctx_json = json.dumps(handler.ctx.to_dict())

            await db.save("run-123", ctx_json)

            print("Workflow context saved.\n")

            # Stop current workflow
            await handler.cancel_run()

            print("Workflow cancelled.\n")

            break

    # -------------------------------------------------------
    # Simulate user coming back later
    # -------------------------------------------------------

    input("Press Enter to simulate the user returning...\n")

    response = input("Enter your response (yes/no): ")

    # Load saved context
    saved_ctx = await db.load("run-123")

    ctx_dict = json.loads(saved_ctx)

    restored_ctx = Context.from_dict(workflow, ctx_dict)

    print("\nWorkflow restored.\n")

    # Resume workflow
    handler = workflow.run(ctx=restored_ctx)

    # Send human response
    await handler.send_event(
        HumanResponseEvent(response=response)
    )

    # Consume remaining events
    async for _ in handler.stream_events():
        pass

    # Wait for completion
    final_result = await handler

    print("\nWorkflow Finished")
    print("-------------------------")
    print("Final Result:", final_result)


if __name__ == "__main__":
    asyncio.run(main())