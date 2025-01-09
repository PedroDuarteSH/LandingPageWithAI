import pandas as pd
import os
import random
from transformers import AutoTokenizer
if __name__ == "__main__":
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    language = "pt"
    file = "data_" + language + ".csv"
    # Open the csv file
    df = pd.read_csv(file, sep=";")

    # Should dataframe with 2 columns: question and answer
    # Create a list of questions and answers
    questions = df["question"].tolist()
    answers = df["answer"].tolist()
    
    # Create a list of conversations with the format:
    # [{"role": "user", "content": question}, {"role": "system", "content": answer}, ...]
    # Each conversation should have a random number between 1 and 10 messages
    conversations_df = pd.DataFrame(columns=["text", "starting_question", "labels"])

    num_pairs = len(questions)
    for k in range(10):
        for i in range(num_pairs):
            if language == "en":
                conversation = [{"role": "system", "content": "I am Pedro Henriques. Ask me anything."}]
            else:
                conversation = [{"role": "system", "content": "Eu sou o Pedro Henriques. Pergunte-me qualquer coisa."}]        
            num_messages = random.randint(2, 30)
            for j in range(num_messages):
                if j == 0:
                    question = questions[i]
                    answer = answers[i]
                elif j == num_messages - 1:
                    index = random.randint(0, num_pairs-1)
                    question = questions[index]
                    answer = answers[index]
                    conversation.append({"role": "user", "content": question})
                    label = answer + "<|im_end|>"
                    continue
            
                conversation.append({"role": "user", "content": question})
                conversation.append({"role": "assistant", "content": answer})
            
            
            text = tokenizer.apply_chat_template(
                conversation,
                tokenize=False,
                add_generation_prompt=True
            )
            conversations_df.loc[len(conversations_df)] = {"text": text, "starting_question": questions[i], "labels": label}
    output_file = "conversations_" + language + ".parquet"
    conversations_df.to_parquet(output_file, index=False)
    
    