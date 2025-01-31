from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import Settings
from loguru import logger
import uvicorn
from db import database
import ngrok
from dependecies import LoadResources
from routes import ai


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

@app.post("/")
async def root(question: str):
    new_vector_store = resources["vector_store"]
    model = resources["model"]
        
    results = new_vector_store.similarity_search_with_relevance_scores(
        question,
        k=3,
    )
    print(results)
    
    
    context = "\n".join([res[0].page_content for res in results])
    print(context)
        
    messages = [
        {"role": "system", "content": "I am Pedro Henriques. Ask me anything."},
        {"role" : "system", "content" : "Only use information given in the context. Do not generate new information. Small answers are preferred."},
        {"role" : "context", "content" : "CONTEXT:\n" + context},
        {"role": "user", "content": question}
    ]
    
    output = model.create_chat_completion(messages)["choices"][0]["message"]
    
    
    return {"message": output, "context" : context}






@app.post("/delete_conversation")
async def delete_conversation(session_id: str):

    return {"message": "Conversation deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
    