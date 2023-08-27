from engine import (
    repo_input,
    repository_overview_update_data,
    web_input,
    youtube_input,
)
from fastapi import APIRouter, BackgroundTasks

router = APIRouter()

VIDEO_PATH = "./data/video/"
AUDIO_PATH = "./data/audio/"
WEB_PATH = "./data/web/"
TRANSCRIBE_PATH = "./data/transcribe/"


@router.post("/repository", status_code=201)
async def repository(
    background_tasks: BackgroundTasks,
    background: bool = False,
    url: str = "https://github.com/XQuisite-AI/lapisai-query-engine.git",
):
    if background:
        background_tasks.add_task(repo_input, url)
        return {"message": "Operations to in the background"}
    else:
        return repo_input(url)


@router.post("/repository/overview", status_code=201)
async def repository_overview_update(
    background_tasks: BackgroundTasks,
    background: bool = False,
):
    if background:
        background_tasks.add_task(repository_overview_update_data)
        return {"message": "Operations to in the background"}
    else:
        return repository_overview_update_data()


@router.post("/youtube", status_code=201)
async def youtube(
    background_tasks: BackgroundTasks,
    background: bool = False,
    url: str = "https://www.youtube.com/watch?v=V7z7BAZdt2M&pp=ygUKZm90b2dyYXBoeQ%3D%3D",
):
    if background:
        background_tasks.add_task(youtube_input, url)
        return {"message": "Operations to in the background"}
    else:
        return youtube_input(url)


@router.post("/web", status_code=201)
async def web(
    background_tasks: BackgroundTasks,
    background: bool = False,
    url: str = "https://en.wikipedia.org/wiki/Large_language_model",
):
    if background:
        background_tasks.add_task(web_input, url)
        return {"message": "Operations sent to the background"}
    else:
        return web_input(url)
