import requests
from bs4 import BeautifulSoup
import pandas as pd


def generate_url(search_query):
    base_url = "https://www.flipkart.com/search?q="
    search_query = search_query.replace(" ", "%20")
    url = base_url + search_query
    return url


def scrape_flipkart_products(search_query):
    search_url = generate_url(search_query)
    print(search_url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    titles = soup.find_all("div", class_="_4rR01T")
    images = soup.find_all("img", class_="_396cs4")
    specifications_div = soup.find_all("div", class_="fMghEO")
    prices = soup.find_all("div", class_="_30jeq3 _1_WHN1")

    products_data = []

    for title, image, spec_div, price in zip(
        titles, images, specifications_div, prices
    ):
        product_title = title.text
        image_url = image["src"]
        specifications = spec_div.find_all("li", class_="rgWa7D")
        product_price = price.text

        product_dict = {
            "Title": product_title,
            "Image URL": image_url,
            "Specifications": [spec.get_text(strip=True) for spec in specifications],
            "Price": product_price,
        }

        products_data.append(product_dict)

    df = pd.DataFrame(products_data)

    # print("\n\n info in fn /n/n", df.info())

    return df


# Example usage
# print(scrape_flipkart_products("laptop").info())
