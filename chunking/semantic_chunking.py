import os
import requests
import fitz # (pymupdf, found this is better than pypdf for our use case, note: licence is AGPL-3.0, keep that in mind if you want to use any code commercially)
from tqdm.auto import tqdm # for progress bars, requires !pip install tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.lang.en import English # see https://spacy.io/usage for install instructions

nlp = English()

# Add a sentencizer pipeline, see https://spacy.io/api/sentencizer/
nlp.add_pipe("sentencizer")

# Get PDF document
pdf_path = "human-nutrition-text.pdf"

# Download PDF if it doesn't already exist
if not os.path.exists(pdf_path):
  print("File doesn't exist, downloading...")

  # The URL of the PDF you want to download
  url = "https://pressbooks.oer.hawaii.edu/humannutrition2/open/download?type=pdf"

  # The local filename to save the downloaded file
  filename = pdf_path

  # Send a GET request to the URL
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
      # Open a file in binary write mode and save the content to it
      with open(filename, "wb") as file:
          file.write(response.content)
      print(f"The file has been downloaded and saved as {filename}")
  else:
      print(f"Failed to download the file. Status code: {response.status_code}")
else:
  print(f"File {pdf_path} exists.")
  
  
def text_formatter(text: str) -> str:
    """Performs minor formatting on text."""
    cleaned_text = text.replace("\n", " ").strip() # note: this might be different for each doc (best to experiment)

    # Other potential text formatting functions can go here
    return cleaned_text

# Open PDF and get lines/pages
# Note: this only focuses on text, rather than images/figures etc
def open_and_read_pdf(pdf_path: str) -> list[dict]:
    """
    Opens a PDF file, reads its text content page by page, and collects statistics.

    Parameters:
        pdf_path (str): The file path to the PDF document to be opened and read.

    Returns:
        list[dict]: A list of dictionaries, each containing the page number
        (adjusted), character count, word count, sentence count, token count, and the extracted text
        for each page.
    """
    doc = fitz.open(pdf_path)  # open a document
    pages_and_texts = []
    for page_number, page in tqdm(enumerate(doc)):  # iterate the document pages
        text = page.get_text()  # get plain text encoded as UTF-8
        text = text_formatter(text)
        pages_and_texts.append({"page_number": page_number - 41,  # adjust page numbers since our PDF starts on page 42
                                "page_char_count": len(text),
                                "page_word_count": len(text.split(" ")),
                                "page_sentence_count_raw": len(text.split(". ")),
                                "page_token_count": len(text) / 4,  # 1 token = ~4 chars, see: https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them
                                "text": text})
    
    print(f"Total pages read: {len(pages_and_texts)}")
    return pages_and_texts

def sentence_embedding_generator(pages_and_texts: list[dict], model_name: str = "all-MiniLM-L6-v2") -> list:
    """
    Generate sentence embeddings using a pre-trained SentenceTransformer model.
    """
    for item in tqdm(pages_and_texts):
        item["sentences"] = list(nlp(item["text"]).sents)

        # Make sure all sentences are strings
        item["sentences"] = [str(sentence) for sentence in item["sentences"]]

        # Count the sentences
        item["page_sentence_count_spacy"] = len(item["sentences"])
    
        model = SentenceTransformer(model_name)
        embeddings = model.encode(item["sentences"], show_progress_bar=True)
        item["sentence_embeddings"] = embeddings
    return pages_and_texts

def semantic_chunk(sentences, embeddings, threshold=0.7):
    """
    Split a list of sentences into semantic chunks based on similarity.
    """
    chunks, current_chunk = [], [sentences[0]]
    prev_emb = embeddings[0]

    for i in range(1, len(sentences)):
        sim = cosine_similarity([prev_emb], [embeddings[i]])[0][0]
        if sim > threshold:
            current_chunk.append(sentences[i])
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
        prev_emb = embeddings[i]

    # Append last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    print(f"Created {len(chunks)} semantic chunks with threshold {threshold}")
    return chunks




if __name__ == "__main__":
    # Example usage
    pages_and_chunks = []
    pages_and_texts = open_and_read_pdf(pdf_path=pdf_path)

    print("Loading sentence transformer model...")
    print("Pages and Texts Length: ",len(pages_and_texts))
    pages_and_texts = sentence_embedding_generator(pages_and_texts, model_name="all-MiniLM-L6-v2")
    print("Generated sentence embeddings.")
    for item in tqdm(pages_and_texts):
        sentences = item.get("sentences", [])
        embeddings = item.get("sentence_embeddings", [])

        # Skip empty pages
        if not sentences or not embeddings.any():
            continue

        chunks = semantic_chunk(sentences, embeddings, threshold=0.7)

    for chunk in chunks:
            chunk_dict = {}
            chunk_dict["page_number"] = item["page_number"]
            chunk_dict["sentence_chunk"] = chunk

            # Stats
            chunk_dict["chunk_char_count"] = len(chunk)
            chunk_dict["chunk_word_count"] = len(chunk.split())
            chunk_dict["chunk_token_count"] = len(chunk) / 4

            pages_and_chunks.append(chunk_dict)

    len(pages_and_chunks)
    print("Chunked Pages and their Chunks: ",len(pages_and_chunks))
        
    for page in pages_and_chunks[:2]:  # print first 2 pages' chunks
        print(f"Page Number: {page['page_number']}")
        print(f"Chunk: {page['sentence_chunk']}")
        print(f"Character Count: {page['chunk_char_count']}")
        print(f"Word Count: {page['chunk_word_count']}")
        print(f"Token Count: {page['chunk_token_count']}")
        print("-" * 40)