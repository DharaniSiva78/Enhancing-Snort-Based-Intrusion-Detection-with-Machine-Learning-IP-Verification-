# Enhancing-Snort-Based-Intrusion-Detection-with-Machine-Learning-IP-Verification

A hybrid IDS that combines **Snort's** rule-based detection with **machine learning** (Random Forest & XGBoost) to verify alerts, cut false positives, and classify network traffic as **Benign** or **Malicious** in real time — served through a Flask web app.

## Features
- Hybrid Snort + ML detection pipeline
- Random Forest & XGBoost classifiers trained on the CICIDS 2017 Balanced Dataset
- Flask web interface: upload a Snort log CSV → get an instant classification
- False positive rate reduced from ~18% to ~5%

## Results

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|:--:|:--:|:--:|:--:|
| Random Forest | 94.33% | 93.80% | 94.10% | 94.00% |
| **XGBoost** | **95.45%** | **95.00%** | **95.30%** | **95.25%** |

## Project Structure
```
snort_webapp/
├── app.py                 # Flask app
├── templates/              # a.html (upload), result.html (output)
├── training/                # ll.py (train), evaluate_and_plot.py (metrics)
├── model/                    # Saved .joblib model artifacts
└── requirements.txt
```


## Tech Stack
Python · Flask · Scikit-learn · XGBoost · Pandas · Snort · CICIDS 2017 Dataset

<img width="750" height="400" alt="image" src="https://github.com/user-attachments/assets/c2d01734-f15d-4726-ae4a-3dedcdceb0ba" />

<img width="750" height="400" alt="image" src="https://github.com/user-attachments/assets/8c32e742-9b8e-41d9-9134-ca3dd3d571d3" />

<img width="503" height="237" alt="image" src="https://github.com/user-attachments/assets/fd2de02c-2639-4148-802f-cf22486a57b7" />

<img width="503" height="237" alt="image" src="https://github.com/user-attachments/assets/020b490f-8cc5-4e83-9193-08fcb030f050" />

<img width="412" height="287" alt="image" src="https://github.com/user-attachments/assets/449e351d-23ff-4803-9d69-8c625ff7aa45" />

<img width="412" height="287" alt="image" src="https://github.com/user-attachments/assets/a0c8deb5-e1d4-45d7-8d76-25162122a95a" />
