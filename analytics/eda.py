import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# 1. LOAD TITANIC DATASET
# --------------------------------------------------

df = sns.load_dataset("titanic")

print("Dataset loaded successfully.")
print()

print("Dataset information:")
df.info()

print()
print("Dataset shape:")
print(df.shape)

print()
print("Dataset description:")
print(df.describe())

# Save the raw dataset immediately
df.to_csv("analytics/titanic.csv", index=False)

print()
print("Raw dataset saved as analytics/titanic.csv")


# --------------------------------------------------
# 2. MISSING VALUE ANALYSIS
# --------------------------------------------------

print()
print("Missing values:")
print(df.isna().sum())

print()
print("Missing value percentages:")

missing_percentage = (
    df.isna().mean() * 100
)

for column in df.columns:
    if missing_percentage[column] > 0:
        print(
            column,
            ":",
            round(missing_percentage[column], 4),
            "%"
        )


# --------------------------------------------------
# 3. MISSING VALUE HANDLING
# --------------------------------------------------

# Age has around 20% missing values.
# Since it is between 5% and 30%, use median imputation.

df["age"] = df["age"].fillna(
    df["age"].median()
)

# Embarked has less than 5% missing values.
# Drop those rows.

df = df.dropna(
    subset=["embarked"]
)

# Deck has very high missing values.
# Instead of dropping the column, treat missing
# as its own category.

df["deck"] = df["deck"].astype("object")

df["deck"] = df["deck"].fillna(
    "missing"
)

# Embark_town also has less than 5% missing values.
# Drop those rows.

df = df.dropna(
    subset=["embark_town"]
)

print()
print("Missing values after cleaning:")
print(df.isna().sum())

print()
print("Cleaned dataset shape:")
print(df.shape)


# --------------------------------------------------
# 4. AGE - HISTOGRAM
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["age"],
    bins=20
)

plt.xlabel("Age")
plt.ylabel("Number of passengers")
plt.title("Age Distribution")

plt.savefig(
    "analytics/age_histogram.png"
)

plt.close()


# --------------------------------------------------
# 5. AGE - BOX PLOT
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.boxplot(
    df["age"]
)

plt.ylabel("Age")
plt.title("Age Box Plot")

plt.savefig(
    "analytics/age_boxplot.png"
)

plt.close()


# --------------------------------------------------
# 6. FARE - HISTOGRAM
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["fare"],
    bins=20
)

plt.xlabel("Fare")
plt.ylabel("Number of passengers")
plt.title("Fare Distribution")

plt.savefig(
    "analytics/fare_histogram.png"
)

plt.close()


# --------------------------------------------------
# 7. FARE - BOX PLOT
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.boxplot(
    df["fare"]
)

plt.ylabel("Fare")
plt.title("Fare Box Plot")

plt.savefig(
    "analytics/fare_boxplot.png"
)

plt.close()


# --------------------------------------------------
# 8. IQR OUTLIER ANALYSIS
# --------------------------------------------------

def find_outliers(column):

    q1 = df[column].quantile(0.25)

    q3 = df[column].quantile(0.75)

    iqr = q3 - q1

    lower_limit = q1 - 1.5 * iqr

    upper_limit = q3 + 1.5 * iqr

    outliers = df[
        (df[column] < lower_limit)
        |
        (df[column] > upper_limit)
    ]

    return len(outliers)


age_outliers = find_outliers("age")

fare_outliers = find_outliers("fare")

print()
print("IQR outlier counts:")

print(
    "Age outliers:",
    age_outliers
)

print(
    "Fare outliers:",
    fare_outliers
)


# --------------------------------------------------
# 9. FARE MEAN, MEDIAN AND MODE
# --------------------------------------------------

fare_mean = df["fare"].mean()

fare_median = df["fare"].median()

fare_mode = df["fare"].mode()[0]

print()
print("Fare statistics:")

print(
    "Mean:",
    fare_mean
)

print(
    "Median:",
    fare_median
)

print(
    "Mode:",
    fare_mode
)

if fare_mean > fare_median > fare_mode:

    print(
        "Fare distribution is right-skewed."
    )

elif fare_mean < fare_median < fare_mode:

    print(
        "Fare distribution is left-skewed."
    )

else:

    print(
        "Fare distribution does not follow "
        "a simple mean-median-mode ordering."
    )


# --------------------------------------------------
# 10. SURVIVAL RATE BY SEX
#     BOOLEAN MASKING
# --------------------------------------------------

female_survival = df.loc[
    df["sex"] == "female",
    "survived"
].mean()

male_survival = df.loc[
    df["sex"] == "male",
    "survived"
].mean()

print()
print("Survival rate by sex:")

print(
    "Female:",
    female_survival
)

print(
    "Male:",
    male_survival
)


# --------------------------------------------------
# 11. SURVIVAL RATE BY PASSENGER CLASS
#     BOOLEAN MASKING
# --------------------------------------------------

class_1_survival = df.loc[
    df["pclass"] == 1,
    "survived"
].mean()

class_2_survival = df.loc[
    df["pclass"] == 2,
    "survived"
].mean()

class_3_survival = df.loc[
    df["pclass"] == 3,
    "survived"
].mean()

print()
print("Survival rate by passenger class:")

print(
    "Class 1:",
    class_1_survival
)

print(
    "Class 2:",
    class_2_survival
)

print(
    "Class 3:",
    class_3_survival
)


