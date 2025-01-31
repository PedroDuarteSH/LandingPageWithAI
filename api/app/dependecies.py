from fastapi import Depends, HTTPException
from fastapi import Request
import os
from llama_cpp import Llama
from loguru import logger
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings
from config import Settings
class LoadResources():
    def __init__(self, settings: Settings):
        self.settings : Settings = settings
        self.embeddings_model : LlamaCppEmbeddings = self.__load_embedding_model()
        self.vector_store : FAISS = self.__load_local_faiss_index()
        self.model : Llama = self.__load_model()
        
    def __load_embedding_model(self) -> LlamaCppEmbeddings:
        logger.info("Load Embedding model")
        try:
            return LlamaCppEmbeddings(
                repo_id=self.settings.embeddings_model_name, 
                filename=self.settings.embeddings_file_name
            )
        except Exception as e:
            logger.error(f"Failed to load Embeddings_model from {self.settings.embeddings_model_name}. Error: {e}")
    
    def __load_local_faiss_index(self) -> FAISS:
        try:
            vector_store = FAISS.load_local(
                self.settings.faiss_index_path, self.embeddings_model, allow_dangerous_deserialization=True
            )
            return vector_store
        except Exception as e:
            logger.error(f"Failed to load FAISS index from {self.settings.faiss_index_path}. Error: {e}")
            raise e
    
    def __load_model(self) -> Llama:
        logger.info("Loading LlamaCPP model")
        try:
            if os.path.exists(self.settings.model_name):
                return Llama(model_path=self.settings.model_name)
            else:
                return Llama.from_pretrained(
                    repo_id=self.settings.model_name,
                    filename=self.settings.model_file_name,
                    verbose=False
                )
        except Exception as e:
            logger.error(f"Failed to load model from {self.settings.model_name}. Error: {e}")
            raise e
    
        

def get_embedding_model(request: Request):
    if not hasattr(request.app.state, "embedding_model"):
        raise HTTPException(status_code=500, detail="Embedding model not initialized")
    return request.app.state.embedding_model

def get_vector_store(request: Request):
    if not hasattr(request.app.state, "vector_store"):
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    return request.app.state.vector_store

def get_model(request: Request):
    if not hasattr(request.app.state, "model"):
        raise HTTPException(status_code=500, detail="Model not initialized")
    return request.app.state.model

