from workflows import Workflow, step
from workflows.events import (
    StartEvent,
    StopEvent,
    InputRequiredEvent,
    HumanResponseEvent,
)


class ApprovalWorkflow(Workflow):
    """
    A simple Human-in-the-Loop workflow.

    Flow:
        StartEvent
            ↓
        ask()
            ↓
        InputRequiredEvent
            ↓
        HumanResponseEvent
            ↓
        answer()
            ↓
        StopEvent
    """

    @step
    async def ask(self, ev: StartEvent) -> InputRequiredEvent:
        print("Step 1: ask() executed")

        return InputRequiredEvent(
            prefix="Do you approve this request? (yes/no): "
        )

    @step
    async def answer(self, ev: HumanResponseEvent) -> StopEvent:
        print("Step 2: answer() executed")

        if ev.response.lower() == "yes":
            return StopEvent(result="Request Approved")

        return StopEvent(result="Request Rejected")
