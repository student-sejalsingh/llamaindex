from llama_index.core import SimpleDirectoryReader


# Load only PDF files
documents = SimpleDirectoryReader(
    input_dir="data/01_pdf",
    recursive=True,
    required_exts=[".pdf"],
).load_data()


print("\n📚 Total PDF Documents:", len(documents))


for i, document in enumerate(documents):

    print("\n" + "=" * 70)
    print(f"📄 PDF Document {i + 1}")
    print("=" * 70)

    # File information automatically provided by the reader
    print("\n📁 File Name:")
    print(document.metadata.get("file_name"))

    print("\n📍 File Path:")
    print(document.metadata.get("file_path"))

    print("\n📄 File Type:")
    print(document.metadata.get("file_type"))

    # Extracted PDF text
    print("\n📝 Extracted Text:")
    print(document.text[:1000])

    print("\n...")