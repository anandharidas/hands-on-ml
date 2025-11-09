#Requires !pip install PyMu
import fitz # PyMuPDF
from tqdm.auto import tqdm
import random
import pandas as pd
from spacy.lang.en import English


def text_formatter(text:str)->str :
    cleaned_text = text.replace("\n", " ").strip()
    return cleaned_text
    
def parse_pdf(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages_and_texts = []
    for page_number, page in enumerate(tqdm(doc)):
       text = page.get_text()
       text = text_formatter(text)
       pages_and_texts.append({"page_number": page_number - 41,
                        "page_char_count" : len(text),
                        "page_word_count" : len(text.split(" ")),
                        "page_sentence_count_raw" : len(text.split(". ")),
                        "page_token_count" : len(text)/4,  #token = ~4 chars
                        "text": text})
    return pages_and_texts
   
pages_and_texts = parse_pdf("datasets/nutrition/human-nutrition-text.pdf")
#print(random.sample(pages_and_texts,k=1))
nlp = English()
nlp.add_pipe("sentencizer")
for item in tqdm(pages_and_texts):
    item["sentences"] = nlp(item["text"]).sents
    
    #make sure all the sentences are strings
    item["sentences"] = [str(sentence) for sentence in item["sentences"]]
 
    #count sentences per page
    item["page_sentence_count_spacy"] = len(item["sentences"])
    

#define split size to turn groups of sentences into chunks
num_sentence_chunk_size = 2
#print(random.sample(pages_and_texts,k=2))

def split_list(input_list: list, slize_size: int) -> list[list[str]]:
    return [input_list[i:i+slize_size] for i in range(0, len(input_list), slize_size)]

for item in tqdm(pages_and_texts):
    item["sentence_chunks"] = split_list(item["sentences"], num_sentence_chunk_size)
    item["num_chunks"] = len(item["sentence_chunks"])
    
df = pd.DataFrame(pages_and_texts)
print(df.head())
print(df.describe().round(2))

import re
pages_and_chunks = []
for item in tqdm(pages_and_texts):
    for sentence_chunk in item["sentence_chunks"]:
        chunk_dict = {}
        chunk_dict["page_number"] = item["page_number"]
        
        #join senteences together into a paragrahp-like structure, aka a chunk (so they are a single string)
        joined_sentence_chunk = "".join(sentence_chunk).replace("  "," ").strip()
        joined_sentence_chunk = re.sub(r'\.([A-Z])',r'. \1',joined_sentence_chunk)
        chunk_dict["sentence_chunk"] = joined_sentence_chunk
        
        #Get stats about the chunk
        chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
        chunk_dict["chunk_word_count"] = len( [words for words in joined_sentence_chunk.split(" ")])
        chunk_dict["chunk_token_count"] = len(joined_sentence_chunk)/4 
        pages_and_chunks.append(chunk_dict)

print("Pages & Chunks Count: ",len(pages_and_chunks))
print(random.sample(pages_and_chunks,k=2))

df = pd.DataFrame(pages_and_chunks)
print(df.head())
print(df.describe().round(2))

# show ranom chunks with under 30 toekns in length
min_token_length = 30
for row in df[df["chunk_token_count"] < min_token_length].sample(n=5).iterrows():
    print(f"Chunk token count: {row[1]['chunk_token_count']} | Text: {row[1]['sentence_chunk']}")


pages_and_chunks_over_min_token_len = df[df["chunk_token_count"] > min_token_length].to_dict(orient="records")
print("Pages & Chunks Over Min Token Length: ",len(pages_and_chunks_over_min_token_len))
print(random.sample(pages_and_chunks_over_min_token_len,k=2))

from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer(model_name_or_path = "all-mpnet-base-v2" , device="mps")

embedding_model.to("mps")

for item in tqdm(pages_and_chunks_over_min_token_len):
    item["embedding"] = embedding_model.encode(item["sentence_chunk"])

text_chunks_and_embeddings_df = pd.DataFrame(pages_and_chunks_over_min_token_len)
embedding_store_path = "text_chunks_and_embeddings.csv"
text_chunks_and_embeddings_df.to_csv(embedding_store_path,index=False)

text_chunks_and_embeddings_df_loaded = pd.read_csv(embedding_store_path)
print(text_chunks_and_embeddings_df_loaded.head())
print(text_chunks_and_embeddings_df_loaded.describe().round(2))

