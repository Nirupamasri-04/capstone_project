import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("data_pipeline/books.db")


# Read books table using pandas
books = pd.read_sql(
    "SELECT * FROM books",
    connection
)

print("Books data:")
print(books.head())


# Read JOIN result using pandas
join_data = pd.read_sql(
    """
    SELECT books.title, books.price_gbp, categories.category
    FROM books
    JOIN categories
    ON books.category_id = categories.category_id
    """,
    connection
)

print("\nJOIN result:")
print(join_data.head())


# Read categories table
categories = pd.read_sql(
    "SELECT * FROM categories",
    connection
)


# Do the same JOIN using pandas merge
merge_data = pd.merge(
    books,
    categories,
    on="category_id"
)

print("\nPandas merge result:")
print(
    merge_data[
        ["title", "price_gbp", "category"]
    ].head()
)


# Check whether both results are the same
sql_result = join_data.sort_values("title").reset_index(drop=True)

pandas_result = merge_data[
    ["title", "price_gbp", "category"]
].sort_values("title").reset_index(drop=True)

print("\nAre SQL JOIN and Pandas merge the same?")
print(sql_result.equals(pandas_result))


connection.close()