# generator.py

import cohere
from app.config import Config
from .retriever import retrieve_documents

cohere_client = cohere.Client(Config.COHERE_API_KEY)

# Store chat history globally or manage it via session/user state if needed
chat_history = []

def generate_answer(query: str) -> str:
    """Generate an answer using Cohere's language model based on retrieved context."""
    context_docs = retrieve_documents(query)
    context = "\n\n".join(context_docs)


    # Add current context as a system message for grounding
    chat_history.insert(0, {"role": "system", "message": (
        "You are a helpful assistant that answers user questions about restaurants "
        "based only on provided context including restaurant name, menu, pricing, and dietary options. "
        "Do not fabricate information outside the given context."
    )})
    # Add the user query to chat history
    chat_history.append({"role": "user", "message": query})

    prompt = (
        "You are a helpful assistant that answers user questions about restaurants "
        "based on menu, pricing, and dietary options. Do Not add additional information from out of context.\n\n"
        f"Context:\n{context}\n\n"
        f"User Question: {query}\n"
        "Answer:"
    )

    response = cohere_client.chat(
        model="command-r-plus",  # You can use other available models from Cohere
        chat_history=chat_history,
        message=prompt,
        max_tokens=300,
        temperature=0.7
    )

    # Add assistant response to history
    chat_history.append({"role": "chatbot", "message": response.text.strip()})

    return response.text.strip()

