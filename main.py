from pymongo import MongoClient  # importing agent from client
import pandas as pd  # importing pandas to write csv file
from bs4 import BeautifulSoup  # for parsing and scraping the site
import requests  # to get requests permission from the page
import datetime  # to keep track of when the data was created


link = requests.get("https://books.toscrape.com/catalogue/category/books_1/index.html")  # getting the html form the page
soup = BeautifulSoup(link.text, "html.parser")  # parsing the page


# Function for creating a CSV file to store the data
def dataToCsv(titles, images, ratings, instocks, prices):
    # Creating a structure
    Title_columns = {
        "Book Names": titles,
        "Book Prices": prices,
        "Image Links": images,
        "Availability": instocks,
        "Book Rating": ratings
    }

    data = pd.DataFrame(Title_columns)
    print(data)

    # Save the data into a CSV file
    data.to_csv("books_data.csv", index=False)
    print("Data has been successfully written to 'books_data.csv'")


# Function for sending the data to the database
def database(titles, images, ratings, instocks, prices):
    client = MongoClient("connection string")

    db = client.beautiful_soup_test

    for title, image, rating, instock, price in zip(titles, images, ratings, instocks, prices):
        post = {
            "Book name": title,
            "Image link": image,
            "Rating": rating,
            "Price": price,
            "Availability": instock,
            "date": datetime.datetime.now(tz=datetime.timezone.utc),
        }

        posts = db.posts
        post_id = posts.insert_one(post).inserted_id

    print("Data sending complete")
    return post_id


def main():
    # Fetching elements required for scraping
    name_elements = soup.find_all("h3")
    rating_elements = soup.find_all('article', class_="product_pod")
    image_elements = soup.find_all('div', class_="image_container")
    price_elements = soup.find_all('div', class_="product_price")

    # Lists to store the scraped data
    titles = []
    images = []
    prices = []
    instocks = []
    ratings = []

    # Looping through the elements
    for book in name_elements:
        title = book.find('a')['title']
        titles.append(title)

    for image in image_elements:
        img_src = image.find('img')['src']
        full_img_url = "https://books.toscrape.com/" + img_src.replace("../../../", "")
        images.append(full_img_url)

    for price in price_elements:
        price_text = price.find('p').text.strip()
        prices.append(price_text)

    for stock in rating_elements:
        instock_text = stock.find('p', class_="instock availability").text.strip()
        instocks.append(instock_text)

    for rating in rating_elements:
        rating_class = rating.find('p')['class']
        # Assuming the rating class format is like 'star-rating Three'
        ratings.append(rating_class[1])

    # Calling functions with the collected data
    dataToCsv(titles, images, ratings, instocks, prices)
    database(titles, images, ratings, instocks, prices)


# Run the main function to start scraping and storing data
main()
