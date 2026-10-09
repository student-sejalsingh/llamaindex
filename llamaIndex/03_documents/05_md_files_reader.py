from llama_index.core import SimpleDirectoryReader


# Load Markdown files from the markdown folder
documents = SimpleDirectoryReader(
    input_dir="data/02_md",
    recursive=True,
    required_exts=[".md"],
).load_data()


print("\n📚 Total Markdown Documents:", len(documents))


for i, document in enumerate(documents):

    print("\n" + "=" * 70)
    print(f"📄 Markdown Document {i + 1}")
    print("=" * 70)

    # Automatically generated metadata
    print("\n🏷️ Metadata:")
    print(document.metadata)

    # Extracted Markdown content
    print("\n📝 Content:")
    print(document.text[:1000])

    print("\n...")