# --------------------------------------------------
# 12. SURVIVAL RATE BY SEX AND CLASS
#     BOOLEAN MASKING WITH &
# --------------------------------------------------

female_class_1 = df.loc[
    (df["sex"] == "female")
    & (df["pclass"] == 1),
    "survived"
].mean()

female_class_2 = df.loc[
    (df["sex"] == "female")
    & (df["pclass"] == 2),
    "survived"
].mean()

female_class_3 = df.loc[
    (df["sex"] == "female")
    & (df["pclass"] == 3),
    "survived"
].mean()

male_class_1 = df.loc[
    (df["sex"] == "male")
    & (df["pclass"] == 1),
    "survived"
].mean()

male_class_2 = df.loc[
    (df["sex"] == "male")
    & (df["pclass"] == 2),
    "survived"
].mean()

male_class_3 = df.loc[
    (df["sex"] == "male")
    & (df["pclass"] == 3),
    "survived"
].mean()

print()
print("Survival rate by sex and passenger class:")

print(
    "Female, Class 1:",
    female_class_1
)

print(
    "Female, Class 2:",
    female_class_2
)

print(
    "Female, Class 3:",
    female_class_3
)

print(
    "Male, Class 1:",
    male_class_1
)

print(
    "Male, Class 2:",
    male_class_2
)

print(
    "Male, Class 3:",
    male_class_3
)


# --------------------------------------------------
# 13. CORRELATION MATRIX
# --------------------------------------------------

correlation_columns = [
    "survived",
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

correlation_matrix = df[
    correlation_columns
].corr()

print()
print("Correlation matrix:")

print(correlation_matrix)


# --------------------------------------------------
# 14. CORRELATION HEATMAP
# --------------------------------------------------

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Titanic Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "analytics/correlation_heatmap.png"
)

plt.close()


# --------------------------------------------------
# 15. FIND TWO STRONGEST CORRELATIONS
# --------------------------------------------------

correlation_pairs = []

for i in range(
    len(correlation_matrix.columns)
):

    for j in range(
        i + 1,
        len(correlation_matrix.columns)
    ):

        column_1 = correlation_matrix.columns[i]

        column_2 = correlation_matrix.columns[j]

        value = correlation_matrix.iloc[i, j]

        correlation_pairs.append(
            (
                column_1,
                column_2,
                value,
                abs(value)
            )
        )


correlation_pairs.sort(
    key=lambda x: x[3],
    reverse=True
)

print()
print("Two strongest correlations:")

for pair in correlation_pairs[:2]:

    print(
        pair[0],
        "and",
        pair[1],
        ":",
        round(pair[2], 4)
    )


# --------------------------------------------------
# 16. MULTIVARIATE CHART 1
#     SURVIVAL BY SEX
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="sex",
    y="survived"
)

plt.ylabel("Survival Rate")
plt.title("Survival Rate by Sex")

plt.savefig(
    "analytics/survival_by_sex.png"
)

plt.close()


# --------------------------------------------------
# 17. MULTIVARIATE CHART 2
#     SURVIVAL BY CLASS
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="pclass",
    y="survived"
)

plt.ylabel("Survival Rate")
plt.xlabel("Passenger Class")
plt.title("Survival Rate by Passenger Class")

plt.savefig(
    "analytics/survival_by_class.png"
)

plt.close()


# --------------------------------------------------
# 18. MULTIVARIATE CHART 3
#     SEX + CLASS + SURVIVAL
# --------------------------------------------------

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="pclass",
    y="survived",
    hue="sex"
)

plt.ylabel("Survival Rate")
plt.xlabel("Passenger Class")
plt.title("Survival Rate by Sex and Passenger Class")

plt.savefig(
    "analytics/survival_by_sex_class.png"
)

plt.close()


# --------------------------------------------------
# 19. MULTIVARIATE CHART 4
#     AGE + FARE + SURVIVAL
# --------------------------------------------------

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=df,
    x="age",
    y="fare",
    hue="survived"
)

plt.xlabel("Age")
plt.ylabel("Fare")
plt.title("Age vs Fare by Survival")

plt.savefig(
    "analytics/age_fare_survival.png"
)

plt.close()


# --------------------------------------------------
# 20. STANDARDIZATION OF AGE AND FARE
#     EDA ONLY
# --------------------------------------------------

scaler = StandardScaler()

df_standardized = df.copy()

df_standardized[
    ["age", "fare"]
] = scaler.fit_transform(
    df_standardized[
        ["age", "fare"]
    ]
)


print()
print("Before standardization:")

print(
    df[
        ["age", "fare"]
    ].agg(
        ["mean", "std"]
    )
)


print()
print("After standardization:")

print(
    df_standardized[
        ["age", "fare"]
    ].agg(
        ["mean", "std"]
    )
)


# --------------------------------------------------
# 21. SAVE STANDARDIZED EDA DATA
# --------------------------------------------------

df_standardized.to_csv(
    "analytics/titanic_standardized_eda.csv",
    index=False
)

print()
print(
    "Standardized EDA data saved successfully."
)


# --------------------------------------------------
# 22. FINAL MESSAGE
# --------------------------------------------------

print()
print("EDA completed successfully.")

print()
print("Charts saved inside analytics/:")
print("- age_histogram.png")
print("- age_boxplot.png")
print("- fare_histogram.png")
print("- fare_boxplot.png")
print("- correlation_heatmap.png")
print("- survival_by_sex.png")
print("- survival_by_class.png")
print("- survival_by_sex_class.png")
print("- age_fare_survival.png")