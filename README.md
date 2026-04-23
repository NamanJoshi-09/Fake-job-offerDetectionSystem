# 🛡️ JobShield — Fake Job Detection System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Accuracy](https://img.shields.io/badge/Accuracy-98.4%25-2a4d3e?style=for-the-badge)
![Live](https://img.shields.io/badge/Live-Streamlit_Cloud-00c7b7?style=for-the-badge&logo=streamlit&logoColor=white)

**An AI-powered web app that detects fraudulent job postings in real time.**

*B.Tech Minor Project · Semester II · CSE AI & ML (Section F)*
*K.R. Mangalam University, Gurugram · January 2026*

---

## 🔗 Live Demo

**[→ minor-sem2-dataminds.streamlit.app](https://minor-sem2-dataminds.streamlit.app/)**

> Paste any job description and get an instant fraud verdict — no sign-up, no cost.

---

## 📸 Screenshot

![JobShield App Screenshot](https://raw.githubusercontent.com/NamanJoshi-09/Fake-job-offerDetectionSystem/main/screenshot.png)

> *Dark-themed UI with sample loader, analysis portal, and a 3-step "How It Works" section.*

---

## 📌 Overview

Millions of fake job postings target students and freshers every year — causing financial loss, identity theft, and psychological distress. **JobShield** is a free, accessible tool that analyzes any job description and instantly flags it as legitimate or fraudulent using a machine learning model trained on 17,880 real-world postings.

**Paste a job description → click Run Diagnostics → get a trust score with verdict.**

---

## ✨ Features

- 🔍 **Real-time analysis** — instant fraud probability score for any job posting
- 📊 **Trust score meter** — visual confidence bar with color-coded verdict
- 🧪 **Sample loader** — one-click Scam and Real job examples to test the model
- ⚙️ **Pre-trained model** — `model.pkl` and `vectorizer.pkl` ship with the repo; no retraining needed on first run
- 🎨 **Custom dark UI** — sleek Streamlit interface with branded JOBSHIELD · DATAMINDS header

---

## 🖥️ App Preview

| Section | Description |
|---|---|
| **Quick Load** | Load a Scam Sample or Real Sample with one click |
| **Analysis Portal** | Paste any full job description and run diagnostics |
| **How It Works** | 3-step explainer — Paste → Engine Scans → Get Report |
| **About & Team** | Project info, tech tags, and team member roles |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/NamanJoshi-09/Fake-job-offerDetectionSystem.git
cd Fake-job-offerDetectionSystem

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

> **Note:** `model.pkl` and `vectorizer.pkl` are already included in the repo — the model loads instantly with no retraining step required.

---

## 📂 Project Structure

```
Fake-job-offerDetectionSystem/
├── data/
│   └── jobs.csv                 # Dataset (EMSCAD Kaggle — fake job postings)
├── model/
│   └── train_model.py           # Script to retrain the model from scratch
├── app.py                       # Main Streamlit application
├── model.pkl                    # Pre-trained Logistic Regression model
├── vectorizer.pkl               # Pre-fitted TF-IDF vectorizer
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

---

## 🧠 How It Works

### ML Pipeline

```
Raw Job Text
     │
     ▼
┌─────────────────────────┐
│  1. Text Preprocessing  │  Strip HTML, special chars, extra whitespace
│                         │  Merge: title + company + description +
│                         │         requirements + benefits → one string
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  2. TF-IDF Vectorizer   │  15,000 features · bigrams (1,2)
│  (vectorizer.pkl)       │  sublinear_tf=True · English stop words removed
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. Logistic Regression │  class_weight='balanced' (handles 20:1 imbalance)
│  (model.pkl)            │  Outputs calibrated fraud probability [0–1]
└────────────┬────────────┘
             │
             ▼
      Trust Score (%)
      Verdict + Bar
```

### Model Performance (80/20 train-test split)

| Metric | Genuine Jobs | Fake Jobs |
|---|---|---|
| Precision | 1.00 | 0.77 |
| Recall | 0.99 | **0.93** |
| F1-Score | 0.99 | 0.85 |
| **Overall Accuracy** | | **98.4%** |

> The model is tuned for **high recall on fake jobs** — it is better to flag a real job as suspicious than to miss a scam.

---

## 📦 Dataset

| Property | Details |
|---|---|
| Source | [Kaggle — EMSCAD Real or Fake Job Postings](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) |
| File | `data/jobs.csv` |
| Total records | 17,880 |
| Genuine postings | 17,014 |
| Fake postings | 866 |
| Features used | `title`, `company_profile`, `description`, `requirements`, `benefits` |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit + custom HTML/CSS |
| ML Pipeline | scikit-learn (TF-IDF + Logistic Regression) |
| Model persistence | joblib (`model.pkl`, `vectorizer.pkl`) |
| Data processing | pandas |
| Deployment | Streamlit Cloud |
| Language | Python 3.9+ |

---

## 🔁 Retraining the Model

If you want to retrain on updated data:

```bash
python model/train_model.py
```

This will regenerate `model.pkl` and `vectorizer.pkl` from `data/jobs.csv`.

---

## 👨‍💻 Team — DataMinds

| Name | Enrollment No. | Role |
|---|---|---|
| Naman Joshi | 2501730415 | Data Processing & Vectorization |
| Vedansh Rawat | 2501730364 | Main ML Engineer |
| Dhruv Jaiswal | 2501730362 | Streamlit Frontend Developer |
| Pranav Yadav | 2501730390 | Backend & Logic Integration |
| V.R. Adikrishna | 2501730397 | Documentation & Data Handling |
| Vansh Sihag | 2501730387 | Debugging & Deployment Engineer |

**Supervisor:** Atisha Dahiya
**School:** School of Engineering & Technology, K.R. Mangalam University
**Projexa Team ID:** 26E1022

---

## 📄 License

This project was developed for academic purposes as part of a B.Tech minor project.
Dataset credit: [Kaggle EMSCAD](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) — used for research and educational use only.

---

*Made with ❤️ by DataMinds Engineering · K.R. Mangalam University · 2026*