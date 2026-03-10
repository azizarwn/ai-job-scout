from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.database import ChatSession
from app.models.engine import get_db

session_router = APIRouter(prefix="/chat-sessions")


@session_router.post("/")
async def create_session(db_session: AsyncSession = Depends(get_db)):
    new_session = ChatSession()
    db_session.add(new_session)
    await db_session.commit()
    await db_session.refresh(new_session)
    return new_session
