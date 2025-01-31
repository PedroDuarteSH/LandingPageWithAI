from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional
from sqlalchemy import Text

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_question: str = Field(default=None, sa_type=Text)  # Large text
    model_answer: str = Field(default=None, sa_type=Text)   # Large text
    model_context: str = Field(default=None, sa_type=Text)  