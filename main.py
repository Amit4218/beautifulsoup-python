from bs4 import BeautifulSoup
import requests



link = requests.get("https://books.toscrape.com/catalogue/category/books_1/index.html")

soup = BeautifulSoup(link.text, "html.parser")


def main():

    # fetching elements which is required for scraping

    name_element = soup.find_all("h3")   

    rating_elements = soup.find_all('article', class_="product_pod")    

    image_elements = soup.find_all('div', class_="image_container")    

    price_element = soup.find_all('div', class_="product_price")      
  


    # looping through the elements 

    for elements in name_element, rating_elements, image_elements, price_element:

            title = elements.find('a')['title']  # Find the 'a' tag and get the 'title' attribute

            print(title)

            image = elements.find('img')['src']
            image = image.replace("../../../","")

            print(image)

            price = elements.find('p').text

            instock = elements.find('p', class_="instock availability").text
            instock = instock.replace(" ","")

            print(instock)

            rating = elements.find('p')['class']

            print(rating)


main()




        


























# elements = soup.find_all('article', class_="product_pod")

# for element in elements:

#     title = elements.find('a')['title']  # Find the 'a' tag and get the 'title' attribute
#     print(title)

#     image = elements.find('img')['src']
#     image = image.replace("../../../","")
#     print(image)




# name_element = soup.find_all("h3")

# for book_name in name_element:
#     title = book_name.find('a')['title']  # Find the 'a' tag and get the 'title' attribute
#     print(title)


# image_elements = soup.find_all('div', class_="image_container")

# for image_url in image_elements:

#     image = image_url.find('img')['src']
#     image = image.replace("../../../","")
#     # print(image)


# price_element = soup.find_all('div', class_="product_price")

# for prices in price_element:
#     price = prices.find('p').text
#     # print(price)

#     instock = prices.find('p', class_="instock availability").text
#     instock = instock.replace(" ","")
#     print(instock)

# rating_elements = soup.find_all('article', class_="product_pod")

# for ratings in rating_elements:
#     rating = ratings.find('p')['class']

#     print(rating)