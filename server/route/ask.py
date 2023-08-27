from engine import ask_vector, ask_vector_conv, ask_vector_memory
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/vector", status_code=200)
async def ask_vector_store(
    title: str = "lapisai-query-engine.git",
    question: str = "summarize the repo lapisai-query-engine",
    stream: bool = False,
):
    if stream:
        return ask_vector(title, question)
    else:
        return StreamingResponse(
            ask_vector(title, question), media_type="text/event-stream"
        )


@router.get("/vector-conv", status_code=200)
async def ask_vector_store_conv(
    conv_id: str,
    title: str = "lapisai-query-engine.git",
    question: str = "what is query engine",
    stream: bool = False,
):
    if stream:
        return ask_vector_conv(title, question, conv_id)
    else:
        return StreamingResponse(
            ask_vector_conv(title, question, conv_id), media_type="text/event-stream"
        )


@router.get("/vector-memory", status_code=200)
async def ask_vector_store_memory(
    session_id: str,
    title: str = "lapisai-query-engine.git",
    question: str = "what is query engine",
    stream: bool = False,
):
    return ask_vector_memory(title, question, session_id)
    # if stream:
    #     return ask_vector_memory(title, question, session_id)
    # else:
    #     return StreamingResponse(
    #         ask_vector_memory(title, question, session_id),
    #         media_type="text/event-stream",
    #     )
