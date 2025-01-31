from pydantic import BaseModel

class Message(BaseModel):
    session_id: str
    question: str
    

class Context(Message):
    context:str

class ModelResponse(Message):
    context:str
    question: str
    
