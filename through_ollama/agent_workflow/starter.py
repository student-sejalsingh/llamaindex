import asyncio
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from ddgs import DDGS
from dotenv import load_dotenv


# Define a simple calculator tool
def multiply(a: float, b: float) -> float:
    """Useful for multiplying two numbers."""
    return a * b

def add(a: float, b: float) -> float:
    """Useful for adding two numbers."""
    return a + b

# custom tool
def get_age(name: str) -> int:
    """Get the age of a person by name."""
    # For demonstration purposes, we'll use a simple dictionary to store ages.
    ages = {
        "Alice": 30,
        "Bob": 25,
        "Charlie": 35,
    }
    return ages.get(name, -1)  # Return -1 if the name is not found

# database tool
def get_user_info(user_id: int) -> dict:
    """Get the information of a user by ID."""
    # For demonstration purposes, we'll use a simple dictionary to store user information.
    users = {
        1: {"name": "Alice", "age": 30},
        2: {"name": "Bob", "age": 25},
        3: {"name": "Charlie", "age": 35},
    }
    return users.get(user_id, {})  # Return an empty dictionary if the user ID is not found
def weather_tool(location: str) -> str:
    """Get the current weather for a given location."""
    # For demonstration purposes, we'll return a static weather report.
    # In a real-world scenario, you would integrate with a weather API.
    weather_reports = {
        "New York": "Sunny, 25°C",
        "Los Angeles": "Cloudy, 20°C",
        "Chicago": "Rainy, 15°C",
    }
    return weather_reports.get(location, "Weather data not available for this location.")

# file search tool
def file_search_tool(file_name: str) -> str:
    """Search for a file by name and return its path."""
    # For demonstration purposes, we'll use a simple dictionary to simulate file paths.
    # In a real-world scenario, you would implement a more sophisticated file search mechanism.
    files = {
        "document.txt": "/path/to/document.txt",
        "image.png": "/path/to/image.png",
        "report.pdf": "/path/to/report.pdf",
    }
    return files.get(file_name, "File not found.")

def web_search_tool(query: str) -> str:
    """Search the web."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
    output = ""

    for r in results:
        output += f"""
Title: {r['title']}
Snippet: {r['body']}
URL: {r['href']}

"""

    return output


# Create an agent workflow with our calculator tool
agent = FunctionAgent(
    # tools=[multiply, add, get_age, get_user_info, weather_tool, file_search_tool, web_search_tool],
    tools=[web_search_tool],
    llm=Ollama(
        model="qwen3:4b",
        request_timeout=360.0,
        # Manually set the context window to limit memory usage
        context_window=8000,
    ),
    system_prompt="You are a helpful assistant that can multiply , add two numbers , get the information of a user by ID ,weather information for a location , get the age of a person by name.",
)




async def main():
    # Run the agent
    response = await agent.run("What is 1234 * 4567?")
    response2 = await agent.run("What is 1234 + 4567?")
    response3 = await agent.run("What is the age of Alice?")
    response4 = await agent.run("What is the information of user 1?")
    response5 = await agent.run("What is the weather in New York?")
    response6 = await agent.run("Where is the file document.txt located?")
    response7 = await agent.run("Search the web for the latest news on AI.")
    print(str(response))
    print(str(response2))
    print(str(response3))
    print(str(response4))
    print(str(response5))
    print(str(response6))
    print(str(response7))
# Run the agent
if __name__ == "__main__":
    asyncio.run(main())