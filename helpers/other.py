from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTextEncoding

if __name__ == "__main__":
    embeddings_model = HuggingFaceEmbeddings(model_name="Snowflake/snowflake-arctic-embed-xs")
    new_vector_store = FAISS.load_local(
        "faiss_index", embeddings_model, allow_dangerous_deserialization=True
    )

    model_name = "Qwen/Qwen2.5-0.5B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )

    question = "Who are you?"


    tokenizer = AutoTokenizer.from_pretrained(model_name)

        
    docs = new_vector_store.similarity_search("qux")


    results = new_vector_store.similarity_search(
        question,
        k=3
    )
    
    context = " ".join([res.page_content for res in results])
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")
    
    
        
    messages = [{"role" : "system", "content" : "Do not generate new information. Only use information given in the CONTEXT."}, 
            {"role": "user", "content": "CONTEXT: " + context},
            {"role": "user", "content": question},   
    ]
    
    
    print(results)

    documents = [{"title":res.metadata["question"], "text":res.page_content} for res in results]


    
    
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

    print(generated_ids)
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=False)[0]

print(response)