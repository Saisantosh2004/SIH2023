import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_amazon_products(search_query):
    # Function to generate Amazon search URL
    def generate_amazon_url(search_query):
        base_url = "https://www.amazon.in/s?k="
        search_query = "+".join(search_query.split())  # Join words with '+'
        return base_url + search_query

    # Function to extract product details from Amazon product container
    def extract_product_details(product):
        title_element = product.find("span", class_="a-size-medium")
        title = title_element.get_text(strip=True) if title_element else "N/A"

        price_element = product.find("span", class_="a-price-whole")
        price = price_element.get_text(strip=True) if price_element else "N/A"

        rating_element = product.find("span", class_="a-icon-alt")
        rating = rating_element.get_text(strip=True) if rating_element else "N/A"

        specs = [
            li.get_text(strip=True)
            for li in product.find_all("li", class_="a-spacing-small")
        ]

        img_element = product.find("img", class_="s-image")
        img_url = img_element["src"] if img_element else "N/A"

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Specifications": specs,
            "Image URL": img_url,
        }

    # Generate Amazon search URL
    amazon_url = generate_amazon_url(search_query)
    # print(amazon_url)

    # Send HTTP GET request to Amazon and parse the HTML content
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all product containers on the page
    product_containers = soup.find_all("div", class_="s-result-item")

    # Extract product details and store them in a list of dictionaries
    product_data_list = [
        extract_product_details(product) for product in product_containers
    ]

    # Create a Pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(product_data_list)

    return df


# Example usage:
# search_query = "laptop"
# result_df = scrape_amazon_products(search_query)
# print(result_df.info())
