import sqlite3

# Connect to the database
connection = sqlite3.connect("data_pipeline/books.db")

cursor = connection.cursor()


# Query 1: Select all books
query1 = """
SELECT *
FROM books
"""

cursor.execute(query1)

result = cursor.fetchall()

print("\nQuery 1: All books")
print(result[:5])


# Query 2: WHERE
query2 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp > 50
"""

cursor.execute(query2)

result = cursor.fetchall()

print("\nQuery 2: Books costing more than £50")
print(result[:5])


# Query 3: ORDER BY and LIMIT
query3 = """
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 5
"""

cursor.execute(query3)

result = cursor.fetchall()

print("\nQuery 3: Five most expensive books")
print(result)


# Query 4: DISTINCT
query4 = """
SELECT DISTINCT category
FROM categories
"""

cursor.execute(query4)

result = cursor.fetchall()

print("\nQuery 4: Different categories")
print(result)


# Query 5: BETWEEN
query5 = """
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 30
"""

cursor.execute(query5)

result = cursor.fetchall()

print("\nQuery 5: Books between £20 and £30")
print(result[:5])


# Query 6: JOIN
query6 = """
SELECT books.title, books.price_gbp, categories.category
FROM books
JOIN categories
ON books.category_id = categories.category_id
"""

cursor.execute(query6)

result = cursor.fetchall()

print("\nQuery 6: Books with their categories")
print(result[:5])


connection.close()