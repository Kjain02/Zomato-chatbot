import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Handle readline dependency for Windows
if sys.platform == 'win32':
    try:
        import readline
    except ImportError:
        import pyreadline3 as readline

from pinecone import Pinecone, ServerlessSpec
from app.config import Config  # make sure this loads your .env properly
from app.embeddings import get_embedding
from uuid import uuid4
import re
import time
import hashlib



# Initialize Pinecone client
pc = Pinecone(api_key=Config.PINECONE_API_KEY)

# Connect or create the index
index_name = Config.PINECONE_INDEX_NAME

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,  # or whatever your embedding dimension is
        metric="cosine",
        spec=ServerlessSpec(
            cloud=Config.PINECONE_CLOUD,
            region=Config.PINECONE_REGION
        )
    )

index = pc.Index(index_name)




def generate_id(text: str) -> str:
    """Generate a deterministic ID using SHA-256 hash of the text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_text_data(filepath):
    """Loads restaurant blocks from a text file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split each restaurant block
    restaurants = [block.strip() for block in content.split("\n\n") if block.strip()]
    return restaurants

def chunk_text(text, max_len, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_len, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = start + max_len - overlap
    return chunks

EXISTING_IDS_FILE = "F:\\zomato\\rag_chatbot\\existing_vector_ids.txt"

def load_existing_ids():
    if not os.path.exists(EXISTING_IDS_FILE):
        return set()
    with open(EXISTING_IDS_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_existing_ids(ids):
    with open(EXISTING_IDS_FILE, "a") as f:
        for id_ in ids:
            f.write(f"{id_}\n")

def upsert_restaurant_data(filepath):
    # print("jj")
    """Reads data from a file and pushes to Pinecone."""
    records = []
    restaurants = load_text_data(filepath)

    existing_ids = load_existing_ids()
    new_ids = []
    for text in restaurants:
        # Extract restaurant name from the text
        restaurant_match = re.search(r"Restaurant Name:\s*(.*)", text)
        restaurant_name = restaurant_match.group(1).strip() if restaurant_match else "Unknown"
        # print("vv")
        text_chunks = chunk_text(text, max_len=1000, overlap=200)
        
        for text in text_chunks:
            
            vector_id = generate_id(text)
            if vector_id in existing_ids:
                continue  # Skip if already upserted           
            embedding = get_embedding(text)
            time.sleep(1.6)
            metadata = {
                "restaurant_name": restaurant_name,
                "raw_text": text
            }
            records.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })
            new_ids.append(vector_id)

    if records:
        index.upsert(records)
        save_existing_ids(new_ids)
        print(f"Uploaded {len(records)} records to Pinecone.")
    # else:
    #     print("No valid records found.")


    # data_file_path = os.path.join("synthetic_restaurant_reviews.txt")  # Make sure this path is correct
upsert_restaurant_data("F:\\zomato\\rag_chatbot\\restaurant_info.txt")

# # Adding data to Pinecone
# def add_to_pinecone(restaurant_data):
#     vectors = []
#     metadata = []

#     for restaurant in restaurant_data:
#         menu_embedding = get_embedding(restaurant['menu'])
#         vectors.append(menu_embedding)
#         metadata.append({
#             "name": restaurant['name'],
#             "menu": restaurant['menu'],
#             "price_range": restaurant['price_range'],
#             "dietary_options": restaurant['dietary_options']
#         })
    
#     index.upsert(vectors=vectors, metadata=metadata)

# file_path = "synthetic_restaurants.txt"  # change if needed

# with open(file_path, "r", encoding="utf-8") as file:
#     content = file.read()

# print(content)  # Or process it as needed

# documents = [doc.strip() for doc in content.split("\n\n") if doc.strip()]

# # for i, doc in enumerate(documents):
# #     print(f"--- Restaurant #{i+1} ---")
# #     print(doc)
# #     print()

# # Add synthetic data to Pinecone
# add_to_pinecone(documents)

