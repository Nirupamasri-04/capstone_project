import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

base_url = "https://books.toscrape.com/"

books_data = []

for page in range(1, 6):

    if page == 1:
        url = base_url
    else:
        url = urljoin(base_url, "catalogue/page-" + str(page) + ".html")

    print("Scraping page:", page)

    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    print("Books found:", len(books))

    for book in books:

        title = book.select_one("h3 a")["title"]

        price = book.select_one(".price_color").get_text(strip=True)

        rating = book.select_one("p.star-rating")["class"][1]

        availability = book.select_one(
            ".availability"
        ).get_text(" ", strip=True)

        link = book.select_one("h3 a")["href"]

        book_url = urljoin(url, link)

        # Get category
        try:
            book_response = requests.get(book_url, timeout=10)
            book_response.encoding = "utf-8"

            book_soup = BeautifulSoup(
                book_response.text,
                "html.parser"
            )

            breadcrumb = book_soup.select("ul.breadcrumb li")

            if len(breadcrumb) >= 2:
                category = breadcrumb[-2].get_text(strip=True)
            else:
                category = "Unknown"

        except requests.RequestException:
            category = "Unknown"

        books_data.append([
            title,
            price,
            rating,
            availability,
            category
        ])


print("Total books:", len(books_data))


# Save the data
with open(
    "data_pipeline/raw_books.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "title",
        "price",
        "star_rating",
        "availability",
        "category"
    ])

    writer.writerows(books_data)

print("Raw data saved.")