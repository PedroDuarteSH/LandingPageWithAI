from fastapi import FastAPI, Request
from sse_starlette import EventSourceResponse  # Correct import after installing sse-starlette

import asyncio
from contextlib import asynccontextmanager
from config import Settings
from loguru import logger
import uvicorn
from db import database
import ngrok
from dependecies import LoadResources
from routes import ai
import json

APPLICATION_PORT = 5000
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    print(settings)
    try:
        if settings.use_ngrok:
            logger.info("Creating Ngrok Instance")
            ngrok.set_auth_token(settings.ngrok_auth_token)
            ngrok.forward(addr=settings.application_port, labels=settings.ngrok_edge, proto="labeled")
        
        resources = LoadResources(settings)
        
        
        app.state.embeddings_model = resources.embeddings_model
        app.state.vector_store = resources.vector_store
        app.state.model = resources.model
        
        logger.info("Connecting to database")
        database.create_db_and_tables()
        yield
    except Exception as e:
        logger.error(f"Error during resourse setup: {e}")
        raise e
    finally:
        if settings.use_ngrok:
            logger.info("Tearing Down Ngrok Tunnel")
            ngrok.disconnect()
        logger.info("Clearing remaining Resources")
        app.state.model.close()


app = FastAPI(lifespan=lifespan)

app.include_router(ai.router, prefix="/ai", tags=["ai"])


# This endpoint will handle POST requests and stream data back to the client using SSE
@app.post("/stream")
async def stream(request: Request):
    # Get the question from the POST body
    body = await request.json()
    print(body)
    
    messages = body.get("messages")
    question = messages[len(messages) - 1]["content"]
    if not question:
        return {"error": "Question is required"}

    # Asynchronous generator function to stream data to the client
    async def event_stream():
        # Perform similarity search (you can replace this with your actual code)
        new_vector_store = app.state.vector_store
        model = app.state.model

        # Perform similarity search using the question (can be replaced with your actual logic)
        results = new_vector_store.similarity_search_with_relevance_scores(question, k=3)

        # Format the context from the results
        context = "\n".join([res[0].page_content for res in results])
    
        default_messages = [{"role": "system", "content": "I am Pedro Henriques. Ask me anything. Only use information given in the context. Do not generate new information. Small answers are mandatory."}]
        # Create chat completion with streaming enabled
        print(default_messages + messages + [{"role" : "context", "content" : "CONTEXT:\n" +  context}])
        
        response = model.create_chat_completion(default_messages + messages + [{"role" : "system", "content" : "CONTEXT:\n" +  context}], stream=True)
        
        # Stream each part of the response to the client
        for chunk in response:
            output = json.dumps(chunk["choices"][0])
            yield f"{output}"  # This is the SSE format for each chunk

    # Return the response using EventSourceResponse to stream the data to the client
    return EventSourceResponse(event_stream())





@app.post("/delete_conversation")
async def delete_conversation(session_id: str):

    return {"message": "Conversation deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
    