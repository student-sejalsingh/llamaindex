import asyncio

from llama_index.core.workflow import (
    HumanResponseEvent,
    InputRequiredEvent,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)


class NumberWorkflow(Workflow):
    @step
    # This step is the starting point of the workflow. It will be called when the workflow is run.
    async def ask(self, ev: StartEvent) -> InputRequiredEvent:
        return InputRequiredEvent(prefix="Enter a number: ")

    @step
    # This step will be called when the user provides a response to the InputRequiredEvent.
    async def answer(self, ev: HumanResponseEvent) -> StopEvent:
        return StopEvent(result=ev.response)


workflow = NumberWorkflow()


async def main() -> None:
    handler = workflow.run()
    async for event in handler.stream_events():
        print(event)
        # Process each event as it comes in
        if isinstance(event, InputRequiredEvent):
            # This could be input(), a websocket reply, a web form submission, etc.
            response = input(event.prefix)
            await handler.send_event(HumanResponseEvent(response=response))

    final_result = await handler
    print(final_result)


if __name__ == "__main__":
    asyncio.run(main())