import pickle
import numpy as np
import pandas as pd
from typing import List
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

def _age_group(age: int) -> str:
    if age < 25:
        return "young"
    elif age < 45:
        return "adult"
    elif age < 60:
        return "middle_age"
    return "senior"

def _lifestyle_risk(row) -> str:
    if row["smoker"] and row["bmi"] > 30:
        return "high"
    elif row["smoker"] and row["bmi"] > 27:
        return "medium"
    else:
        return "low"

def _city_tier(city: str) -> int:
    if city in tier_1_cities:
        return 1
    elif city in tier_2_cities:
        return 2
    return 3

def create_and_apply_features(df: pd.DataFrame) -> pd.DataFrame:
    # add bmi
    df['bmi'] = df['weight'] / (df['height'] ** 2)

    # add age group
    df['age_group'] = df['age'].apply(_age_group)

    # add life risk
    df['lifestyle_risk'] = df.apply(_lifestyle_risk, axis=1)

    # add city tier
    df['city_tier'] = df['city'].apply(_city_tier)

    # drop the unwanted features
    df = df.drop(columns=['age', 'weight', 'height', 'smoker', 'city'])[['income_lpa', 'occupation', 'bmi', 'age_group', 'lifestyle_risk', 'city_tier', 'insurance_premium_category']]

    return df



if __name__ == '__main__':
    df: pd.DataFrame = pd.read_csv("insurance.csv")

    # copy the dataset
    df_copy = df.copy()

    # apply feature engineering
    df_copy = create_and_apply_features(df_copy)

    # select features and target
    X: pd.DataFrame = df_copy[["bmi", "age_group", "lifestyle_risk", "city_tier", "income_lpa", "occupation"]]
    y: pd.DataFrame = df_copy["insurance_premium_category"]

    # define categorical and numerical features
    categorical_features: List[str] = ['age_group', 'lifestyle_risk', 'occupation', 'city_tier']
    numerical_features: List[str] = ['bmi', 'income_lpa']

    # create column transfer for OHE
    preprocessor: ColumnTransformer = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numerical_features)
        ]
    )

    # create a pipeline with preprocessing and random forest classifier
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                max_depth=None,
                min_samples_leaf=2,
                class_weight="balanced",
                criterion="entropy",
                random_state=42,
                n_jobs=-1
            )  
        )
    ])
    
    # Split data and train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipeline.fit(X_train, y_train)
    
    # Predict and evaluate
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    
    # Save the trained pipeline using pickle
    pickle_model_path = "trained_model.pkl"
    with open(pickle_model_path, "wb") as f:
        pickle.dump(pipeline, f)