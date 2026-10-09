from workflows import Workflow, step
from workflows.events import (
    StartEvent,
    StopEvent,
    InputRequiredEvent,
    HumanResponseEvent,
)

from through_ollama.human_in_loop.stoping_resumining.db import FakeDB

class ApprovalWorkflow(Workflow):
    def __init__(self, db: FakeDB):
        self.db = db

    @step
    async def ask(self, ev: StartEvent):
        return InputRequiredEvent(prefix="Approve? ")

    @step
    async def answer(self, ev: HumanResponseEvent):
        return StopEvent(result=ev.response)