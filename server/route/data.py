import json
import os

from engine.kgraph2 import format
from engine.tree import generate_folder_tree, generate_folder_tree_link
from fastapi import APIRouter, Query

router = APIRouter()

VIDEO_PATH = "./data/video/"
AUDIO_PATH = "./data/audio/"
WEB_PATH = "./data/web/"
TRANSCRIBE_PATH = "./data/transcribe/"
RAW_PATH = "./data/raw/"
SUMMARY_PATH = "./data/summary/"
DB_PATH = "./data/db/"
GRAPH_PATH = "./data/graph/"


@router.get("/", status_code=200)
async def list_items(
    type: str = Query(None, description="Filter by item type"),
    source: str = Query(None, description="Filter by item source"),
):
    result = []

    if os.path.exists(DB_PATH) and os.path.isdir(DB_PATH):
        for filename in os.listdir(DB_PATH):
            if filename.endswith(".json"):
                file_path = os.path.join(DB_PATH, filename)
                with open(file_path, "r") as file:
                    data = json.load(file)
                    if type is not None and data.get("type") != type:
                        continue
                    if source is not None and data.get("source") != source:
                        continue
                    result.append(data)

    return result


@router.get("/graph", status_code=200)
async def graph(title, formatted: bool = False):
    if not formatted:
        path = f"{GRAPH_PATH}{title}.json"
        with open(path, "r") as json_file:
            json_data = json.load(json_file)

        return json_data

    else:
        return format(title)


@router.get("/summary", status_code=200)
async def summary(title):
    path = f"{SUMMARY_PATH}{title}.txt"
    with open(path, "r") as json_file:
        json_data = json_file.read()

    return json_data


@router.get("/summary-brief", status_code=200)
async def summary_brief(title):
    path = f"{SUMMARY_PATH}{title}_brief.txt"
    with open(path, "r") as json_file:
        json_data = json_file.read()

    return json_data


@router.get("/docs", status_code=200)
async def docs(title):
    path = f"{SUMMARY_PATH}{title}_docs.txt"
    with open(path, "r") as json_file:
        json_data = json_file.read()

    return json_data


@router.get("/tree", status_code=200)
async def tree(title, link: bool = False):
    path = f"data/repository/{title}"
    if not link:
        return generate_folder_tree(path, title)
    else:
        return generate_folder_tree_link(path, title, title)


@router.delete("/", status_code=200)
async def delete(title):
    file_path = f"data/db/{title}.json"
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except OSError as e:
        print(f"Error deleting '{file_path}': {e}")

    return True
