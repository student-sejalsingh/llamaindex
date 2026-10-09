import asyncio

from llama_index.llms.ollama import Ollama

# Initialize the LLM
llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


async def ask_llm(prompt: str):
    """Send an async request to the LLM."""
    response = await llm.acomplete(prompt)

    print(f"\nPrompt: {prompt}")
    print(response.text)


async def main():
    # Run all requests concurrently
    await asyncio.gather(
        ask_llm("What is Artificial Intelligence?"),
        ask_llm("Explain Machine Learning."),
        ask_llm("What is Deep Learning?")
    )


if __name__ == "__main__":
    asyncio.run(main())