from llama_cpp import Llama
from script_params import VectorDatabaseGenerationArguments
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import LlamaCppEmbeddings

import pandas as pd





if __name__ == "__main__":
    #parser = HfArgumentParser([VectorDatabaseGenerationArguments])
    #datapipeline_args: VectorDatabaseGenerationArguments = parser.parse_args_into_dataclasses()[0]
    datapipeline_args = VectorDatabaseGenerationArguments(dataset_path="data/vector.csv")
    embedder = LlamaCppEmbeddings(repo_id="ChristianAzinn/snowflake-arctic-embed-xs-GGUF", verbose=False, filename="snowflake-arctic-embed-xs--Q4_K_S.GGUF", embedding = True)

    
 
    # Load dataset
    df = pd.read_csv(datapipeline_args.dataset_path, sep=";")


    # Create vector database
    vector_database = FAISS(
        embedding_function=embedder,
        index=faiss.IndexFlatIP(len(embedder.embed_query("test"))),
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )
    
    
    
    documents = [
        Document(
            page_content=row["information"],
            metadata={"index": idx},
        )
        for idx, row in df.iterrows()
    ]
    
  
    
    # Use metadata 'index' as ids
    ids = [doc.metadata["index"] for doc in documents]
   

    vector_database.add_documents(documents=documents, ids=ids)

    vector_database.save_local("information_index")

   