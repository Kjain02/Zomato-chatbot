import cohere
from app.config import Config

cohere_client = cohere.Client(Config.COHERE_API_KEY)

def get_embedding(text: str):
    """Generate embeddings using Cohere API."""
    response = cohere_client.embed(texts=[text], model="embed-english-v3.0", input_type="search_document")
    return response.embeddings[0]
