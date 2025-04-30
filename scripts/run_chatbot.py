import sys
import os

# if os.path.isdir("f:\\zomato\\rag_chatbot\\app"):
#     print("Folder exists")
# else:
#     print("Folder does not exist")

# Add the project root (rag_chatbot) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# print("Current sys.path:", sys.path)
from app.retrieval.generator import generate_answer



from app.retrieval.generator import generate_answer

query = "Suggest restaurants with price range less than 20?"
response = generate_answer(query)
print(response)
