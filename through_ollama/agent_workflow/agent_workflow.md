# LlamaIndex Agent Workflow

This example creates a LlamaIndex `FunctionAgent` powered by a local Ollama model. The agent can call Python functions as tools when those functions are included in the `tools` list.

## Requirements

Install the packages used by `starter.py`:

```powershell
pip install llama-index llama-index-llms-ollama ddgs python-dotenv
```

Install Ollama and download the model:

```powershell
ollama pull qwen3:4b
```

Ollama must be running before starting the script.

## Run the Example

From the `agent_workflow` directory:

```powershell
python starter.py
```

The script creates an agent, sends several requests, and prints the responses.

## Tools Defined in `starter.py`

- `multiply(a, b)` multiplies two numbers.
- `add(a, b)` adds two numbers.
- `get_age(name)` returns demo ages for Alice, Bob, and Charlie.
- `get_user_info(user_id)` returns demo user information.
- `weather_tool(location)` returns a static weather report.
- `file_search_tool(file_name)` returns a demo file path.
- `web_search_tool(query)` searches the web through `ddgs`.

Only the web search tool is currently enabled:

```python
tools=[web_search_tool]
```

To enable all defined tools, use:

```python
tools=[
	multiply,
	add,
	get_age,
	get_user_info,
	weather_tool,
	file_search_tool,
	web_search_tool,
]
```

## How the Workflow Works

```text
User request
	|
	v
FunctionAgent
	|
	+--> Selects a matching Python tool when needed
	|
	+--> Sends requests to the Ollama model
	|
	v
Printed response
```

The function tools in this example use demonstration data. The database, weather, and file-search tools do not connect to real services.

## Ollama Timeout Troubleshooting

The `qwen3:4b` model may be slow on a CPU. If the script raises `httpx.ReadTimeout`, test Ollama directly:

```powershell
ollama run qwen3:4b "Say hello"
```

You can use a smaller installed model, such as `qwen3:0.6b`, by changing the model configuration:

```python
llm=Ollama(
	model="qwen3:0.6b",
	request_timeout=360.0,
	context_window=8000,
)
```

The `ddgs` package replaces the older `duckduckgo_search` package. Web search also requires an internet connection.
