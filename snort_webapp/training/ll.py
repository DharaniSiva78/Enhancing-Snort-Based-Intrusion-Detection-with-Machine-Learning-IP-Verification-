import os
import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the training CSV. Override with:
#   python training/ll.py path/to/CICIDS_balanced.csv
# or by setting the DATA_PATH environment variable.
DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "DATA_PATH", os.path.join(BASE_DIR, "data", "CICIDS_balanced.csv")
)
MODEL_DIR = os.environ.get("MODEL_DIR", os.path.join(BASE_DIR, "model"))
TARGET_COLUMN = "Label"
TEST_SIZE = 0.2
RANDOM_STATE = 42

sys.stdout.reconfigure(encoding='utf-8')
os.makedirs(MODEL_DIR, exist_ok=True)

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        f"Dataset not found at '{DATA_PATH}'.\n"
        f"Place the full CICIDS_balanced.csv in the 'data/' folder, or pass a path:\n"
        f"  python training/ll.py path/to/CICIDS_balanced.csv"
    )

df = pd.read_csv(DATA_PATH)
X = df.drop(columns=[TARGET_COLUMN])
y = df[TARGET_COLUMN]

if y.dtype == 'object' or not np.issubdtype(y.dtype, np.number):
    le = LabelEncoder()
    y = le.fit_transform(y)
    joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.joblib"))
else:
    le = None

X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(0)
X = X.astype(np.float64)

joblib.dump(X.columns.tolist(), os.path.join(MODEL_DIR, "columns.pkl"))

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.joblib"))

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

subset_size = min(100000, len(X_train))
X_train_sub = X_train[:subset_size]
y_train_sub = y_train[:subset_size]

rf_model = RandomForestClassifier(
    n_estimators=100, max_depth=10, random_state=RANDOM_STATE, n_jobs=-1
)
rf_model.fit(X_train_sub, y_train_sub)
joblib.dump(rf_model, os.path.join(MODEL_DIR, "rf_model.joblib"))

xgb_model = XGBClassifier(
    n_estimators=100, learning_rate=0.1, max_depth=6,
    subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_STATE,
    n_jobs=-1, eval_metric="mlogloss"
)
xgb_model.fit(X_train_sub, y_train_sub)
joblib.dump(xgb_model, os.path.join(MODEL_DIR, "xgb_model.joblib"))

sample_size = min(len(X_test), len(y_test), 20000)
rf_acc = accuracy_score(y_test[:sample_size], rf_model.predict(X_test[:sample_size]))
xgb_acc = accuracy_score(y_test[:sample_size], xgb_model.predict(X_test[:sample_size]))

print(f"Random Forest Accuracy: {rf_acc:.4f}")
print(f"XGBoost Accuracy: {xgb_acc:.4f}")
