"""
Phase 2: Machine Learning Model Training Pipeline
Trains a Physics-Informed Random Forest Classifier for Flash Flood Prediction in Mountainous Terrain.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, train_test_split, cross_validate
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# Base Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_DATA_PATH = os.path.join(BASE_DIR, "dataset.csv")
INCIDENTS_PATH = os.path.join(BASE_DIR, "India_Flood_Incidents_Data.csv")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "ml", "data", "processed")
ML_MODELS_DIR = os.path.join(BASE_DIR, "ml_models")
BACKEND_MODELS_DIR = os.path.join(BASE_DIR, "backend", "app", "models")

# Import physics formulas from backend
import sys
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
from app.models.feature_engineering import (
    calculate_api,
    adjust_cn_for_moisture,
    calculate_potential_retention,
    calculate_scs_runoff,
    calculate_time_concentration,
    engineer_all_features
)

FEATURE_COLS = [
    'rainfall_6h',
    'rainfall_24h',
    'soil_moisture',
    'slope',
    'elevation',
    'cn',
    'antecedent_rain_3d',
    'api',
    'cn_adjusted',
    'potential_retention_mm',
    'expected_runoff_mm',
    'time_concentration_min'
]


def load_and_merge_datasets() -> pd.DataFrame:
    """Load base synthetic/empirical dataset and merge with real historical flood events."""
    print("Loading base dataset from:", RAW_DATA_PATH)
    df_base = pd.read_csv(RAW_DATA_PATH)
    
    # Check if India_Flood_Incidents_Data exists and merge
    if os.path.exists(INCIDENTS_PATH):
        print("Merging real historical flood incident records from:", INCIDENTS_PATH)
        df_incidents = pd.read_csv(INCIDENTS_PATH)
        
        # Normalize soil_moisture (if fraction <= 1.0, scale to percentage 0-100)
        if df_incidents['soil_moisture'].max() <= 1.0:
            df_incidents['soil_moisture'] = df_incidents['soil_moisture'] * 100.0
            
        df_incidents['flood_occurred'] = 1
        df_incidents['severity'] = 'SEVERE'
        
        # Fill missing non-feature columns
        for col in ['state', 'lat', 'lon', 'casualties', 'damage_estimate_inr']:
            if col not in df_incidents.columns:
                df_incidents[col] = 0
                
        # Align columns
        cols = [c for c in df_base.columns if c in df_incidents.columns]
        df_merged = pd.concat([df_base, df_incidents[cols]], ignore_index=True)
    else:
        df_merged = df_base
        
    print(f"Total merged records: {len(df_merged)} (Floods: {(df_merged['flood_occurred'] == 1).sum()}, Non-Floods: {(df_merged['flood_occurred'] == 0).sum()})")
    return df_merged


def compute_physics_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply SCS-CN and Kirpich physics formulas to generate the 12 feature set."""
    print("Computing derived hydrological and topographic features...")
    records = []
    
    for idx, row in df.iterrows():
        r6 = float(row['rainfall_6h'])
        r24 = float(row.get('rainfall_24h', r6 * 2))
        sm = float(row['soil_moisture'])
        slope = float(row['slope'])
        elevation = float(row['elevation'])
        cn = float(row['cn'])
        ant = float(row['antecedent_rain_3d'])
        
        # Compute physics features
        api_val = calculate_api(ant)
        cn_adj = adjust_cn_for_moisture(cn, sm)
        retention = calculate_potential_retention(cn_adj)
        runoff = calculate_scs_runoff(r6, cn_adj)
        tc = calculate_time_concentration(slope, elevation)
        
        records.append({
            'rainfall_6h': r6,
            'rainfall_24h': r24,
            'soil_moisture': sm,
            'slope': slope,
            'elevation': elevation,
            'cn': cn,
            'antecedent_rain_3d': ant,
            'api': api_val,
            'cn_adjusted': cn_adj,
            'potential_retention_mm': retention,
            'expected_runoff_mm': runoff,
            'time_concentration_min': tc,
            'flood_occurred': int(row['flood_occurred'])
        })
        
    df_feat = pd.DataFrame(records)
    
    # Save processed features CSV
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    processed_csv_path = os.path.join(PROCESSED_DATA_DIR, "features.csv")
    df_feat.to_csv(processed_csv_path, index=False)
    print(f"Saved processed features to: {processed_csv_path}")
    
    return df_feat


