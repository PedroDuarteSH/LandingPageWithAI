
from transformers import HfArgumentParser, DataCollatorForLanguageModeling, AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from script_params import FinetuneArguments
import os
from datasets import load_dataset

MAX_VALIDATION_SIZE = 5000

class QwenTrainer:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def compute_loss(self, model, inputs, return_outputs=False):
        loss = super().compute_loss(model, inputs, return_outputs)
        outputs = model(**inputs)
        print(loss)
        exit()
        return (loss, outputs) if return_outputs else loss


if __name__ == "__main__":
    parser = HfArgumentParser([FinetuneArguments])
    datapipeline_args: FinetuneArguments = parser.parse_args_into_dataclasses()[0]
    
    model = AutoModelForCausalLM.from_pretrained(
        datapipeline_args.model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    
    tokenizer = AutoTokenizer.from_pretrained(datapipeline_args.tokenizer_dir)
    
    dataset = load_dataset(
        "parquet",
        data_files={"train": datapipeline_args.tokenized_data},
        split="train",
        num_proc=os.cpu_count(),
    )
    
    print(f"Dataset loaded: {len(dataset)}")
    print(dataset)
    
    
    
    # select columns that matter for train
    dataset = dataset.select_columns(["input_ids", "labels_ids"])

    dataset = dataset.rename_column("labels_ids", "labels")  # rename the column to labels
    
    print(f"Dataset loaded: {len(dataset)}")
   
    # use the train/test split to create the validation set
    # compute test size
    if datapipeline_args.validation_frac:
        validation_size = int(len(dataset) * datapipeline_args.validation_frac)
        validation_size = min(MAX_VALIDATION_SIZE, validation_size)

        dataset = dataset.train_test_split(test_size=validation_size, seed=datapipeline_args.seed)
    
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm = False)
     
    
    
    training_args = TrainingArguments(
        output_dir=datapipeline_args.output_dir,
        overwrite_output_dir=True,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=8,
        num_train_epochs=3,
        logging_dir=datapipeline_args.output_dir,
        logging_steps=100,
        save_steps=100,
        save_total_limit=2,
        fp16=True,
    )
    
    
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"] if datapipeline_args.validation_frac else dataset,
        eval_dataset=dataset["test"] if datapipeline_args.validation_frac else None,
        data_collator=data_collator
    )
    
    trainer.train()
    # Save the fine-tuned model
    model.save_pretrained(datapipeline_args.output_dir)
    
    
    