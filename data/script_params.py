import os
from dataclasses import dataclass, field
from typing import Optional




@dataclass
class VectorDatabaseGenerationArguments:
    dataset_path: str = field(
        default="C:/Users/pedro/Desktop/Self Projects/LandingPageWithAI/data/data.csv", metadata={"help": "Path to the dataset."}
    )
    
    embedding_model: str = field(
        default="Snowflake/snowflake-arctic-embed-xs", metadata={"help": "Embedding model to use."}
    )