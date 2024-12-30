from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_local_faiss_index(index_path: str, embeddings_model: HuggingFaceEmbeddings):
    try:
        
        vector_store = FAISS.load_local(
            index_path, embeddings_model, allow_dangerous_deserialization=True
        )
        return vector_store
    except Exception as e:
        raise RuntimeError(f"Failed to load FAISS index from {index_path}. Error: {e}")