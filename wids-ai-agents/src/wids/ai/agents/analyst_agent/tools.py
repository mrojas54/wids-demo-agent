import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from langchain.tools import tool


@tool
def perform_eda() -> str:
    """Perform exploratory data analysis on the diabetes dataset."""

    df = pd.read_csv(
       "/Users/michellerojas/pydata/virginia2025/wids-demo-agent/wids-ai-agents/src/wids/ai/agents/analyst_agent/diabetes.csv"
    )

    # Basic statistics
    stats = df.describe().to_dict()

    # Check for missing values
    missing_values = df.isnull().sum().to_dict()

    # Check for zero values (which might be missing values in this dataset)
    zero_values = {col: (df[col] == 0).sum() for col in df.columns}

    # Correlation with target
    correlations = df.corr()["Outcome"].drop("Outcome").to_dict()

    # Result dictionary
    eda_results = {
        "basic_stats": stats,
        "missing_values": missing_values,
        "zero_values": zero_values,
        "correlations_with_target": correlations,
    }
    return eda_results


@tool
def train_model():
    """Train a Random Forest model on the diabetes dataset."""

    df = pd.read_csv(
        "/Users/michellerojas/pydata/virginia2025/wids-demo-agent/wids-ai-agents/src/wids/ai/agents/analyst_agent/diabetes.csv"
    )

    # Replace zeros with NaN for certain columns where zero doesn't make biological sense
    cols_with_zeros = ["Glucose", "BloodPressure", "BMI"]
    for col in cols_with_zeros:
        df[col] = df[col].replace(0, np.nan)

        # Simple imputation with median
    for col in cols_with_zeros:
        df[col] = df[col].fillna(df[col].median())

        # Split features and target
    X = df.drop("Outcome", axis=1)
    y = df["Outcome"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=3,
        max_depth=3,
        min_samples_split=20,
        max_features="sqrt",
        class_weight="balanced",
        bootstrap=True,
        random_state=42,
        max_samples=0.8,
        min_samples_leaf=10,
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()

    # Feature importance
    feature_importances = dict(zip(X.columns, model.feature_importances_))

    # Results
    model_results = {
        "accuracy": accuracy,
        "classification_report": class_report,
        "confusion_matrix": conf_matrix,
        "feature_importances": feature_importances,
    }

    return model_results


@tool
def presentation_tool(content: str, theme_path: str = "presenter_theme.pptx"):
    """
    Build a PowerPoint presentation with a background theme.

    Args:
        content: Text content to include in the presentation.
        theme_path: (Optional) Path to a PowerPoint theme/template (.pptx) file.
    """
    from wids.ai.agents.analyst_agent.custom_tools.presenter import generate_presentation
  
    try:
        file_path = generate_presentation(content, theme_path)
        print(f"Presentation created successfully at {file_path}")
        return {
            "status": "success",
            "message": f"Presentation created successfully at {file_path}",
            "file_path": file_path
        }

    except Exception as e:
        raise e

