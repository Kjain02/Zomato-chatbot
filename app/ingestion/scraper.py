import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse
import time
from app.config import Config
# from dotenv import load_dotenv

# Load API key from .env
# load_dotenv()
SERPAPI_API_KEY = Config.SERPAPI_API_KEY

# Track processed queries
def load_processed_queries(filename="F:\zomato\\rag_chatbot\\app\\ingestion\\processed_queries.txt"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    return set()

def save_processed_query(query, filename="F:\zomato\\rag_chatbot\\app\\ingestion\\processed_queries.txt"):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(query.strip() + "\n")

# Google search using SerpApi
def google_search_serpapi(query, api_key):
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code != 200:
        raise Exception(f"SerpApi request failed with status code {response.status_code}: {response.text}")

    data = response.json()
    if "organic_results" in data and len(data["organic_results"]) > 0:
        for result in data["organic_results"]:
            link = result.get("link", "")
            if "zomato" in link:
                return link
        raise Exception('No search result URL containing "zomato" found')
    else:
        raise Exception("No search results found")

# Scrape sections from Zomato URL
def scrape_website_sections(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url + "/order", headers=headers, timeout=10)
        response.raise_for_status()
        response2 = requests.get(url + "/", headers=headers, timeout=10)
        response2.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        soup2 = BeautifulSoup(response2.text, 'html.parser')

        main = soup.find('main')
        if not main:
            return {"status": "error", "message": "<main> not found", "url": url}
        first_div = main.find('div')
        if not first_div:
            return {"status": "error", "message": "First <div> inside <main> not found", "url": url}
        sections = first_div.find_all('section', recursive=False)
        section2 = sections[1] if len(sections) >= 2 else None
        section5 = sections[3] if len(sections) >= 5 else None

        main2 = soup2.find('main')
        if not main2:
            return {"status": "error", "message": "<main> not found", "url": url}
        first_div2 = main2.find('div')
        if not first_div2:
            return {"status": "error", "message": "First <div> inside <main> not found", "url": url}
        sections2 = first_div2.find_all('section', recursive=False)
        section5_2 = sections2[3] if len(sections2) >= 5 else None

        return {
            "status": "success",
            "file": "extracted_sections.html",
            "found_sections": {
                "overview": section2.get_text(separator=" ", strip=True) if section2 else "",
                "menu": section5.get_text(separator=" ", strip=True) if section5 else "",
                "cuisines_stuff": section5_2.get_text(separator=" ", strip=True) if section5_2 else "",
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "url": url
        }

# Save results to file
def save_results(data, filename="F:\zomato\\rag_chatbot\\scraping_results.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    else:
        existing = {}
    existing.update(data)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=4)
    print(f"Results saved to {filename}")

# Main function
def main():
    if not SERPAPI_API_KEY:
        print("API key not found in environment. Please set SERPAPI_API_KEY in .env")
        return

    input_file = "F:\zomato\\rag_chatbot\\app\ingestion\queries.txt"
    if not os.path.exists(input_file):
        print(f"{input_file} not found.")
        return

    processed = load_processed_queries()
    results = {}

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            query = line.strip()
            if not query or query in processed:
                continue
            try:
                print(f"Processing: {query}")
                url = google_search_serpapi(query, SERPAPI_API_KEY)
                print(f" → Found URL: {url}")
                data = scrape_website_sections(url)
                results[query] = {
                    "url": url,
                    "scraped": data
                }
                save_processed_query(query)
                time.sleep(2)
            except Exception as e:
                print(f"Error with query '{query}': {str(e)}")
                results[query] = {
                    "error": str(e)
                }

    if results:
        save_results(results)
    else:
        print("No new queries to process.")

# if __name__ == "__main__":
main()