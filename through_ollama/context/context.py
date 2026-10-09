from llama_index.core.workflow import Context
import asyncio
from starter import agent
print ("Starting the agent with context...")

async def main():
   # create context
   ctx = Context(agent)

#    response = await agent.run("My name is Sejal", ctx=ctx)
#    print(response)

#    response = await agent.run("What is my name?", ctx=ctx)
#    print(response)
#    user context
   while True:
    query = input("> ")
    result=await agent.run(query, ctx=ctx)
    print(str(result))


   # run agent with context
#    conversation context
#    response = await agent.run("My name is Logan", ctx=ctx)
#    print(response)
#    response = await agent.run("What is my name?", ctx=ctx)
#    print(response)


if __name__ == "__main__":
   asyncio.run(main())