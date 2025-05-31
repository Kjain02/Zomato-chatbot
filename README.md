# Zomato Chatbot

A conversational AI chatbot that answers questions about restaurants using retrieval-augmented generation (RAG). It provides information like menus, prices, cuisines, and other restaurant-specific details by extracting and embedding content from the Zomato website.

## Features

- Extracts restaurant information from Zomato using restaurant names and cities
- Stores and embeds data using Postgres and Pinecone vector database
- Retrieves contextually relevant data to answer queries
- Uses Cohere LLMs to generate accurate, context-aware responses

## Project Structure

```
rag-chatbot/
├── app/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── database.py            # PostgreSQL connection and ORM models
│   ├── pinecone_client.py     # Pinecone initialization and operations
│   ├── embeddings.py          # Functions to generate embeddings
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── scraper.py         # Web scraping logic for restaurant data
│   │   └── processor.py       # Data cleaning and preprocessing
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── retriever.py       # Logic to retrieve relevant documents
│   │   └── generator.py       # LLM-based answer generation
│   └── api/
│       ├── __init__.py
│       └── routes.py          # API endpoints using FastAPI or Flask
├── scripts/
│   ├── ingest_data.py         # Script to run data ingestion pipeline
│   └── run_chatbot.py         # Script to start the chatbot
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   └── test_api.py
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── README.md
└── Dockerfile                 # For containerization (optional)
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Kjain02/Zomato-chatbot.git
cd zomato-chatbot
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
COHERE_API_KEY=your_cohere_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
PINECONE_INDEX_NAME=your_pinecone_index_name
```

## Usage

### Running the Chatbot

1. Navigate to the scripts directory:
```bash
cd app/scripts
```

2. Run the chatbot:
```bash
python run_chatbot.py
```

3. Enter your query (e.g., "What is the cost for two at Big Chill, Delhi?")

### Adding New Restaurant Data

1. Restaurant data is managed in `ingestion/queries.txt`

2. To extract data for a new restaurant:
   - Add the restaurant name and city (comma-separated) in `queries.txt`:
     ```
     Big Chill, Delhi
     Pizza Hut, Bangalore
     ```
   - New entries are automatically processed and appended to `rag_chatbot/restaurant_info.txt`
   - Already processed entries are tracked in `ingestion/processed_queries.txt`