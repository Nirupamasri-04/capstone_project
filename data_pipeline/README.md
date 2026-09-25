# Data Pipeline

## Overview

This module builds a complete data pipeline for book catalog data from `books.toscrape.com`.

The workflow includes:

- Web scraping
- Data cleaning
- GBP to INR currency conversion
- SQLite database creation
- SQL querying
- Pandas analysis
- SQL and Pandas result comparison

## Pipeline

```text
books.toscrape.com
        ↓
Web Scraping
        ↓
raw_books.csv
        ↓
Data Cleaning and Enrichment
        ↓
cleaned_books.csv
        ↓
SQLite Database
        ↓
books.db
        ↓
SQL Queries
        ↓
Pandas Analysis
        ↓
SQL vs Pandas Comparison
Results
100 books were scraped from the first five pages.
Book price, rating, and availability data were cleaned and converted into appropriate formats.
GBP prices were converted to INR using a fixed rate of 1 GBP = 105.50 INR.
The cleaned data was stored in a normalized SQLite database.
SQL queries demonstrated SELECT, WHERE, ORDER BY, LIMIT, DISTINCT, BETWEEN, and JOIN.
Equivalent SQL and Pandas operations were compared.
The SQL JOIN result and the equivalent pd.merge() result matched.
Files
data_pipeline/
├── README.md
├── scrape_books.py
├── clean_books.py
├── database.py
├── queries.py
├── compare_data.py
├── raw_books.csv
├── cleaned_books.csv
└── books.db
How to Run

From the project root:

python data_pipeline/scrape_books.py
python data_pipeline/clean_books.py
python data_pipeline/database.py
python data_pipeline/queries.py
python data_pipeline/compare_data.py

Run the scripts in this order because each stage uses the output from the previous stage.

Design Decisions

The pipeline separates scraping, cleaning, database loading, querying, and comparison into individual scripts. The raw and cleaned datasets are stored separately so that the original scraped data is preserved.

SQLite was used as a lightweight relational database, while Pandas was used to verify the SQL analysis through equivalent operations.