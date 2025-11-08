from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(model_name_or_path="all-mpnet-base-v2", device="mps")

sentences = [
    "The Sentences Transformers library provides an easy and open-source way to create embeddings.",
    "Sentences can be embedded one by one or as a list of strings.",
    "Embeddings are one of the most powerful concepts in machine learning!",
    "Learn to use embeddings well and you'll be well on your way to being an AI engineer."
]


embeddings = embedding_model.encode(sentences)
embedding_dict = dict (zip (sentences, embeddings))
for sentence, embedding in embedding_dict.items():
    
    print(f"Sentence: {sentence}")
    print(f"Embedding: {embedding}")
    print("-"*100)
    print(len(embedding))