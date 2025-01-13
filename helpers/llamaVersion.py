from llama_cpp import Llama


if __name__ == "__main__":
    llm = Llama.from_pretrained(
        repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
        filename="*q8_0.gguf",
        verbose=False
    )
    
    embeddings_model = Llama.from_pretrained(repo_id="ChristianAzinn/snowflake-arctic-embed-xs-GGUF", verbose=False, filename="snowflake-arctic-embed-xs--Q4_K_S.GGUF", embedding = True)
    
    question = "Tell me about your hobbies?"
    
    embeddings = embeddings_model.create_embedding("Hello, world!")
    print(embeddings)
    exit()
    # Create a chat template
    
    output = llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "I am Pedro Henriques. Ask me anything."},
            {"role": "context", "content": "CONTEXT:"},
            
            {"role": "user", "content": question}
        ],
        max_new_tokens=512,
    )
    print(output)
    