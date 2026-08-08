from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="Financial AI Assistant",
    description="RAG-powered Financial AI Assistant with RBAC",
    version="1.0.0"
)

app.include_router(router)