def train_and_evaluate(df_feat: pd.DataFrame) -> Tuple[RandomForestClassifier, StandardScaler, Dict[str, Any]]:
    """Train Random Forest with Stratified 5-Fold CV and full evaluation."""
    X = df_feat[FEATURE_COLS].values
    y = df_feat['flood_occurred'].values
    
    print("\nSplitting dataset (80% Train, 20% Test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Model definition: Random Forest Classifier
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42
    )
    
    # 5-Fold Stratified Cross Validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(
        rf_model, X_train_scaled, y_train,
        cv=cv,
        scoring=['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    )
    
    cv_summary = {
        'cv_accuracy_mean': round(float(np.mean(cv_results['test_accuracy'])), 4),
        'cv_precision_mean': round(float(np.mean(cv_results['test_precision'])), 4),
        'cv_recall_mean': round(float(np.mean(cv_results['test_recall'])), 4),
        'cv_f1_mean': round(float(np.mean(cv_results['test_f1'])), 4),
        'cv_roc_auc_mean': round(float(np.mean(cv_results['test_roc_auc'])), 4)
    }
    
    print("5-Fold Cross Validation Results:")
    for k, v in cv_summary.items():
        print(f"  {k}: {v*100:.2f}%")
        
    # Fit final model on full training set
    rf_model.fit(X_train_scaled, y_train)
    
    # Test Set Evaluation
    y_pred = rf_model.predict(X_test_scaled)
    y_prob = rf_model.predict_proba(X_test_scaled)[:, 1]
    
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_prob))
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    print("\n--- TEST SET PERFORMANCE ---")
    print(f"Accuracy:  {acc*100:.2f}%")
    print(f"Precision: {prec*100:.2f}%")
    print(f"Recall:    {rec*100:.2f}%  (Target: >= 90%)")
    print(f"F1-Score:  {f1*100:.2f}%")
    print(f"ROC-AUC:   {roc_auc*100:.2f}%")
    print("Confusion Matrix (TN, FP / FN, TP):", cm)
    
    # Feature Importances (Gini)
    importances = rf_model.feature_importances_
    feat_imp = [
        {"feature": name, "importance": round(float(imp), 4)}
        for name, imp in sorted(zip(FEATURE_COLS, importances), key=lambda x: x[1], reverse=True)
    ]
    
    print("\nTop Feature Importances:")
    for f in feat_imp[:6]:
        print(f"  {f['feature']}: {f['importance']*100:.2f}%")
        
    metrics = {
        'model_name': 'RandomForestClassifier_Physics_Informed',
        'n_estimators': 100,
        'max_depth': 8,
        'test_metrics': {
            'accuracy': round(acc, 4),
            'precision': round(prec, 4),
            'recall': round(rec, 4),
            'f1_score': round(f1, 4),
            'roc_auc': round(roc_auc, 4),
            'confusion_matrix': cm
        },
        'cross_validation_5fold': cv_summary,
        'feature_importances': feat_imp,
        'features_used': FEATURE_COLS
    }
    
    return rf_model, scaler, metrics


def save_artifacts(model: RandomForestClassifier, scaler: StandardScaler, metrics: Dict[str, Any]):
    """Save trained model artifacts in both ml_models/ and backend/app/models/ directories."""
    os.makedirs(ML_MODELS_DIR, exist_ok=True)
    os.makedirs(BACKEND_MODELS_DIR, exist_ok=True)
    
    # 1. Save in ml_models/
    joblib.dump(model, os.path.join(ML_MODELS_DIR, "flood_model.pkl"))
    joblib.dump(scaler, os.path.join(ML_MODELS_DIR, "scaler.pkl"))
    with open(os.path.join(ML_MODELS_DIR, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    # 2. Save in backend/app/models/ (for direct fast serving)
    joblib.dump(model, os.path.join(BACKEND_MODELS_DIR, "flood_model.joblib"))
    joblib.dump(scaler, os.path.join(BACKEND_MODELS_DIR, "scaler.joblib"))
    joblib.dump(model, os.path.join(BACKEND_MODELS_DIR, "flood_model.pkl"))
    joblib.dump(scaler, os.path.join(BACKEND_MODELS_DIR, "scaler.pkl"))
    
    # Also save model_report.json in ml/
    ml_report_path = os.path.join(BASE_DIR, "ml", "model_report.json")
    with open(ml_report_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    print(f"\nSaved model artifacts successfully:")
    print(f"  -> {os.path.join(ML_MODELS_DIR, 'flood_model.pkl')}")
    print(f"  -> {os.path.join(BACKEND_MODELS_DIR, 'flood_model.joblib')}")
    print(f"  -> {ml_report_path}")


def main():
    print("=" * 60)
    print("FLASH FLOOD PREDICTION: PHASE 2 MODEL TRAINING")
    print("=" * 60)
    
    df_merged = load_and_merge_datasets()
    df_feat = compute_physics_features(df_merged)
    model, scaler, metrics = train_and_evaluate(df_feat)
    save_artifacts(model, scaler, metrics)
    
    print("\n[SUCCESS] PHASE 2 MODEL TRAINING COMPLETE!")

if __name__ == "__main__":
    main()
