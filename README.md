# Zomato-chatbot

# Zomato Chatbot

A conversational AI chatbot that answers questions about restaurants using retrieval-augmented generation (RAG). It provides information like menus, prices, cuisines, and other restaurant-specific details by extracting and embedding content from the Zomato website.

---

## Features

- Extracts restaurant information from Zomato using restaurant names and cities.
- Stores and embeds data using Postgres and Pinecone vector database.
- Retrieves contextually relevant data to answer queries.
- Uses Cohere LLMs to generate accurate, context-aware responses.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Kjain02/Zomato-chatbot.git
cd zomato-chatbot

# Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Add Environment Variables
Create a .env file or add your API keys in app/config.py:

COHERE_API_KEY

PINECONE_API_KEY

PINECONE_ENVIRONMENT

PINECONE_INDEX_NAME


# How to Chat
    # Navigate to:
    app/scripts/run_chatbot.py

    # Run the chatbot script:
    python run_chatbot.py

# Enter your query (e.g., “What is the cost for two at Big Chill, Delhi?”)

# Restaurant Data Extraction
    # Restaurant data is listed in:
        ingestion/queries.txt

    # To extract data for a new restaurant:

        # Add the restaurant name and city (comma-separated) in queries.txt
            Big Chill, Delhi
            Pizza Hut, Bangalore
        # On next run, new entries are auto-processed and appended to:
            ingestion/restaurant_info.txt
    # Already processed entries are tracked in:
        ingestion/processed_queries.txt