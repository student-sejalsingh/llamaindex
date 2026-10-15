
from pymongo import MongoClient

from llama_index.core import (
    Document,
    VectorStoreIndex,
    Settings,
)

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


# 1. Configure local models
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)


# 2. Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

database = client["college_db"]
collection = database["notes"]


# 3. Read documents from MongoDB
mongo_documents = collection.find(
    {},
    {
        "_id": 0,
        "topic": 1,
        "subject": 1,
        "content": 1,
    },
)

documents = []

for item in mongo_documents:

    content = item.get("content", "")

    if not content:
        continue

    document = Document(
        text=content,
        metadata={
            "topic": item.get("topic", "Unknown"),
            "subject": item.get("subject", "Unknown"),
        },
    )

    documents.append(document)


if not documents:
    raise ValueError(
        "No usable documents found in MongoDB collection 'notes'."
    )


print(f"Loaded {len(documents)} documents from MongoDB.")


# 4. Create the LlamaIndex index
index = VectorStoreIndex.from_documents(documents)

print("VectorStoreIndex created successfully!")


# 5. Create a query engine
query_engine = index.as_query_engine(
    similarity_top_k=3
)


# 6. Ask questions
while True:

    question = input(
        "\nAsk a question about your notes "
        "(type 'exit' to stop): "
    )

    if question.strip().lower() == "exit":
        break

    try:
        response = query_engine.query(question)

        print("\nAnswer:")
        print(response)

    except Exception as error:
        print("\nError:", error)


client.close()

