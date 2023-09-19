import pandas as pd
from .flipkart import (
    scrape_flipkart_products,
)  # Import the Flipkart function from flipkart.py
from .amazon import scrape_amazon_products  # Import the Amazon function from amazon.py


def extract_first_three_words(title):
    words = title.lower().split(" ")
    return " ".join(words[:3])


def combine_data(flipkart_df, amazon_df):
    combined_data = []

    # print("\n\ninfo here\n\n", flipkart_df.info())
    flipkart_df["First Three Words"] = flipkart_df["Title"].apply(
        extract_first_three_words
    )
    amazon_df["First Three Words"] = amazon_df["Title"].apply(extract_first_three_words)

    # print(flipkart_df["First Three Words"])
    # print(amazon_df["First Three Words"])

    # Merge the filtered dataframes based on the 'First Three Words' column
    # combined_df = flipkart_df.merge(amazon_df, on="First Three Words", how="inner")
    combined_df = flipkart_df.merge(
        amazon_df,
        left_on="First Three Words",
        right_on="First Three Words",
        how="inner",
    )

    # Rename columns to avoid conflicts
    combined_df = combined_df.rename(
        columns={
            "Title_x": "Flipkart_Title",
            "Title_y": "Amazon_Title",
            "Image URL_x":"Image_URL_x",
            "Image URL_flipkart": "Flipkart_Image_URL",
            "Price_flipkart": "Flipkart Price",
            "Price_amazon": "Amazon Price",
            "Image URL_amazon": "Amazon Image URL",
        }
    )

    # print(combined_df)
    return pd.DataFrame(combined_df)


def get_product_data(search_query):
    flipkart_df = scrape_flipkart_products(search_query)
    amazon_df = scrape_amazon_products(search_query)
    combined_df = combine_data(flipkart_df, amazon_df)
    combined_dict = combined_df.to_dict(orient="records")

    return combined_dict








# Example usage:
# search_query = "redmi"

# print("fn calling")


# flipkart_df = scrape_flipkart_products(search_query)
# amazon_df = scrape_amazon_products(search_query)
# print("fp df", flipkart_df)
# print("amazon df")
# print(amazon_df)


# combined_df = combine_data(flipkart_df, amazon_df)
# print(combined_df)
# combined_dict = combined_df.to_dict(orient="records")
# print("combined_df")
# print(combined_dict)

# print(combined_dict)
