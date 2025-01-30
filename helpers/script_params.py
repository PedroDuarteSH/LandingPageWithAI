import os
from dataclasses import dataclass, field
from typing import Any, Optional




@dataclass
class VectorDatabaseGenerationArguments:
    dataset_path: str = field(
        default="./data/vector.csv", metadata={"help": "Path to the dataset."}
    )
    
    embedding_model: str = field(
        default="Snowflake/snowflake-arctic-embed-xs", metadata={"help": "Embedding model to use."}
    )
    
    model: str = field(
        default="HuggingFaceTB/SmolLM2-135M-Instruct", metadata={"help": "Model to use."}
    )


    
@dataclass
class TokenizationArguments:
    dataset_path: str = field(
        default="./data/conversations.parquet", metadata={"help": "Path to the dataset."}
    )
    
    tokenizer: str = field(
        default="Qwen/Qwen2.5-0.5B-Instruct", metadata={"help": "Model to use."}
    )
    
    max_number_of_train_tokens: Optional[int] = field(
        default=4096, metadata={"help": "Max length of the tokenizer."}
    )
    model_max_length: Optional[int] = field(
        default=4096, metadata={"help": "Max length of the model."}
    )
    tokenizer_dir: Optional[str] = field(
        default="./tokenizer", metadata={"help": "Path to the tokenizer."}
    )
    tokenized_data: Optional[str] = field(
        default="./data/conversations_tokenized.parquet", metadata={"help": "Path to the tokenized data."}
    )
    

@dataclass
class FinetuneArguments:
    model_name: str = field(
        metadata={"help": "Name/Path to the model."},
        default="Qwen/Qwen2.5-0.5B-Instruct"
    )
    tokenizer_dir: str = field(
        metadata={"help": "Path to the tokenizer."},
        default="./tokenizer"
    )
    tokenized_data: str = field(
        metadata={"help": "Path to the tokenized data."},
        default="./data/conversations_tokenized.parquet"
    )
    output_dir: str = field(
        metadata={"help": "Output directory."},
        default='./model/model'
    )
    
    seed: int = field(
        metadata={"help": "Seed."},
        default=42
    )
    early_stopping_patience: int = field(default=2, metadata={"help": "early stopping patience."})
    max_gen_length: Optional[int] = field(default=512, metadata={"help": "The max number of tokens to generate."})
    num_cpus: Optional[int] = field(
        default=os.cpu_count(),
        metadata={"help": "Number of cpus to run the data processing. Default value equals to the number of cores."},
    )
    validation_frac: Optional[float] = field(
        default=0.3, metadata={"help": "Fraction of training dataset to be used for validation."}
    )
    model_max_length: Optional[int] = field(default=512, metadata={"help": "Maximum input length."})
    masking_seed: Optional[int] = field(default=42, metadata={"help": "Seed to compute the masks."})
    truncation: Optional[bool] = field(default=False, metadata={"help": "When True it truncates the input."})
    batch_eval_metrics: Optional[Any] = field(default=None, metadata={"help": "Number of batches to compute the evaluation metrics."})