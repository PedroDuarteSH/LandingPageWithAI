from sentence_transformers import SentenceTransformer
from transformers import pipeline  # For generation

# Load models
retriever = SentenceTransformer("Snowflake/snowflake-arctic-embed-xs")
generator = pipeline("text2text-generation", model="t5-base")  # Or any other generative model

# Encode corpus
documents = [
    "My name is Pedro Henriques",
    "I am from Coimbra, Portugal",
    "I’m fascinated by AI’s ability to process and understand natural language."
]
document_embeddings = retriever.encode(documents)

# Query
query = "How does your passion for AI and technology drive your growth?"
query_embedding = retriever.encode([query], prompt_name="query")

# Compute similarities
import numpy as np
scores = np.dot(query_embedding, np.array(document_embeddings).T)

# Retrieve top-k documents
k = 1
top_k_indices = np.argsort(scores[0])[-k:][::-1]
retrieved_docs = [documents[i] for i in top_k_indices]

# Generate response
context = " ".join(retrieved_docs)
print("Retrieved Documents:", context)   
