from dependecies import get_vector_store
from fastapi import Depends
from db.schemas import Message

def find_context(message: Message, vector_store = Depends(get_vector_store)) -> str:
    question = message.question
    results = vector_store.similarity_search_with_relevance_scores(question, k=3)
    context = "\n".join([res[0].page_content for res in results])

    return context