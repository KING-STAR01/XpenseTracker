from fastapi import FastAPI

from api.api import api_router

app = FastAPI(
    title="Xpense Tracker",
    version="0.1.0",
    description="Track All Your Expenses in One Place with Telegram Bot",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

app.include_router(api_router)

@app.get("/")
def hello():
    return {"hello": "world"}


