from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import EMBEDDINGS_MODEL_NAME, FAISS_INDEX_PATH, MODEL_NAME
from langchain_huggingface import HuggingFaceEmbeddings
from vector_store.faiss import load_local_faiss_index
from transformers import AutoModelForCausalLM, AutoTokenizer


resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    resources["embedding_model"] = HuggingFaceEmbeddings(model_name = EMBEDDINGS_MODEL_NAME)
    resources["vector_store"] = load_local_faiss_index(index_path=FAISS_INDEX_PATH, embeddings_model=resources["embedding_model"])
    resources["model"] =  AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto", device_map="auto")
    resources["tokenizer"] = AutoTokenizer.from_pretrained(MODEL_NAME)
    
    yield
    # Clean up the ML models and release the resources
    resources.clear()


app = FastAPI(lifespan=lifespan)

@app.post("/")
async def root(question: str):
    new_vector_store = resources["vector_store"]
    model = resources["model"]
    tokenizer = resources["tokenizer"]
        
    results = new_vector_store.similarity_search(
        question,
        k=3
    )
    
    context = " ".join([res.page_content for res in results])
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")
    
        
    messages = [ 
            {"role": "system", "content": context},
            {"role" : "system", "content" : "Only use information given in the context. Do not generate new information. Small answers are preferred."},
            {"role": "user", "content": question},   
    ]
    
    
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return {"message": response}




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