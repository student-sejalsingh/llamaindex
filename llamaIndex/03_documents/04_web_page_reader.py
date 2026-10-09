import html2text
import requests
from llama_index.core import Document


# Wikipedia page to load
page_title = "Binary search algorithm"
url = "https://en.wikipedia.org/wiki/Binary_search_algorithm"

# Wikipedia requires clients to identify themselves with a descriptive
# user-agent. Include a contact address when using this outside a local demo.
headers = {
    "User-Agent": "LlamaIndex learning example/1.0 (local educational script)"
}

response = requests.get(
    "https://en.wikipedia.org/w/api.php",
    params={
        "action": "parse",
        "page": page_title,
        "prop": "text",
        "format": "json",
        "formatversion": "2",
        "redirects": "1",
    },
    headers=headers,
    timeout=30,
)
response.raise_for_status()

payload = response.json()
try:
    article_html = payload["parse"]["text"]
except (KeyError, TypeError) as error:
    raise RuntimeError("Wikipedia did not return article content") from error

documents = [
    Document(
        text=html2text.html2text(article_html),
        metadata={"url": url},
    )
]


print("\nNumber of Documents:", len(documents))


for i, document in enumerate(documents):

    print("\n" + "=" * 70)
    print(f"Document {i + 1}")
    print("=" * 70)

    print("\nMetadata:")
    print(document.metadata)

    print("\nWebpage Content:")
    print(document.text[:2000])

    print("\n...")