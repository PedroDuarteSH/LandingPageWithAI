from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings

def load_local_faiss_index(index_path: str, embeddings_model: LlamaCppEmbeddings):
    try:
        
        vector_store = FAISS.load_local(
            index_path, embeddings_model, allow_dangerous_deserialization=True
        )
        return vector_store
    except Exception as e:
        raise RuntimeError(f"Failed to load FAISS index from {index_path}. Error: {e}")