from llama_index.core import SimpleDirectoryReader


# Load documents from your dataset
documents = SimpleDirectoryReader(
    input_dir="data",
    recursive=True,
).load_data()


print("\n📚 Total Documents:", len(documents))


for i, document in enumerate(documents):

    print("\n" + "=" * 70)
    print(f"📄 Document {i + 1}")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Automatically generated metadata
    # --------------------------------------------------

    print("\n🤖 Automatic Metadata:")
    print(document.metadata)

    print("\n📁 File Name:")
    print(document.metadata.get("file_name"))

    print("\n📍 File Path:")
    print(document.metadata.get("file_path"))

    print("\n📄 File Type:")
    print(document.metadata.get("file_type"))

    # --------------------------------------------------
    # 2. Document content
    # --------------------------------------------------

    print("\n📝 Content Preview:")
    print(document.text[:300])