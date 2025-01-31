from fastapi import APIRouter, Depends
from pydantic import BaseModel
from db.schemas import Message, Context
from services import context
router = APIRouter()


@router.post("/context")
def process_data(message: Message, context: str = Depends(context.find_context)):
    return Context(session_id=message.session_id, question=message.question, context=context)