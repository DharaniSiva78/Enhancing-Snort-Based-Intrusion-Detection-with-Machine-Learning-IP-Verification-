<div align="center">

# 🛡️ Enhancing Snort-Based Intrusion Detection with Machine Learning IP Verification

**A hybrid IDS that combines Snort's rule-based detection with machine learning (Random Forest & XGBoost) to verify alerts, cut false positives, and classify network traffic as Benign or Malicious in real time, served through a Flask web app.**


</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Screenshots](#-screenshots)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Workflow Diagrams](#-workflow-diagrams)
- [Machine Learning Pipeline](#-machine-learning-pipeline)
- [Results](#-results)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 📖 Overview

Traditional signature-based IDS tools like **Snort** are fast and reliable at detecting known attack patterns, but they often generate a high number of **false positives**, which overwhelms security analysts.

This project adds a **machine learning verification layer** on top of Snort alerts. Each alert is re-evaluated by trained **Random Forest** and **XGBoost** classifiers, which confirm whether the traffic is truly **Malicious** or actually **Benign**. This reduces the false positive rate from **~18% to ~5%**.

---

## 🖼️ Screenshots

<img width="750" height="400" alt="image" src="https://github.com/user-attachments/assets/c2d01734-f15d-4726-ae4a-3dedcdceb0ba" />

<img width="750" height="400" alt="image" src="https://github.com/user-attachments/assets/8c32e742-9b8e-41d9-9134-ca3dd3d571d3" />

<img width="503" height="237" alt="image" src="https://github.com/user-attachments/assets/fd2de02c-2639-4148-802f-cf22486a57b7" />

<img width="503" height="237" alt="image" src="https://github.com/user-attachments/assets/020b490f-8cc5-4e83-9193-08fcb030f050" />

<img width="412" height="287" alt="image" src="https://github.com/user-attachments/assets/449e351d-23ff-4803-9d69-8c625ff7aa45" />

<img width="412" height="287" alt="image" src="https://github.com/user-attachments/assets/a0c8deb5-e1d4-45d7-8d76-25162122a95a" />

## ✨ Key Features

- 🔗 **Hybrid Snort + ML detection pipeline**
- 🌲 **Random Forest & XGBoost** classifiers trained on the **CICIDS 2017 Balanced Dataset**
- 🌐 **Flask web interface**: upload a Snort log CSV and get an instant classification
- 📉 **False positive rate reduced** from ~18% to ~5%
- ⚡ Real-time Benign vs. Malicious traffic classification

---

## 🏗️ System Architecture

The system has two parts. An **offline training phase** builds the models, and an **online detection phase** verifies Snort alerts through the web app.

```mermaid
flowchart TB
    subgraph NET["🌐 Network Layer"]
        T["Network Traffic<br/>(Packets / Flows)"]
    end

    subgraph IDS["🐗 Detection Layer: Snort IDS"]
        S1["Packet Capture &<br/>Preprocessing"]
        S2["Rule-Based<br/>Signature Matching"]
        S3["Snort Alerts<br/>& Log Output"]
        S1 --> S2 --> S3
    end

    subgraph OFFLINE["🏋️ Offline Training Phase"]
        D1[("CICIDS 2017<br/>Balanced Dataset")]
        D2["Data Cleaning &<br/>Preprocessing"]
        D3["Feature Selection &<br/>Train/Test Split"]
        D4["Train Random Forest<br/>(ll.py)"]
        D5["Train XGBoost<br/>(ll.py)"]
        D6["Evaluate & Plot Metrics<br/>(evaluate_and_plot.py)"]
        D7[("Saved Models<br/>model/*.joblib")]
        D1 --> D2 --> D3
        D3 --> D4
        D3 --> D5
        D4 --> D6
        D5 --> D6
        D4 --> D7
        D5 --> D7
    end

    subgraph WEB["🌐 Application Layer: Flask Web App"]
        W1["Upload Page<br/>(templates/a.html)"]
        W2["Flask Backend<br/>(app.py)"]
        W3["Feature Preprocessing<br/>(Pandas)"]
        W4["ML Verification Engine<br/>(Random Forest / XGBoost)"]
        W5["Result Page<br/>(templates/result.html)"]
        W1 --> W2 --> W3 --> W4 --> W5
    end

    subgraph USER["👤 Security Analyst"]
        U1["Reviews verified alerts<br/>Benign vs. Malicious"]
    end

    T --> S1
    S3 -- "Export log as CSV" --> W1
    D7 -- "Load trained model" --> W4
    W5 --> U1

    classDef net fill:#e3f2fd,stroke:#1976d2,color:#0d47a1
    classDef ids fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef train fill:#fff3e0,stroke:#f57c00,color:#e65100
    classDef web fill:#e8f5e9,stroke:#388e3c,color:#1b5e20
    classDef user fill:#f3e5f5,stroke:#8e24aa,color:#4a148c
    class T net
    class S1,S2,S3 ids
    class D1,D2,D3,D4,D5,D6,D7 train
    class W1,W2,W3,W4,W5 web
    class U1 user
```

### Component Summary

| Component | File / Tool | Responsibility |
|---|---|---|
| **Snort IDS** | Snort | Rule-based packet inspection and alert generation |
| **Training Script** | `training/ll.py` | Trains Random Forest and XGBoost models |
| **Evaluation Script** | `training/evaluate_and_plot.py` | Computes metrics and generates plots |
| **Model Store** | `model/*.joblib` | Persisted trained model artifacts |
| **Flask App** | `app.py` | Handles upload, preprocessing, prediction, and response |
| **Templates** | `a.html`, `result.html` | Upload UI and classification result UI |

---

## 🔄 Workflow Diagrams

### 1️⃣ End-to-End Detection Workflow

```mermaid
flowchart TD
    A([▶️ Network traffic flows]) --> B["Snort inspects packets<br/>using rule signatures"]
    B --> C{Rule matched?}
    C -- No --> D["✅ Traffic allowed<br/>No alert raised"]
    C -- Yes --> E["⚠️ Snort generates alert<br/>and writes log"]
    E --> F["Export alert log<br/>as CSV file"]
    F --> G["Analyst uploads CSV<br/>via Flask web app"]
    G --> H["Preprocess data<br/>clean, select features, scale"]
    H --> I["Load trained ML model<br/>(.joblib)"]
    I --> J["🤖 ML verification<br/>Random Forest / XGBoost"]
    J --> K{ML prediction}
    K -- Malicious --> L["🚨 Confirmed Threat<br/>True Positive"]
    K -- Benign --> M["✅ Likely False Positive<br/>Alert filtered out"]
    L --> N["Display result<br/>on result page"]
    M --> N
    N --> O(["👤 Analyst takes action<br/>on verified alerts only"])

    classDef start fill:#c8e6c9,stroke:#2e7d32,color:#1b5e20
    classDef decision fill:#fff9c4,stroke:#f9a825,color:#6d4c00
    classDef ml fill:#ffe0b2,stroke:#ef6c00,color:#bf360c
    classDef threat fill:#ffcdd2,stroke:#c62828,color:#b71c1c
    classDef safe fill:#bbdefb,stroke:#1565c0,color:#0d47a1
    class A,O start
    class C,K decision
    class H,I,J ml
    class E,L threat
    class D,M safe
```

### 2️⃣ Web Application Request Flow

```mermaid
sequenceDiagram
    autonumber
    actor Analyst
    participant UI as 🌐 Upload Page (a.html)
    participant App as ⚙️ Flask App (app.py)
    participant Prep as 🧹 Pandas Preprocessing
    participant Model as 🤖 ML Model (.joblib)
    participant Res as 📄 Result Page (result.html)

    Analyst->>UI: Select Snort log CSV
    UI->>App: POST /upload (CSV file)
    App->>Prep: Read and clean data
    Prep-->>App: Feature matrix
    App->>Model: Load model and predict
    Model-->>App: Benign / Malicious labels
    App->>Res: Render predictions
    Res-->>Analyst: Classification results
```

### 3️⃣ Model Training Workflow (Offline)

```mermaid
flowchart LR
    A[("CICIDS 2017<br/>Balanced Dataset")] --> B["Load with Pandas"]
    B --> C["Clean data<br/>handle NaN / inf values"]
    C --> D["Encode labels<br/>Benign = 0, Malicious = 1"]
    D --> E["Train / Test Split"]
    E --> F["Train<br/>Random Forest"]
    E --> G["Train<br/>XGBoost"]
    F --> H["Evaluate<br/>Accuracy · Precision<br/>Recall · F1"]
    G --> H
    H --> I["Plot metrics &<br/>confusion matrix"]
    F --> J[("Save .joblib")]
    G --> J
    J --> K["Deploy in Flask app"]
```

### 4️⃣ Hybrid Decision Logic

```mermaid
flowchart LR
    S{{"Snort says"}} --> SA["🚨 Alert"]
    S --> SN["✅ No Alert"]
    SA --> M{{"ML says"}}
    M --> MM["Malicious"]
    M --> MB["Benign"]
    MM --> R1["🔴 Confirmed attack<br/>(True Positive)"]
    MB --> R2["🟢 Suppressed alert<br/>(False Positive removed)"]
    SN --> R3["⚪ Normal traffic"]
```

---

## 🧠 Machine Learning Pipeline

| Stage | Description |
|---|---|
| **Dataset** | CICIDS 2017 Balanced Dataset (benign and attack network flows) |
| **Preprocessing** | Cleaning, handling missing and infinite values, feature selection |
| **Models** | Random Forest and XGBoost classifiers |
| **Task** | Binary classification: **Benign** vs. **Malicious** |
| **Evaluation** | Accuracy, Precision, Recall, F1-Score |
| **Persistence** | Models saved as `.joblib` artifacts for reuse in the web app |

**Why add ML to Snort?**
- 🎯 Snort rules are static, so they can flag harmless traffic that merely resembles an attack
- 🤖 ML learns patterns from flow features and can separate real threats from noise
- 📉 The combination keeps Snort's speed and cuts analyst alert fatigue

---

## 📊 Results

| Model | Accuracy | Precision | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|
| Random Forest | 94.33% | 93.80% | 94.10% | 94.00% |
| **XGBoost** | **95.45%** | **95.00%** | **95.30%** | **95.25%** |

```mermaid
xychart-beta
    title "Model Performance Comparison (%)"
    x-axis ["Accuracy", "Precision", "Recall", "F1-Score"]
    y-axis "Score (%)" 90 --> 100
    bar [94.33, 93.80, 94.10, 94.00]
    bar [95.45, 95.00, 95.30, 95.25]
```
> 🟦 Random Forest  |  🟧 XGBoost

### False Positive Reduction

| Detection Approach | False Positive Rate |
|---|:---:|
| Snort alone | ~18% |
| **Snort + ML verification** | **~5%** |

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python |
| **Web Framework** | Flask |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Data Processing** | Pandas |
| **IDS** | Snort |
| **Dataset** | CICIDS 2017 |

---

## 📂 Project Structure

```
snort_webapp/
├── app.py                  # Flask app
├── templates/              # a.html (upload), result.html (output)
├── training/               # ll.py (train), evaluate_and_plot.py (metrics)
├── model/                  # Saved .joblib model artifacts
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- *(Optional)* Snort installed, if you want to generate your own alert logs

### 1. Clone the repository
```bash
git clone https://github.com/DharaniSiva78/Enhancing-Snort-Based-Intrusion-Detection-with-Machine-Learning-IP-Verification-.git
cd Enhancing-Snort-Based-Intrusion-Detection-with-Machine-Learning-IP-Verification-/snort_webapp
```

### 2. Create a virtual environment *(recommended)*
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the models *(skip if `model/` already has `.joblib` files)*
```bash
python training/ll.py
```

### 5. Evaluate and plot metrics *(optional)*
```bash
python training/evaluate_and_plot.py
```

### 6. Run the web app
```bash
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

---

## 💻 Usage

1. Open the web app in your browser.
2. Upload a **Snort log CSV** file on the upload page.
3. The app preprocesses the data and runs it through the trained model.
4. View the **Benign / Malicious** classification on the result page.
5. Act only on alerts that the ML layer confirms as malicious.

---

## 🔮 Future Enhancements

- 📡 Real-time Snort log streaming instead of manual CSV upload
- 🌍 Threat intelligence feeds for IP reputation checks
- 🧬 Deep learning models (LSTM / CNN) for sequence-based detection
- 📈 Dashboard with live alert statistics and charts
- 🧩 Multi-class attack classification (DoS, PortScan, Brute Force, etc.)
- 🐳 Docker containerization for easy deployment
- 🔔 Email and Slack alerts for confirmed threats

---

## 👤 Author

**Dharani Siva**
GitHub: [@DharaniSiva78](https://github.com/DharaniSiva78)

---

<div align="center">

⭐ If you found this project useful, please consider giving it a star!

</div>
