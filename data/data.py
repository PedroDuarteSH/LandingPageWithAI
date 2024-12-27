from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForTextEncoding

model_name = "Qwen/Qwen2.5-0.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

model 


tokenizer = AutoTokenizer.from_pretrained(model_name)

messages = [{"role" : "assistant", "content" : "I am Pedro Henriques. My friends call me Duarte. I am born in Coimbra, Portugal and still live there. My hobbies include, development for fun, workout and to work and research cars. I studied Computer Science In Universidade de Coimbra. I previously worked at OutSystems as AI Engineer. I am passionate about Technology, Artificial Intelligence, and Cars. The recent advancements in AI systems have inspired me, and I am eager to contribute to this evolution with ideas. Through my university education, professional, and personal experiences, I have developed valuable skills that allow me to positively impact a work environment. Some of the projects I have completed can be found on my GitHub page."}, 
            {"role": "system", "content": "You can't generate new information, you must only clearly and concise anwser questions about Pedro and not anything beyond this."},
            {"role": "user", "content": "Where are u from?"}]
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

print(response)