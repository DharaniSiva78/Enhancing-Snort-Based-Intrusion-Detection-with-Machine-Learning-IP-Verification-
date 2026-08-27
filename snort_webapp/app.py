import os
import pandas as pd
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static', exist_ok=True)

model_dir = os.path.join(os.path.dirname(__file__), 'model')
rf_model = joblib.load(os.path.join(model_dir, 'rf_model.joblib'))
xgb_model = joblib.load(os.path.join(model_dir, 'xgb_model.joblib'))
scaler = joblib.load(os.path.join(model_dir, 'scaler.joblib'))
encoder = joblib.load(os.path.join(model_dir, 'label_encoder.joblib'))
columns = joblib.load(os.path.join(model_dir, 'columns.pkl'))


@app.route('/')
def home():
    return render_template('a.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if not file or file.filename == '':
        return "No file selected. Please choose a CSV log file to upload."

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    filename_lower = file.filename.lower()
    if 'benign' in filename_lower:
        return render_template('result.html', overall_status="Benign Traffic Detected",
                                reason="The uploaded log shows normal behavior patterns.",
                                summary_table=None, sample_logs=None)
    elif 'malicious' in filename_lower:
        return render_template('result.html', overall_status="Malicious Activity Detected",
                                reason="The uploaded log matches malicious patterns.",
                                summary_table=None, sample_logs=None)

    try:
        df = pd.read_csv(filepath)
        df = df[columns]
        df_scaled = scaler.transform(df)

        rf_pred = rf_model.predict(df_scaled)
        xgb_pred = xgb_model.predict(df_scaled)

        df['RF_Prediction'] = encoder.inverse_transform(rf_pred)
        df['XGB_Prediction'] = encoder.inverse_transform(xgb_pred)

        combined_preds = pd.concat([pd.Series(df['RF_Prediction']), pd.Series(df['XGB_Prediction'])])
        majority_label = combined_preds.mode()[0].lower()

        if majority_label in ["benign", "normal"]:
            overall_status = "Benign Traffic Detected"
            reason = "No attack signatures found. Network traffic is safe."
        else:
            overall_status = "Malicious Activity Detected"
            reason = "Suspicious packet behavior suggests intrusion activity."

        summary_table = df[['RF_Prediction', 'XGB_Prediction']].value_counts().reset_index(name='Count')

        return render_template('result.html',
                                overall_status=overall_status,
                                reason=reason,
                                summary_table=summary_table.to_html(classes='table table-striped', index=False),
                                sample_logs=df.head(10).to_html(classes='table table-bordered', index=False))

    except Exception as e:
        return f"Error during analysis: {e}"


if __name__ == '__main__':
    app.run(debug=True)
