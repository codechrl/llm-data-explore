from os import environ, makedirs

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route import ask, data, input
from setting import setting
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    title="Hackathon Team 5's Swagger UI",
    version="0.1.0",
    description=""" Welcome to the Swagger UI documentation for the Hackathon Team 5. """,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(SessionMiddleware, secret_key=setting.FASTAPI_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/healthz", status_code=200, tags=["Health Check"])
async def health_check():
    return "Hello from Hackathon Team 5!"


app.include_router(
    input.router,
    prefix="/api/engine",
    tags=["Engine"],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    data.router,
    prefix="/api/data",
    tags=["Data"],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    ask.router,
    prefix="/api/ask",
    tags=["Ask"],
    responses={404: {"description": "Not found"}},
)


@app.on_event("startup")
async def startup():
    print("INFO:     Export OpenAI API KEY")
    environ["OPENAI_API_KEY"] = setting.OPENAI_API_KEY
    makedirs("data", exist_ok=True)
    makedirs("data/db", exist_ok=True)
    makedirs("data/summary", exist_ok=True)
    makedirs("data/raw", exist_ok=True)
    makedirs("data/video", exist_ok=True)
    makedirs("data/audio", exist_ok=True)
    makedirs("data/repository", exist_ok=True)
    makedirs("data/graph", exist_ok=True)
    makedirs("data/data_store", exist_ok=True)

    print("INFO:     Export Langsmith API KEY")
    # environ["LANGCHAIN_TRACING_V2"] = "true"
    # environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    # environ["LANGCHAIN_API_KEY"] = setting.LANGSMITH_API_KEY
    # environ["LANGCHAIN_PROJECT"] = setting.LANGSMITH_PROJECT
    # Client()

    # await db.open_pool()


@app.on_event("shutdown")
async def shutdown():
    # await db.close_pool()
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
