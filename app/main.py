from fastapi import FastAPI

from app import api_version1_router

app = FastAPI(
    docs_url="/docs",
    title="Order tracking module",
)

app.include_router(api_version1_router)
