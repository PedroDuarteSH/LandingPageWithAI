from pydantic import BaseModel

class Question(BaseModel):
    session_id: str
    question: str
    answer: str