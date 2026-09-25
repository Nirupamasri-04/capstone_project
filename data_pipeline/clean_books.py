import pandas as pd

df = pd.read_csv("data_pipeline/raw_books.csv")

print("Raw data:")
print(df.head())

print("\nColumns:")
print(df.columns)

df["price_gbp"] = df["price"].str.replace(
    "£", "", regex=False
)

df["price_gbp"] = df["price_gbp"].astype(float)

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

df["rating"] = df["star_rating"].map(rating_map)

df["in_stock"] = df["availability"].str.contains(
    "In stock",
    case=False,
    na=False
)

df["price_gbp"] = df["price_gbp"].fillna(
    df["price_gbp"].median()
)

df["rating"] = df["rating"].fillna(
    df["rating"].median()
)

df["rating"] = df["rating"].astype(int)

df["category"] = df["category"].fillna("Unknown")

gbp_to_inr = 105.50

df["price_inr"] = df["price_gbp"] * gbp_to_inr

print("\nCleaned data:")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nNumber of rows:")
print(len(df))

df.to_csv(
    "data_pipeline/cleaned_books.csv",
    index=False
)

print("\nCleaned data saved.")