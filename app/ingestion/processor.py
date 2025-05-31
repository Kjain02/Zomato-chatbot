import json
import os

def json_to_text(json_file, txt_file):
    if not os.path.exists(json_file):
        print(f"{json_file} not found.")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(txt_file, 'w', encoding='utf-8') as f:
        for restaurant, details in data.items():
            f.write(f"Restaurant Name: {restaurant}\n")
            if 'scraped' in details and details['scraped'].get('status') == 'success':
                found = details['scraped'].get('found_sections', {})
                f.write(f"Overview:\n{found.get('overview', 'N/A')}\n")
                f.write(f"Menu:\n{found.get('menu', 'N/A')}\n")
                f.write(f"Cuisines Stuff:\n{found.get('cuisines_stuff', 'N/A')}\n")
            else:
                f.write("Data scraping failed or not available.\n")
            f.write("="*60 + "\n\n")

    print(f"Text data saved to {txt_file}")

# if __name__ == "__main__":
json_path = "F:\zomato\\rag_chatbot\\scraping_results.json"
txt_path = "F:\zomato\\rag_chatbot\\restaurant_info.txt"
json_to_text(json_path, txt_path)
