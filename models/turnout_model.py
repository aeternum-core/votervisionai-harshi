import pandas as pd
import numpy as np
import os
import sys
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score, accuracy_score, classification_report

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def train_and_save_models():
    # 1. Load data
    if not os.path.exists(config.DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {config.DATASET_PATH}. Please run the synthetic generator first.")
        
    df = pd.read_csv(config.DATASET_PATH)
    
    # 2. Preprocess & Feature Engineering
    # Encode region_type
    df['is_urban'] = df['region_type'].map({'Urban': 1, 'Rural': 0}).fillna(0).astype(int)
    
    # Define features
    feature_cols = [
        'historical_turnout',
        'literacy_rate',
        'awareness_score',
        'transport_accessibility',
        'weather_score',
        'campaign_intensity',
        'holiday_factor',
        'is_urban'
    ]
    
    X = df[feature_cols]
    
    # Targets
    y_reg = df['actual_final_turnout']
    
    # Map risk levels to numbers: Low: 0, Medium: 1, High: 2
    risk_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
    y_clf = df['risk_level'].map(risk_mapping).fillna(0).astype(int)
    
    # Train-test split
    X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    _, _, y_train_clf, y_test_clf = train_test_split(X, y_clf, test_size=0.2, random_state=42)
    
    # 3. Train Turnout Regressor (Regression)
    print("Training Voter Turnout Regressor (Random Forest)...")
    reg_model = RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42)
    reg_model.fit(X_train, y_train_reg)
    
    # Evaluate Regressor
    y_pred_reg = reg_model.predict(X_test)
    mae = mean_absolute_error(y_test_reg, y_pred_reg)
    rmse = root_mean_squared_error(y_test_reg, y_pred_reg)
    r2 = r2_score(y_test_reg, y_pred_reg)
    
    print(f"Regressor Metrics - MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")
    
    # 4. Train Risk Classifier (Classification)
    print("Training Risk Classifier (Random Forest)...")
    clf_model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf_model.fit(X_train, y_train_clf)
    
    # Evaluate Classifier
    y_pred_clf = clf_model.predict(X_test)
    acc = accuracy_score(y_test_clf, y_pred_clf)
    report = classification_report(y_test_clf, y_pred_clf, target_names=['Low', 'Medium', 'High'], output_dict=True)
    
    print(f"Classifier Metrics - Accuracy: {acc:.4f}")
    
    # 5. Save Models
    joblib.dump(reg_model, config.TURNOUT_MODEL_PATH)
    joblib.dump(clf_model, config.RISK_MODEL_PATH)
    print(f"Models saved successfully to {config.TRAINED_MODELS_DIR}")
    
    # Save Feature Importance for visualization
    feature_importance_reg = dict(zip(feature_cols, reg_model.feature_importances_.tolist()))
    feature_importance_clf = dict(zip(feature_cols, clf_model.feature_importances_.tolist()))
    
    # Save Metrics JSON
    eval_metrics = {
        'regression': {
            'mae': float(mae),
            'rmse': float(rmse),
            'r2': float(r2),
            'feature_importance': feature_importance_reg
        },
        'classification': {
            'accuracy': float(acc),
            'precision': float(report['macro avg']['precision']),
            'recall': float(report['macro avg']['recall']),
            'f1_score': float(report['macro avg']['f1-score']),
            'feature_importance': feature_importance_clf
        }
    }
    
    eval_path = os.path.join(config.TRAINED_MODELS_DIR, 'model_evaluation.json')
    with open(eval_path, 'w') as f:
        json.dump(eval_metrics, f, indent=4)
    print(f"Evaluation metrics saved to {eval_path}")

if __name__ == '__main__':
    train_and_save_models()
