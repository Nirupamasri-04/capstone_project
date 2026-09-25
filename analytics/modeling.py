import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv("analytics/titanic.csv")

X = df[
    ["pclass", "sex", "age", "sibsp", "parch", "fare", "embarked"]
]

y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

numeric_columns = [
    "pclass",
    "age",
    "sibsp",
    "parch",
    "fare"
]

categorical_columns = [
    "sex",
    "embarked"
]

numeric_process = Pipeline(
    steps=[
        ("missing", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]
)

categorical_process = Pipeline(
    steps=[
        ("missing", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessing = ColumnTransformer(
    transformers=[
        ("numbers", numeric_process, numeric_columns),
        ("categories", categorical_process, categorical_columns)
    ]
)

logistic_model = Pipeline(
    steps=[
        ("preprocessing", preprocessing),
        ("model", LogisticRegression(max_iter=1000))
    ]
)

tree_model = Pipeline(
    steps=[
        ("preprocessing", preprocessing),
        ("model", DecisionTreeClassifier(random_state=42))
    ]
)

forest_model = Pipeline(
    steps=[
        ("preprocessing", preprocessing),
        (
            "model",
            RandomForestClassifier(random_state=42)
        )
    ]
)

logistic_model.fit(X_train, y_train)

tree_model.fit(X_train, y_train)

forest_model.fit(X_train, y_train)

logistic_prediction = logistic_model.predict(X_test)

tree_prediction = tree_model.predict(X_test)

forest_prediction = forest_model.predict(X_test)

logistic_probability = logistic_model.predict_proba(X_test)[:, 1]

tree_probability = tree_model.predict_proba(X_test)[:, 1]

forest_probability = forest_model.predict_proba(X_test)[:, 1]

def get_results(y_true, prediction, probability):

    accuracy = accuracy_score(y_true, prediction)

    precision = precision_score(y_true, prediction)

    recall = recall_score(y_true, prediction)

    f1 = f1_score(y_true, prediction)

    auc = roc_auc_score(y_true, probability)

    return accuracy, precision, recall, f1, auc


logistic_results = get_results(
    y_test,
    logistic_prediction,
    logistic_probability
)

tree_results = get_results(
    y_test,
    tree_prediction,
    tree_probability
)

forest_results = get_results(
    y_test,
    forest_prediction,
    forest_probability
)

results = pd.DataFrame(
    [
        logistic_results,
        tree_results,
        forest_results
    ],
    columns=[
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "AUC"
    ],
    index=[
        "Logistic Regression",
        "Decision Tree",
        "Random Forest"
    ]
)

print("Model comparison:")
print(results)

print("Logistic Regression confusion matrix:")
print(confusion_matrix(y_test, logistic_prediction))

print("Decision Tree confusion matrix:")
print(confusion_matrix(y_test, tree_prediction))

print("Random Forest confusion matrix:")
print(confusion_matrix(y_test, forest_prediction))

fpr_logistic, tpr_logistic, _ = roc_curve(
    y_test,
    logistic_probability
)

fpr_tree, tpr_tree, _ = roc_curve(
    y_test,
    tree_probability
)

fpr_forest, tpr_forest, _ = roc_curve(
    y_test,
    forest_probability
)

plt.figure(figsize=(8, 6))

plt.plot(
    fpr_logistic,
    tpr_logistic,
    label="Logistic Regression"
)

plt.plot(
    fpr_tree,
    tpr_tree,
    label="Decision Tree"
)

plt.plot(
    fpr_forest,
    tpr_forest,
    label="Random Forest"
)

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()

plt.savefig("analytics/roc_curve.png")

plt.close()

tree = tree_model.named_steps["model"]

feature_names = (
    tree_model
    .named_steps["preprocessing"]
    .get_feature_names_out()
)

plt.figure(figsize=(20, 10))

plot_tree(
    tree,
    feature_names=feature_names,
    class_names=["Not Survived", "Survived"],
    filled=True
)

plt.title("Decision Tree")

plt.savefig("analytics/decision_tree.png")

plt.close()

grid_pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessing),
        (
            "model",
            RandomForestClassifier(
                random_state=42,
                oob_score=True
            )
        )
    ]
)

parameter_grid = {
    "model__n_estimators": [50, 100],
    "model__max_depth": [None, 5, 10],
    "model__max_features": ["sqrt", "log2"]
}

grid_search = GridSearchCV(
    grid_pipeline,
    parameter_grid,
    cv=5,
    scoring="accuracy",
    n_jobs=-1
)

print("Running GridSearchCV...")

grid_search.fit(X_train, y_train)

print("Best parameters:")

print(grid_search.best_params_)

print("Best cross-validation accuracy:")

print(grid_search.best_score_)

best_random_forest = (
    grid_search
    .best_estimator_
    .named_steps["model"]
)

print("OOB score:")

print(best_random_forest.oob_score_)

regression_features = [
    "pclass",
    "sex",
    "age",
    "sibsp",
    "parch",
    "embarked"
]

X_regression = df[regression_features]

y_regression = df["fare"]

X_reg_train, X_reg_test, y_reg_train, y_reg_test = train_test_split(
    X_regression,
    y_regression,
    test_size=0.2,
    random_state=42
)

regression_preprocessing = ColumnTransformer(
    transformers=[
        (
            "numbers",
            Pipeline(
                steps=[
                    ("missing", SimpleImputer(strategy="median")),
                    ("scale", StandardScaler())
                ]
            ),
            numeric_columns[:-1]
        ),
        (
            "categories",
            Pipeline(
                steps=[
                    ("missing", SimpleImputer(strategy="most_frequent")),
                    ("encode", OneHotEncoder(handle_unknown="ignore"))
                ]
            ),
            categorical_columns
        )
    ]
)

regression_model = Pipeline(
    steps=[
        ("preprocessing", regression_preprocessing),
        ("model", LinearRegression())
    ]
)

regression_model.fit(
    X_reg_train,
    y_reg_train
)

fare_prediction = regression_model.predict(
    X_reg_test
)

mae = mean_absolute_error(
    y_reg_test,
    fare_prediction
)

rmse = np.sqrt(
    mean_squared_error(
        y_reg_test,
        fare_prediction
    )
)

r2 = r2_score(
    y_reg_test,
    fare_prediction
)

n = len(y_reg_test)

number_of_predictors = (
    regression_model
    .named_steps["preprocessing"]
    .transform(X_reg_test)
    .shape[1]
)

adjusted_r2 = 1 - (
    (1 - r2)
    * (n - 1)
    / (n - number_of_predictors - 1)
)


print("Regression results:")

print("MAE:", mae)

print("RMSE:", rmse)

print("R2:", r2)

print("Adjusted R2:", adjusted_r2)

residuals = y_reg_test - fare_prediction

plt.figure(figsize=(8, 6))

plt.scatter(
    fare_prediction,
    residuals
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.xlabel("Predicted Fare")

plt.ylabel("Residuals")

plt.title("Residual Plot")

plt.savefig(
    "analytics/regression_residuals.png"
)

plt.close()


print("Residual plot saved successfully.")

best_pipeline = grid_search.best_estimator_

joblib.dump(
    best_pipeline,
    "analytics/titanic_model.joblib"
)

print("Model saved successfully.")

loaded_pipeline = joblib.load(
    "analytics/titanic_model.joblib"
)

print("Model loaded successfully.")

sample_data = pd.DataFrame(
    {
        "pclass": [3],
        "sex": ["female"],
        "age": [25],
        "sibsp": [0],
        "parch": [0],
        "fare": [15.0],
        "embarked": ["S"]
    }
)

prediction = loaded_pipeline.predict(sample_data)

print("Prediction for sample passenger:")

if prediction[0] == 1:
    print("Survived")
else:
    print("Did not survive")
