import random 
import torch
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

text_chunks_and_embeddings_df = pd.read_csv("text_chunks_and_embeddings.csv")
text_chunks_and_embeddings_df["embedding"] = \
text_chunks_and_embeddings_df["embedding"].apply(lambda x: np.fromstring(x.strip('[]'), sep=' ', dtype=np.float32))
print("Shape:",text_chunks_and_embeddings_df.shape)
print("Sample Head...: \n",text_chunks_and_embeddings_df.head())

pages_and_chunks = text_chunks_and_embeddings_df.to_dict(orient="records")
print("Pages & Chunks Count: ",len(pages_and_chunks))
print(random.sample(pages_and_chunks,k=2))

embeddings = torch.tensor(text_chunks_and_embeddings_df["embedding"].to_list(), dtype=torch.float32, device=device)
print("Embeddings Shape: ",embeddings.shape)
print("Sample Embeddings: \n",embeddings[:5])

from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer(model_name_or_path = "all-mpnet-base-v2" , device="mps")


### RAG

## 1. Define the query
query = "macronutrients functions"
print(f"Query: {query}")

## 2. Set embedding for the query
query_embedding = embedding_model.encode(query, convert_to_tensor=True, device=device)

## 3. Get the similarity scores with the dot product
from time import perf_counter as timer
start_time = timer()
# Compute dot product similarity: embeddings @ query_embedding
# embeddings shape: [num_chunks, embedding_dim]
# query_embedding shape: [embedding_dim]
# Result shape: [num_chunks]
similarity_scores = torch.matmul(embeddings, query_embedding)
end_time = timer()
print(f"Time taken: {end_time - start_time} seconds")
#print("Similarity Scores Shape: ",similarity_scores.shape)
#print("Sample Similarity Scores: \n",similarity_scores[:5])

## 4. Get the top k most similar chunks
top_k = 5
top_k_indices = torch.topk(similarity_scores, k=top_k).indices
print("Top k indices: \n",top_k_indices)
print("Top k similarity scores: \n",similarity_scores[top_k_indices])

## 5. Display the actual text chunks (answers)
print("\n" + "="*80)
print("TOP K MOST RELEVANT CHUNKS:")
print("="*80)
for i, idx in enumerate(top_k_indices, 1):
    idx_int = idx.item()  # Convert tensor to Python int
    chunk = pages_and_chunks[idx_int]
    similarity = similarity_scores[idx].item()
    print(f"\n[{i}] Similarity Score: {similarity:.4f}")
    print(f"    Page Number: {chunk.get('page_number', 'N/A')}")
    print(f"    Text Chunk: {chunk.get('sentence_chunk', chunk.get('text', 'N/A'))[:200]}...")  # Show first 200 chars
    print("-"*80)
