# Titanic Analytics and Machine Learning

## Overview

This module performs exploratory data analysis and machine learning on the Titanic dataset.

The workflow includes:

- Dataset profiling and missing-value analysis
- Univariate and bivariate analysis
- Correlation analysis
- Multivariate visualizations
- Standardization
- Classification using Logistic Regression, Decision Tree, and Random Forest
- Class imbalance analysis
- Random Forest hyperparameter tuning
- Fare regression
- Model evaluation and saving

## Key Results

The Titanic dataset contained **891 rows and 15 columns**. Missing values were handled using median imputation, row removal, or a separate missing category depending on the missing percentage.

The observed survival rate was **74.04% for females** and **18.89% for males**. Survival also differed across passenger classes, with observed rates of **62.62% for first class, 47.28% for second class, and 24.24% for third class**.

The strongest absolute correlations were between `pclass` and `fare` (-0.5482), and `sibsp` and `parch` (0.4145).

For classification, Logistic Regression, Decision Tree, Random Forest, and a balanced Random Forest were evaluated using accuracy, precision, recall, F1, and AUC. Random Forest hyperparameters were tuned using GridSearchCV.

The best Random Forest parameters were `max_depth=5`, `max_features=sqrt`, and `n_estimators=100`. The best cross-validation accuracy was **0.8231**, with an OOB score of **0.8272**.

Linear Regression was used to predict fare. The model achieved an MAE of **20.8094**, RMSE of **30.4731**, R² of **0.3999**, and adjusted R² of **0.3679**. The residual analysis indicated heteroscedasticity.

## Files

```text
analytics/
├── README.md
├── eda.py
├── modeling.py
├── titanic.csv
├── titanic_model.joblib
├── titanic_standardized_eda.csv
└── charts
How to Run

From the project root:

python analytics/eda.py
python analytics/modeling.py
Design Decisions

The Titanic dataset was saved as titanic.csv for offline use. Modeling preprocessing was implemented using scikit-learn pipelines and fitted on the training data. Random Forest hyperparameters were tuned using GridSearchCV, and the complete fitted pipeline was saved using joblib.