import sqlite3
import csv

# Connect to database
connection = sqlite3.connect("data_pipeline/books.db")

cursor = connection.cursor()


# Read cleaned CSV file
with open(
    "data_pipeline/cleaned_books.csv",
    "r",
    encoding="utf-8"
) as file:

    data = csv.DictReader(file)

    rows = list(data)


print("Number of books:", len(rows))


# Add categories
categories = []

for row in rows:

    category = row["category"]

    if category not in categories:
        categories.append(category)


for i in range(len(categories)):

    cursor.execute(
        """
        INSERT OR IGNORE INTO categories
        (category_id, category)
        VALUES (?, ?)
        """,
        (i + 1, categories[i])
    )


# Add books
for i in range(len(rows)):

    row = rows[i]

    category = row["category"]

    cursor.execute(
        "SELECT category_id FROM categories WHERE category = ?",
        (category,)
    )

    category_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO books
        (book_id, title, price_gbp, rating, in_stock, price_inr, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            i + 1,
            row["title"],
            float(row["price_gbp"]),
            int(row["rating"]),
            int(row["in_stock"] == "True"),
            float(row["price_inr"]),
            category_id
        )
    )


connection.commit()


# Check number of books
cursor.execute("SELECT COUNT(*) FROM books")

count = cursor.fetchone()[0]

print("Books inserted:", count)


connection.close()

print("Data inserted successfully.")