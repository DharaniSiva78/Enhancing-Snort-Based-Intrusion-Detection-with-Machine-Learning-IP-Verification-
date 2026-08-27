import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns

import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the evaluation CSV. Override with:
#   python training/evaluate_and_plot.py path/to/CICIDS_balanced.csv
# or by setting the DATA_PATH environment variable.
dataset_path = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "DATA_PATH", os.path.join(BASE_DIR, "data", "CICIDS_balanced.csv")
)

if not os.path.exists(dataset_path):
    raise FileNotFoundError(
        f"Dataset not found at '{dataset_path}'.\n"
        f"Place the full CICIDS_balanced.csv in the 'data/' folder, or pass a path:\n"
        f"  python training/evaluate_and_plot.py path/to/CICIDS_balanced.csv"
    )

df = pd.read_csv(dataset_path)
df = df.replace([np.inf, -np.inf], np.nan).fillna(0)

label_column = df.columns[-1]
X = df.drop(columns=[label_column])
y = df[label_column]

encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_encoded, test_size=0.2, random_state=42
)

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
rf_pred = rf.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

xgb = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss'
)
xgb.fit(X_train, y_train)
xgb_pred = xgb.predict(X_test)
xgb_acc = accuracy_score(y_test, xgb_pred)

print(f"Random Forest Accuracy: {rf_acc*100:.2f}%")
print(f"XGBoost Accuracy: {xgb_acc*100:.2f}%")

print("\nClassification Report — Random Forest:")
print(classification_report(y_test, rf_pred, target_names=encoder.classes_))

print("\nClassification Report — XGBoost:")
print(classification_report(y_test, xgb_pred, target_names=encoder.classes_))

rf_cm = confusion_matrix(y_test, rf_pred)
xgb_cm = confusion_matrix(y_test, xgb_pred)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.heatmap(rf_cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.title('Random Forest Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

plt.subplot(1, 2, 2)
sns.heatmap(xgb_cm, annot=True, fmt='d', cmap='Oranges',
            xticklabels=encoder.classes_, yticklabels=encoder.classes_)
plt.title('XGBoost Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

plt.tight_layout()
plot_path = os.path.join(BASE_DIR, "model", "confusion_matrices.png")
plt.savefig(plot_path)
print(f"\nSaved confusion matrix plot to {plot_path}")

model_dir = os.path.join(BASE_DIR, "model")
os.makedirs(model_dir, exist_ok=True)
joblib.dump(rf, os.path.join(model_dir, 'rf_model.joblib'))
joblib.dump(xgb, os.path.join(model_dir, 'xgb_model.joblib'))
joblib.dump(scaler, os.path.join(model_dir, 'scaler.joblib'))
joblib.dump(encoder, os.path.join(model_dir, 'label_encoder.joblib'))
joblib.dump(list(X.columns), os.path.join(model_dir, 'columns.pkl'))
