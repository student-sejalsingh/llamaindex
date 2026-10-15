from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
)

from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


# --------------------------------------------------
# 1. Configure the local LLM
# --------------------------------------------------

Settings.llm = Ollama(
    model="qwen3:0.6b",
    request_timeout=120.0,
)
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text"
)
print("Local LLM configured successfully!")


# --------------------------------------------------
# 2. Create a SQLite database
# --------------------------------------------------

engine = create_engine("sqlite:///students.db")

metadata = MetaData()


# --------------------------------------------------
# 3. Define the students table
# --------------------------------------------------

students = Table(
    "students",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("subject", String(50)),
    Column("marks", Integer),
)


# Create the table
metadata.create_all(engine)

print("Database and table created successfully!")


# --------------------------------------------------
# 4. Insert sample data
# --------------------------------------------------

with engine.begin() as connection:

    # Insert data only if the table is empty
    existing_students = connection.execute(
        students.select()
    ).fetchone()

    if existing_students is None:

        connection.execute(
            students.insert(),
            [
                {
                    "name": "Sejal",
                    "subject": "DBMS",
                    "marks": 85,
                },
                {
                    "name": "Priya",
                    "subject": "DBMS",
                    "marks": 92,
                },
                {
                    "name": "Aman",
                    "subject": "DBMS",
                    "marks": 78,
                },
                {
                    "name": "Rahul",
                    "subject": "DBMS",
                    "marks": 88,
                },
            ],
        )

print("Student data inserted successfully!")


# --------------------------------------------------
# 5. Connect LlamaIndex to the SQL database
# --------------------------------------------------

sql_database = SQLDatabase(
    engine,
    include_tables=["students"],
)

print("LlamaIndex connected to the database!")


# --------------------------------------------------
# 6. Create the SQL Query Engine
# --------------------------------------------------

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    tables=["students"],
    llm=Settings.llm,
    verbose=True,
)

print("SQL Query Engine created successfully!")


# --------------------------------------------------
# 7. Ask questions in natural language
# --------------------------------------------------

while True:

    question = input(
        "\nAsk a question about students "
        "(type 'exit' to stop): "
    )

    if question.strip().lower() == "exit":
        break

    try:

        response = query_engine.query(question)

        print("\nAnswer:")
        print(response)

        # Display the generated SQL query
        if response.metadata:
            sql_query = response.metadata.get("sql_query")

            if sql_query:
                print("\nGenerated SQL:")
                print(sql_query)

    except Exception as error:
        print("\nSomething went wrong:")
        print(error)

