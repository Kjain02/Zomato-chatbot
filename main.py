from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
from app.retrieval.generator import generate_answer  # Use your existing function to generate chatbot answers

# Initialize FastAPI app
app = FastAPI()

# Enable CORS so the frontend (like React app) can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Allow requests from any origin 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the request schema for chatbot questions (used in /chat endpoint)
class Query(BaseModel):
    question: str

# Define the request schema for saving restaurant data (used in /save_query endpoint)
class QueryData(BaseModel):
    restaurant_name: str
    location: str

# Endpoint to handle chatbot queries
@app.post("/chat")
async def chat(query: Query):
    # Use your generator function to create an answer based on the user's question
    response = generate_answer(query.question)
    return {"answer": response}

# Endpoint to save restaurant information and trigger ingestion script
@app.post("/save_query")
async def save_query(data: QueryData):
    # Clean up inputs
    restaurant_name = data.restaurant_name.strip()
    location = data.location.strip()

    # Debugging output — prints to terminal
    print(restaurant_name)
    print(location)

    # Check if both fields are provided
    if restaurant_name and location:
        # Append the restaurant info to a file (used for future data ingestion)
        with open("app/ingestion/queries.txt", "a") as f:
            f.write(f"{restaurant_name}, {location}\n")

        try:
            # Run the ingestion script to update vector DB [pinecone]
            subprocess.run(["python", "app/ingestion/main.py"], check=True)
        except subprocess.CalledProcessError as e:
            # If the script fails, returning error message
            return {"success": False, "message": f"Script error: {e}"}

        # Success response
        return {"success": True, "message": "Query saved and script executed"}
    else:
        # If required fields are missing then
        return {"success": False, "message": "Missing restaurant name or location"}