from pinecone import Pinecone, ServerlessSpec
from app.config import Config  # make sure this loads your .env properly
from app.embeddings import get_embedding
from uuid import uuid4
import re
import os

# Initialize Pinecone client
pc = Pinecone(api_key=Config.PINECONE_API_KEY)

# Connect or create the index
index_name = Config.PINECONE_INDEX_NAME

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  # or whatever your embedding dimension is
        metric="cosine",
        spec=ServerlessSpec(
            cloud=Config.PINECONE_CLOUD,     # e.g. 'aws'
            region=Config.PINECONE_REGION    # e.g. 'us-west-2'
        )
    )

index = pc.Index(index_name)


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


def upsert_restaurant_data(filepath):
    """Reads data from a file and pushes to Pinecone."""
    records = []
    restaurants = load_text_data(filepath)

    for text in restaurants:
        # Extract restaurant name from the text
        restaurant_match = re.search(r"Restaurant Name:\s*(.*)", text)
        restaurant_name = restaurant_match.group(1).strip() if restaurant_match else "Unknown"
        
        text_chunks = chunk_text(text, max_len=1000, overlap=200)
        for text in text_chunks:
            embedding = get_embedding(text)
            metadata = {
                "restaurant_name": restaurant_name
            }
            records.append({
                "id": str(uuid4()),
                "values": embedding,
                "metadata": metadata
            })

    if records:
        index.upsert(records)
        print(f"Uploaded {len(records)} records to Pinecone.")
    else:
        print("No valid records found.")


    # data_file_path = os.path.join("synthetic_restaurant_reviews.txt")  # Make sure this path is correct
    upsert_restaurant_data("F:\\zz\\Zomato-chatbot\\app\\ingestion\\restaurant_info.txt")

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

