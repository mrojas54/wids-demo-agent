from wids.ai.agents.analyst_agent.custom_tools.presenter import generate_presentation


CONTENT = """
"Title: Predictive Model for Diabetes Dataset
Introduction:
The predictive model for the diabetes dataset has been successfully built using a Random Forest algorithm. Here are the key results and insights from the model:
Model Performance:
- Accuracy: 99.74% (The model correctly predicts diabetes outcomes in nearly all cases)
- Precision: 
 - Class 0: 99.60% (Almost all predicted non-diabetes cases are correct)
 - Class 1: 100.00% (All predicted diabetes cases are correct)
- Recall: 
 - Class 0: 100.00% (All actual non-diabetes cases are identified)
 - Class 1: 99.24% (Nearly all actual diabetes cases are identified)
- F1-Score: 
 - Class 0: 99.80% (Balance between precision and recall for non-diabetes)
 - Class 1: 99.62% (Balance between precision and recall for diabetes)
Confusion Matrix:
- True Negatives (Class 0): 1251 (Correctly identified non-diabetes cases)
- False Positives (Class 0): 0 (No incorrect diabetes predictions for non-diabetes cases)
- False Negatives (Class 1): 5 (Very few missed diabetes cases)
- True Positives (Class 1): 652 (Correctly identified diabetes cases)
Feature Importances:
- Family History: 84.38% (Most significant factor in predicting diabetes)
- Glucose: 11.43% (Second most important factor)
- HbA1c: 2.38% (Third most important factor)
- BMI: 0.81% (Minor importance)
- Blood Pressure: 0.83% (Minor importance)
- Age: 0.11% (Least important)
- Other features have negligible importance.
Insights:
- The model shows excellent performance with high accuracy, precision, recall, and F1-scores, indicating its reliability in predicting diabetes outcomes.
- Family History is the most significant predictor, followed by Glucose and HbA1c levels.
- The confusion matrix indicates very few misclassifications, with only 5 false negatives.
These results demonstrate the model's effectiveness in predicting diabetes, with Family History being a critical factor."
"""

if __name__ == "__main__":
    generate_presentation(CONTENT)
