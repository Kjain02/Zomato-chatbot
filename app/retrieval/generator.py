# generator.py

import cohere
from app.config import Config
from .retriever import retrieve_documents

cohere_client = cohere.Client(Config.COHERE_API_KEY)

def generate_answer(query: str) -> str:
    """Generate an answer using Cohere's language model based on retrieved context."""
    context_docs = retrieve_documents(query)
    context = "\n\n".join(context_docs)

    prompt = (
        "You are a helpful assistant that answers user questions about restaurants "
        "based on menu, pricing, and dietary options. Do Not add additional information from out of context.\n\n"
        f"Context:\n{context}\n\n"
        f"User Question: {query}\n"
        "Answer:"
    )

    response = cohere_client.chat(
        model="command-r-plus",  # You can use other available models from Cohere
        message=prompt,
        max_tokens=150,
        temperature=0.7
    )

    return response.text.strip()

