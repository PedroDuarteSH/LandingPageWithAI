from llama_cpp import Llama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings

if __name__ == "__main__":
    print("Loading models...")
    print("Loading Qwen model...")
    llm = Llama.from_pretrained(
        repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
        filename="*q8_0.gguf",
        verbose=False
    )
    print("Loading Snowflake model...")
    embeddings = LlamaCppEmbeddings(repo_id="ChristianAzinn/snowflake-arctic-embed-xs-GGUF", verbose=False, filename="snowflake-arctic-embed-xs--Q4_K_S.GGUF")
    
    embeddings.embed_query("Where are you")
    
    question = "Where are you from?"
    
    print("Loading vector store...")
    vector_store = FAISS.load_local(
        "information_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    docs = vector_store.similarity_search("qux")


    results = vector_store.similarity_search(
        question,
        k=3
    )
    
    context = "\n".join([res.page_content for res in results])
    print("Context generated")
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]") 
    
    
    
    # Create a chat template
    
    output = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "I am Pedro Henriques. Ask me anything."},
            {"role": "user", "content": "What's your name?"},
            {"role": "assistant", "content": "My name is Pedro Henriques."},
            {"role": "user", "content": "Where are you from?"},
            {"role": "assistant", "content": "I am from Coimbra, Portugal"},
            {"role": "context", "content": "CONTEXT:" + context},
            {"role": "user", "content": question},
        ]
    )
    print(output)
    