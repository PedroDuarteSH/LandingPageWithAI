from transformers import HfArgumentParser
from script_params import VectorDatabaseGenerationArguments

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

import pandas as pd
import os
from pathlib import Path


def get_embedding_size(embeddings_model: HuggingFaceEmbeddings) -> int:
    """Get the size of the embeddings."""
    return embeddings_model._client.get_sentence_embedding_dimension()


if __name__ == "__main__":
    parser = HfArgumentParser([VectorDatabaseGenerationArguments])
    datapipeline_args: VectorDatabaseGenerationArguments = parser.parse_args_into_dataclasses()[0]
    
    embeddings_model = HuggingFaceEmbeddings(model_name = datapipeline_args.embedding_model)
    
    # Load dataset
    df = pd.read_csv(datapipeline_args.dataset_path, sep=";")


    # Create vector database
    vector_database = FAISS(
        embedding_function=embeddings_model,
        index=faiss.IndexFlatIP(get_embedding_size(embeddings_model)),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    documents = [
        Document(
            page_content=row["answer"],
            metadata={"index": idx, "question": row["question"]},
        )
        for idx, row in df.iterrows()
    ]
    
    docs_question = [
        Document(
            page_content=row["question"],
            metadata={"index": idx, "answer": row["answer"]},
        )
        for idx, row in df.iterrows()
    ]
    
    # Use metadata 'index' as ids
    ids = [doc.metadata["index"] for doc in docs_question]
   

    vector_database.add_documents(documents=documents, ids=ids)


    vector_database.save_local("faiss_index")

   