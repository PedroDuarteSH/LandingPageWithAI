from transformers import AutoTokenizer, HfArgumentParser, PreTrainedTokenizer
from script_params import TokenizationArguments
import pandas as pd
from transformers.tokenization_utils_base import TruncationStrategy
from typing import Any
from pathlib import Path
import os
from datasets import load_dataset


def tokenize_batch(
    batch: pd.DataFrame,
    tokenizer: PreTrainedTokenizer,
    add_special_tokens: bool = True,
    truncation: bool | str | TruncationStrategy = False,
) -> dict[str, Any]:
    """ Tokenize the conversation"""
    
    label_tokenization = tokenizer(
        batch["labels"],
        add_special_tokens=add_special_tokens,
        truncation=truncation,
    )
    
    text_tokenization = tokenizer(
        batch["text"],
        add_special_tokens=add_special_tokens,
        truncation=truncation,
    )
    
    assert not any(tokenizer.unk_token_id in tokenized_text for tokenized_text in text_tokenization["input_ids"])
    assert not any(tokenizer.unk_token_id in tokenized_label for tokenized_label in label_tokenization["input_ids"])
    
    return {"input_ids": text_tokenization["input_ids"], "labels_ids": label_tokenization["input_ids"]}
if __name__ == "__main__":
    # Test the tokenizer
    parser = HfArgumentParser([TokenizationArguments])
    datapipeline_args: TokenizationArguments = parser.parse_args_into_dataclasses()[0]
    
    tokenizer = AutoTokenizer.from_pretrained(datapipeline_args.tokenizer)
    
    dataset = load_dataset(
        "parquet",
        data_files={"train": datapipeline_args.dataset_path},
        split="train",
        num_proc=os.cpu_count(),
    )
    
   
    dataset = dataset.map(
        tokenize_batch,
        fn_kwargs={"tokenizer": tokenizer, "add_special_tokens": True, "truncation": False},
        batched=True,
        num_proc=os.cpu_count(),
    )
    
    total_instances = len(dataset)

    # filter instances that do not fit in the total number of tokens we are enabling
    if datapipeline_args.max_number_of_train_tokens is not None:
        print(f"Filtering instances with more than {datapipeline_args.max_number_of_train_tokens} tokens")
        dataset = dataset.filter(
            lambda x, max_number_of_train_tokens = datapipeline_args.max_number_of_train_tokens, model_max_length = datapipeline_args.model_max_length: (
                len(x["input_ids"]) <= max_number_of_train_tokens
                and len(x["labels"]) <= model_max_length
            ),
            num_proc=os.cpu_count(),
        )

        print(f"Discarded (#tokens): {total_instances-len(dataset)}/{total_instances}")
        total_instances = len(dataset)

  
    print(f"Discarded (xre): {total_instances-len(dataset)}/{total_instances}")

    print(f"Max number of tokens: {max(len(x['input_ids']) for x in dataset)}")
    # save tokenizer
    tokenizer.save_pretrained(datapipeline_args.tokenizer_dir)

    # save dataset
    dataset.to_parquet(datapipeline_args.tokenized_data)
    
    
    