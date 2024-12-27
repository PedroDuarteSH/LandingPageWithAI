from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

if __name__ == "__main__":
    embeddings_model = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-xs")
    new_vector_store = FAISS.load_local(
        "faiss_index", embeddings_model, allow_dangerous_deserialization=True
    )

    docs = new_vector_store.similarity_search("qux")


    results = new_vector_store.similarity_search(
        "Estás solteira não estavas?",
        k=2
    )
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")