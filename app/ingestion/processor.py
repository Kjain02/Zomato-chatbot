import json
import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh;'
                         ' Intel Mac OS X 10_15_4) '
                         ' AppleWebKit/537.36 (KHTML, like Gecko) '
                         ' Chrome/83.0.4103.97 Safari/537.36'}


def get_info(url):
    """ Get Information about the restaurant from URL """
    
    global headers
    webpage = requests.get(url, headers=headers, timeout=3)
    html_text = BeautifulSoup(webpage.text, 'html.parser')  # Use html.parser
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


def clean_reviews(html_text):
    """ Cleans and collect the review from the html """
    
    reviews = html_text.find_all('div', type='application/ld+json')[1]
    print(reviews)
    reviews = json.loads(reviews.string)['reviews']
    data = []
    for review in reviews:
        data.append({
            'author': review['author'],
            'review_url': review['url'],
            'description': review['description'],
            'rating': review['reviewRating']['ratingValue']
        })
    return data


def get_reviews(url, max_reviews, sort='new'):
    """ Get all Reviews from the passed url """
    
    global headers
    
    # Set variables for scraping
    max_reviews = max_reviews // 5
    if sort == 'popular':
        sort = '&sort=rd'
    elif sort == 'new':
        sort = '&sort=dd'
    
    reviews = []
    prev_data = None
    rn = ""
    
    # Collect reviews
    for i in range(1, max_reviews + 1):
        link = url + f"/reviews?page={i}{sort}"
        webpage = requests.get(link, headers=headers, timeout=5)
        html_text = BeautifulSoup(webpage.text, 'html.parser')  # Use html.parser
        # print(html_text.text)
        rn = html_text.head.find('title').text
        data = clean_reviews(html_text)
        if prev_data == data:
            break
        reviews.extend(data)
        prev_data = data
    
    restaurant_name = rn[rn.find("User Reviews"):-1]
    return reviews


def save_json(file_name, data):
    """ Save data as JSON """
    
    if not os.path.exists("Restaurants"):
        os.makedirs("Restaurants")
    
    with open(f"Restaurants/{file_name}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_restaurant_info(url_list, max_reviews=10, sort='popular', save=True, file_name="Restaurant_Data"):
    """ Get Restaurant Information from all urls passed and their reviews """
    
    restaurant_data = []
    for url in url_list:
        # Get restaurant info
        info = get_info(url)
        
        # Get reviews for the restaurant
        reviews = get_reviews(url, max_reviews, sort)
        
        # Merge the data
        data = info
        data['reviews'] = reviews
        
        restaurant_data.append(data)
    
    # Save as JSON if needed
    if save:
        save_json(file_name, restaurant_data)
    
    return restaurant_data


if __name__ == "__main__":
    urls = [
        "https://www.zomato.com/bangalore/voosh-thalis-bowls-1-bellandur-bangalore",
        "https://www.zomato.com/bangalore/flying-kombucha-itpl-main-road-whitefield-bangalore",
        "https://www.zomato.com/bangalore/matteo-coffea-indiranagar"
    ]
    
    data = get_restaurant_info(urls, max_reviews=10, save=True, file_name="Restaurant_Information")
    print(data)  # This will print the final combined data
