import json
import asyncio
from workflows import Workflow, step
from workflows import Context

async def main():
    handler = workflow.run()
    async for event in handler.stream_events():
        if isinstance(event, InputRequiredEvent):
            await db.save("run-123", json.dumps(handler.ctx.to_dict()))
            await handler.cancel_run()
            break

    # Later, when the human response arrives:
    response = form_data["response"]
    ctx_dict = json.loads(await db.load("run-123"))
    restored_ctx = Context.from_dict(workflow, ctx_dict)
    handler = workflow.run(ctx=restored_ctx)

    await handler.send_event(HumanResponseEvent(response=response))
    async for event in handler.stream_events():
        continue

    final_result = await handler
    return final_result


if __name__ == "__main__":
    asyncio.run(main())