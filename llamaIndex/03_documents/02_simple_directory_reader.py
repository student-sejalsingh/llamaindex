from llama_index.core import SimpleDirectoryReader


# Load files from data/ and all its subfolders
documents = SimpleDirectoryReader(
    input_dir="data",
    recursive=True
).load_data()


print("\n📚 Total Documents:", len(documents))


for i, document in enumerate(documents):

    print("\n" + "=" * 70)
    print(f"📄 Document {i + 1}")
    print("=" * 70)

    print("\n🏷️ Metadata:")
    print(document.metadata)

    print("\n📝 Content:")
    print(document.text[:500])

    print("\n...")