import json
import time

from engine.kgraph2 import generate_pydantic_iter
from engine.repository import clone
from engine.transcriber import transcribe as ts
from engine.vector import (
    ask,
    ask_conv,
    ask_memory,
    generate_embedding,
    load_embedding,
    repository_overview,
    split_doc,
)
from engine.video_processor import extract_audio_from_video
from engine.web import load
from engine.youtube import download

REPO_DOCS_SECTION = [
    {
        "section": "Introducton",
        "instruction": "This section provides an introducton, overview of the project's goals and objectives.",
    },
    {
        "section": "Tech Stack",
        "instruction": "List the technologies and library modules used in the project.",
    },
    {
        "section": "Flow",
        "instruction": "Explain the high-level flow and architecture of the project. Provide mermaid diagram from overview code.",
    },
    {
        "section": "Configuration",
        "instruction": "Detail the configuration settings required for the project.",
    },
    {
        "section": "Usage Instruction",
        "instruction": "Provide step-by-step instructions on how to use the project.",
    },
    {
        "section": "Troubleshooting",
        "instruction": "List how to troubleshoot the project code."
        # "instruction": "List possible issues and their solutions of the code. Issues must be about the code and NOT about the git like branch, changes, check etc.",
    },
]


def status(title, type=None, source=None, status=None, new=False):
    output_path = f"data/db/{title}.json"

    if new:
        with open(output_path, "w") as file:
            json.dump(
                {"title": title, "type": type, "source": source, "status": status},
                file,
            )

    else:
        with open(output_path, "r") as json_file:
            json_data = json.load(json_file)

        if type:
            json_data["type"] = type
        if source:
            json_data["source"] = source
        if status:
            json_data["status"] = status

        with open(output_path, "w") as file:
            json.dump(
                json_data,
                file,
            )


def ask_vector(title, question):
    vector = load_embedding(title)
    return ask(vector, question)


def ask_vector_conv(title, question, conv_id):
    vector = load_embedding(title)
    return ask_conv(vector, question, conv_id)


def ask_vector_memory(title, question, conv_id):
    vector = load_embedding(title)
    return ask_memory(vector, question, conv_id)


def repo_input(url):
    start = time.time()
    title = clone(url)
    # title = "lapisai-query-engine.git"
    status(title, type="repository", source="github", status="started", new=True)

    status(title, status="split_docs")
    split_docs = split_doc(title)

    status(title, status="generate_embedding")
    generate_embedding(title, split_docs)

    status(title, status="summarize")
    vector = load_embedding(title)
    summary = ask(
        vector,
        f"""provide precise and concise summary of the repo {title} in max 5 sentence.""",
    )
    with open(f"data/summary/{title}_brief.txt", "w") as file:
        file.write(summary["answer"])

    vector = load_embedding(title)
    summary = ask(
        vector,
        f"""provide precise summary of the repo {title}. explain as detailed as possible.""",
    )
    with open(f"data/summary/{title}.txt", "w") as file:
        file.write(summary["answer"])

    docs = ""
    for i_section in REPO_DOCS_SECTION:
        instruct = i_section["instruction"]
        section = i_section["section"]
        doc = ask(
            vector,
            f"""provide precise summary of the repo {title} for section {section}.
                  first line should be header (# {section}) bold of {section}.
                  {instruct}
                  style your summary with points or bullet in markdown format, add some creativity.""",
        )
        docs += doc["answer"] + " \n\n"

    with open(f"data/summary/{title}_docs.txt", "w") as file:
        file.write(docs)

    status(title, status="graph")
    generate_pydantic_iter(title)

    status(title, status="done")

    print(title, f"DONE in {time.time()-start}")
    return title


def youtube_input(url):
    video = download(url)
    title = video[:-4]
    status(title, type="video", source="youtube", status="started", new=True)

    status(title, status="video")
    extract_audio_from_video(title)

    status(title, status="transcribe")
    ts(title)

    status(title, status="summarize")
    split_docs = split_doc(title, folder="raw", only=["txt"])
    generate_embedding(title, split_docs)
    vector = load_embedding(title)
    summary = ask(
        vector,
        f"""provide precise and concise summary of the youtube {title} in max 5 sentence.""",
    )
    with open(f"data/summary/{title}_brief.txt", "w") as file:
        file.write(summary["answer"])

    summary = ask(
        vector,
        f"""provide precise summary of the youtube {title}.""",
    )
    with open(f"data/summary/{title}.txt", "w") as file:
        file.write(summary["answer"])

    status(title, status="graph")
    generate_pydantic_iter(title)

    status(title, status="done")

    print(title, "DONE")
    return True


def web_input(url):
    title = load(url)
    status(title, type="text", source="web", status="started", new=True)

    status(title, status="summarize")
    split_docs = split_doc(title, folder="raw", only=["txt"])
    generate_embedding(title, split_docs)
    vector = load_embedding(title)
    summary = ask(
        vector,
        f"""provide precise and concise summary of the article {title} in max 5 sentence.""",
    )
    with open(f"data/summary/{title}_brief.txt", "w") as file:
        file.write(summary["answer"])

    summary = ask(
        vector,
        f"""provide precise summary of the article {title}.""",
    )
    with open(f"data/summary/{title}.txt", "w") as file:
        file.write(summary["answer"])

    status(title, status="graph")
    generate_pydantic_iter(title)

    status(title, status="done")

    print(title, "DONE")
    return True


def repository_overview_update_data():
    repository_overview()

    start = time.time()
    title = "overview_repository"
    # title = "lapisai-query-engine.git"
    status(title, type="repository", source="github", status="started", new=True)

    # status(title, status="split_docs")
    # split_docs = []
    # directory_path = f"data/db"
    # for filename in os.listdir(directory_path):
    #     if filename.endswith(".json"):
    #         file_path = os.path.join(directory_path, filename)

    #         with open(file_path, "r") as file:
    #             json_data = json.load(file)
    #             if json_data.get("status") == "done":
    #                 split_doc = split_doc(title)
    #                 split_docs.append(split_doc)

    status(title, status="summarize")
    vector = load_embedding(title)
    summary = ask(
        vector,
        """provide precise and concise summary all sources in max 5 sentence.""",
    )
    with open(f"data/summary/{title}_brief.txt", "w") as file:
        file.write(summary["answer"])

    vector = load_embedding(title)
    summary = ask(
        vector,
        """provide precise summary of all sources. explain as detailed as possible.""",
    )
    with open(f"data/summary/{title}.txt", "w") as file:
        file.write(summary["answer"])

    docs = ""
    for i_section in REPO_DOCS_SECTION:
        instruct = i_section["instruction"]
        section = i_section["section"]
        doc = ask(
            vector,
            f"""provide precise summary of the repo {title} for section {section}.
                  first line should be header (# {section}) bold of {section}.
                  {instruct}
                  style your summary with points or bullet in markdown format, add some creativity.""",
        )
        docs += doc["answer"] + " \n\n"

    with open(f"data/summary/{title}_docs.txt", "w") as file:
        file.write(docs)

    status(title, status="graph")
    generate_pydantic_iter(title)

    status(title, status="done")

    print(title, f"DONE in {time.time()-start}")
