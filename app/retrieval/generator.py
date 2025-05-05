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
            )
        }
    )
    # Add the user query to chat history
    chat_history.append({"role": "user", "message": query})

    prompt = (
        "You are a helpful assistant that answers user questions about restaurants. "
        "You have access to data including restaurant name, location, menu items with descriptions "
        "and prices, special features (e.g., vegetarian options, spice levels, allergens), operating " 
        "hours, and contact details\n\n Answer users’ queries clearly and informatively, using only "
        "the information available from your knowledge base."
        '''You can handle questions such as:\n
        “Does The Spicy Spoon in Bangalore have gluten-free options?”
        “What’s the price of Chicken Biryani at Royal Biryani House?”
        “Compare the vegetarian offerings of Green Harvest and Desi Grills.”
        “Which restaurants serve low-spice or dairy-free meals?”'''

        "Always provide helpful, relevant, and concise answers. "
        "If the requested information is not available, politely mention that it’s not in your database."
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

