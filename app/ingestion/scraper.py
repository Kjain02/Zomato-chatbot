import json
import requests
from bs4 import BeautifulSoup

# Headers for web scraping
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

def get_info(url):
    """ Get Information about the restaurant from URL """
    
    global headers
    webpage = requests.get(url, headers=headers, timeout=3)
    html_text = BeautifulSoup(webpage.text, 'html.parser')  # Use html.parser here
    info = html_text.find_all('script', type='application/ld+json')[1]
    info = json.loads(info.string)
    
    data = {
        "type": info['@type'],
        "name": info['name'],
        "url": info['url'],
        "opening_hours": info['openingHours'],
        "street": info['address']['streetAddress'],
        "locality": info['address']['addressLocality'],
        "region": info['address']['addressRegion'],
        "postal_code": info['address']['postalCode'],
        "country": info['address']['addressCountry'],
        "latitude": info['geo']['latitude'],
        "longitude": info['geo']['longitude'],
        "telephone": info['telephone'],
        "price_range": info['priceRange'],
        "payment_accepted": info['paymentAccepted'],
        "image": info['image'],
        "serves_cuisine": info['servesCuisine'],
        # "rating_value": info['aggregateRating']['ratingValue'],
        # "rating_count": info['aggregateRating']['ratingCount']
    }
    return data

def save_to_json(file_name, data):
    """ Save data to JSON file """
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_restaurant_info(url_list, save=True, file_name="restaurants.json"):
    """ Get Restaurant Information from all urls passed """
    data = []
    for url in url_list:
        restaurant_info = get_info(url)
        data.append(restaurant_info)

    # Save to JSON file if save is True
    if save:
        save_to_json(file_name, data)

    return data

if __name__ == "__main__":
    # Sample list of URLs to scrape restaurant data from
    urls = [
        "https://www.zomato.com/bangalore/voosh-thalis-bowls-1-bellandur-bangalore",
        "https://www.zomato.com/bangalore/flying-kombucha-itpl-main-road-whitefield-bangalore",
        "https://www.zomato.com/bangalore/matteo-coffea-indiranagar"
    ]
    get_restaurant_info(urls)
