from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.modules.chats.router import chat_router
from app.modules.sessions.router import session_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router)
app.include_router(chat_router)


# Serve index.html at root
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    with open("index.html") as f:
        return HTMLResponse(content=f.read())


@app.get(path="/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
