import os
import re
import subprocess

from setting import setting

os.environ["OPENAI_API_KEY"] = setting.OPENAI_API_KEY

REPO_URL = "https://github.com/GovTechSG/developer.gov.sg"  # Source URL
DOCS_FOLDER = "data/repository"  # Folder to check out to
REPO_DOCUMENTS_PATH = ""  # Set to "" to index the whole data folder
DOCUMENT_BASE_URL = "https://www.developer.tech.gov.sg/products/categories/devops/ship-hats"  # Actual URL
DATA_STORE_DIR = "data/data_store"

name_filter = "**/*.md"
name_filter = "**/*.*"
separator = "\n### "
separator = " "  # Thi+s separator assumes Markdown docs from the repo uses ### as logical main header most of the time
chunk_size_limit = 1000
max_chunk_overlap = 20


def run_command_with_output(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True
    )

    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())

    return process.poll()


def convert_path_to_doc_url(doc_path):
    # Convert from relative path to actual document url
    return re.sub(
        f"{DOCS_FOLDER}/{REPO_DOCUMENTS_PATH}/(.*)\.[\w\d]+",
        f"{DOCUMENT_BASE_URL}/\\1",
        str(doc_path),
    )


def clone(url):
    try:
        title = url.split("/")[-1]
        run_command_with_output(
            [f"git clone {transform_github_url(url)} data/repository/{title}"]
        )
        return title
    except Exception as exc:
        print(exc)


def transform_github_url(url):
    # Extract repository path from the URL
    repo_path = url.split("github.com/")[-1]

    # Construct the new clone URL with authentication
    clone_url = (
        f"https://{setting.GITHUB_USER}:{setting.GIHUB_PAT}@github.com/{repo_path}"
    )

    return clone_url
