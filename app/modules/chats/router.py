import json

from agents import Agent, RawResponsesStreamEvent, RunItemStreamEvent, Runner
from agents.extensions.memory import SQLAlchemySession
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from openai.types.responses import ResponseFunctionToolCall, ResponseTextDeltaEvent
from sqlmodel import Session

from app.models.engine import engine, get_db
from app.modules.agents.models import llm_model
from app.modules.agents.prompt import SYSTEM_PROMPT
from app.modules.agents.tools import analyze_job_market, search_web
from app.modules.chats.schema import ChatRequest

chat_router = APIRouter(prefix="/chat")


@chat_router.post("/")
async def generate_answer(request: ChatRequest, db_session: Session = Depends(get_db)):
    session = SQLAlchemySession(session_id=request.session_id, engine=engine, create_tables=True)

    agent = Agent(
        "Assistant",
        instructions=SYSTEM_PROMPT,
        model=llm_model,
        tools=[analyze_job_market, search_web],
    )

    runner = Runner.run_streamed(agent, input=request.job_description, session=session)

    async def event_generator():
        async for event in runner.stream_events():
            if isinstance(event, RawResponsesStreamEvent):
                if isinstance(event.data, ResponseTextDeltaEvent):
                    yield f"data: {json.dumps({'type': 'text', 'content': event.data.delta})}\n\n"

            elif isinstance(event, RunItemStreamEvent) and event.name == "tool_called":
                if isinstance(event.item.raw_item, ResponseFunctionToolCall):
                    yield f"data: {
                        json.dumps(
                            {
                                'type': 'tool_call',
                                'content': event.item.raw_item.name,
                                'argument': event.item.raw_item.arguments,
                            }
                        )
                    }\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
