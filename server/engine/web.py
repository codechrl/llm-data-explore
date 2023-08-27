import os

from langchain.document_loaders import WebBaseLoader


def load(url, output_path="data/raw"):
    loader = WebBaseLoader(url)
    data = loader.load()

    title = data[0].metadata.get("title")

    os.makedirs(f"{output_path}/{title}", exist_ok=True)
    output_path = f"{output_path}/{title}/{title}.txt"

    with open(output_path, "w") as file:
        file.write(data[0].page_content)

    return title
