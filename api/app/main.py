from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import Settings
from vector_store.faiss import load_local_faiss_index
from llama_cpp import Llama
from langchain_community.embeddings import LlamaCppEmbeddings
import os
from pathlib import Path
from loguru import logger
import uvicorn
#import ngrok
resources = {}



APPLICATION_PORT = 5000
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    # Load the ML model
    #ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    #ngrok.forward(addr=APPLICATION_PORT, labels=NGROK_EDGE, proto="labeled")
    
    
    
    resources["embedding_model"] = LlamaCppEmbeddings(repo_id=settings.embeddings_model_name, filename=settings.embeddings_file_name)
    resources["vector_store"] = load_local_faiss_index(index_path=settings.faiss_index_path, embeddings_model=resources["embedding_model"])
    if os.path.exists(settings.model_name):
        resources["model"] = Llama(model_path=settings.model_name)
    else:
        resources["model"] = Llama.from_pretrained(
            repo_id=settings.model_name,
            filename=settings.model_file_name,
            verbose=False
        )
    
    yield
    # Clean up the ML models and release the resources
    logger.info("Tearing Down Ngrok Tunnel")
    #ngrok.disconnect()
    logger.info("Clearing Models in Use")
    resources.clear()


app = FastAPI(lifespan=lifespan)



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




@app.post("/new_message")
async def new_message(session_id: str, message: str):
    # Get the conversation from the session_id
    # Append the new message to the conversation
    # Run the LLM model on the conversation to generate a response
    # Return the response
    
    return {"message": message}


@app.post("/delete_conversation")
async def delete_conversation(session_id: str):

    return {"message": "Conversation deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=APPLICATION_PORT, reload=True)
    