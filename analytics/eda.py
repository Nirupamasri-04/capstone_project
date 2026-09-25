import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("titanic")

df.to_csv("analytics/titanic.csv", index=False)

print(df.head())

print(df.shape)

print(df.info())

print(df.describe())

print(df.isnull().sum())

missing = df.isnull().sum()
missing_percentage = (missing / len(df)) * 100

print(missing_percentage[missing_percentage > 0])

df["age"] = df["age"].fillna(df["age"].median())

df = df.dropna(subset=["embarked"])

df["deck"] = df["deck"].astype("object")
df["deck"] = df["deck"].fillna("missing")

df = df.dropna(subset=["embark_town"])

print(df.isnull().sum())

print(df.shape)

plt.hist(df["age"])
plt.xlabel("Age")
plt.ylabel("Number of passengers")
plt.title("Age Distribution")
plt.show()

plt.boxplot(df["age"])
plt.ylabel("Age")
plt.title("Age Box Plot")
plt.show()

plt.hist(df["fare"])
plt.xlabel("Fare")
plt.ylabel("Number of passengers")
plt.title("Fare Distribution")
plt.show()

plt.boxplot(df["fare"])
plt.ylabel("Fare")
plt.title("Fare Box Plot")
plt.show()

Q1_age = df["age"].quantile(0.25)
Q3_age = df["age"].quantile(0.75)

IQR_age = Q3_age - Q1_age

lower_age = Q1_age - 1.5 * IQR_age
upper_age = Q3_age + 1.5 * IQR_age

age_outliers = df[
    (df["age"] < lower_age) |
    (df["age"] > upper_age)
]

print(len(age_outliers))

Q1_fare = df["fare"].quantile(0.25)
Q3_fare = df["fare"].quantile(0.75)

IQR_fare = Q3_fare - Q1_fare

lower_fare = Q1_fare - 1.5 * IQR_fare
upper_fare = Q3_fare + 1.5 * IQR_fare

fare_outliers = df[
    (df["fare"] < lower_fare) |
    (df["fare"] > upper_fare)
]

print(len(fare_outliers))

print(df["fare"].mean())

print(df["fare"].median())

print(df["fare"].mode()[0])

survival_sex = df.groupby("sex")["survived"].mean()
print(survival_sex)

survival_class = df.groupby("pclass")["survived"].mean()
print(survival_class)

survival_sex_class = df.groupby(
    ["sex", "pclass"]
)["survived"].mean()

print(survival_sex_class)

columns = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

correlation = df[columns].corr()

print(correlation)

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation,
    annot=True
)

plt.title("Correlation Heatmap")
plt.show()

survival_sex = df.groupby("sex")["survived"].mean()

survival_sex.plot(kind="bar")

plt.xlabel("Sex")
plt.ylabel("Survival rate")
plt.title("Survival Rate by Sex")
plt.show()

survival_class = df.groupby("pclass")["survived"].mean()

survival_class.plot(kind="bar")

plt.xlabel("Passenger Class")
plt.ylabel("Survival rate")
plt.title("Survival Rate by Passenger Class")
plt.show()

survival_sex_class = df.groupby(
    ["sex", "pclass"]
)["survived"].mean()

survival_sex_class.plot(kind="bar")

plt.xlabel("Sex and Passenger Class")
plt.ylabel("Survival rate")
plt.title("Survival Rate by Sex and Passenger Class")
plt.show()

sns.scatterplot(
    data=df,
    x="age",
    y="fare",
    hue="survived"
)

plt.xlabel("Age")
plt.ylabel("Fare")
plt.title("Age, Fare and Survival")
plt.show()

df["age_standard"] = (
    df["age"] - df["age"].mean()
) / df["age"].std()

df["fare_standard"] = (
    df["fare"] - df["fare"].mean()
) / df["fare"].std()

print("Mean:", df["age_standard"].mean())
print("Standard deviation:", df["age_standard"].std())

print("Mean:", df["fare_standard"].mean())
print("Standard deviation:", df["fare_standard"].std())