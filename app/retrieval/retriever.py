# retrieval/retriever.py
import cohere
from app.config import Config
from app.pinecone_client import index
from app.embeddings import get_embedding

cohere_client = cohere.Client(Config.COHERE_API_KEY)

def retrieve_documents(query: str, top_k: int = 5) -> list:
    """Retrieve top_k most relevant documents from Pinecone based on query."""
    response = cohere_client.embed(texts=[query], model="embed-english-v3.0", input_type="search_query")
    query_embedding = response.embeddings[0]
    result = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    documents = [match['metadata']['text'] for match in result['matches']]
    return documents
