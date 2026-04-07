# 🛡️ JobShield — Fake Job Detection System

**An AI-powered web app that detects fraudulent job postings in real time.**

*B.Tech Minor Project · Semester II · CSE AI & ML (Section F)*
*K.R. Mangalam University, Gurugram · January 2026*

---

## 📌 Overview

Millions of fake job postings target students and freshers every year — causing financial loss, identity theft, and psychological distress. **JobShield** is a free, accessible tool that analyzes any job description and instantly flags it as legitimate or fraudulent using a machine learning model trained on 17,880 real-world postings.

Paste a job description → click **Run Diagnostics** → get a trust score with verdict.

---

## ✨ Features

- 🔍 **Real-time analysis** — instant fraud probability score for any job posting
- 📊 **Trust score meter** — visual confidence bar with color-coded verdict
- 🧪 **Sample loader** — one-click scam and real job examples to test the model
- ⚙️ **Auto model training** — trains and caches the model on first run if no `.pkl` found
- 🎨 **Clean UI** — custom-designed Streamlit interface with DM Sans + DM Serif Display

---

## 🖥️ Demo

| Legitimate Posting | Fraudulent Posting |
|---|---|
| ✓ Likely Legitimate · High trust score | ✕ High Risk · Low trust score |
| Professional tone, official apply link | Urgency language, WhatsApp contact, fees |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/jobshield.git
cd jobshield/dataminds

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the dataset (download from Kaggle — link below)
#    Put fake_job_postings.csv in the same folder as app.py

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

> **Note:** On first run, if `model.pkl` is not found, the model trains automatically from the CSV (~30 seconds). It is cached for all future runs.

---

## 📂 Project Structure

```
dataminds/
├── app.py                   # Main Streamlit application
├── fake_job_postings.csv    # Dataset (download separately from Kaggle)
├── model.pkl                # Trained model (auto-generated on first run)
├── requirements.txt         # Python dependencies
├── README.md
└── .streamlit/
    └── config.toml          # Theme configuration
```

---

## 🧠 How It Works

### Pipeline

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
│                         │  sublinear_tf=True · English stop words removed
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. Logistic Regression │  class_weight='balanced' (handles 20:1 imbalance)
│                         │  Outputs calibrated fraud probability [0–1]
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

The model is tuned for **high recall on fake jobs** — it is better to flag a real job as suspicious than to miss a scam.

---

## 📦 Dataset

| Property | Details |
|---|---|
| Source | [Kaggle — EMSCAD Real or Fake Job Postings](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) |
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
| Model persistence | joblib |
| Data processing | pandas |
| Language | Python 3.9+ |

---

## 👨‍💻 Team

| Name | Enrollment No. |
|---|---|
| Naman Joshi | 2501730415 |
| Vedansh Rawat | 2501730364 |
| Vansh Sihag | 2501730387 |
| Pranav Yadav | 2501730390 |
| Dhruv Jaiswal | 2501730362 |
| V.R. Adikrishna | 2501730397 |

**Supervisor:** # 🛡️ JobShield — Fake Job Detection System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Accuracy](https://img.shields.io/badge/Accuracy-98.4%25-2a4d3e?style=for-the-badge)

**An AI-powered web app that detects fraudulent job postings in real time.**

*B.Tech Minor Project · Semester II · CSE AI & ML (Section F)*
*K.R. Mangalam University, Gurugram · January 2026*

---

## 📌 Overview

Millions of fake job postings target students and freshers every year — causing financial loss, identity theft, and psychological distress. **JobShield** is a free, accessible tool that analyzes any job description and instantly flags it as legitimate or fraudulent using a machine learning model trained on 17,880 real-world postings.

Paste a job description → click **Run Diagnostics** → get a trust score with verdict.

---

## ✨ Features

- 🔍 **Real-time analysis** — instant fraud probability score for any job posting
- 📊 **Trust score meter** — visual confidence bar with color-coded verdict
- 🧪 **Sample loader** — one-click scam and real job examples to test the model
- ⚙️ **Auto model training** — trains and caches the model on first run if no `.pkl` found
- 🎨 **Clean UI** — custom-designed Streamlit interface with DM Sans + DM Serif Display

---

## 🖥️ Demo

| Legitimate Posting | Fraudulent Posting |
|---|---|
| ✓ Likely Legitimate · High trust score | ✕ High Risk · Low trust score |
| Professional tone, official apply link | Urgency language, WhatsApp contact, fees |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/jobshield.git
cd jobshield/dataminds

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the dataset (download from Kaggle — link below)
#    Put fake_job_postings.csv in the same folder as app.py

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

> **Note:** On first run, if `model.pkl` is not found, the model trains automatically from the CSV (~30 seconds). It is cached for all future runs.

---

## 📂 Project Structure

```
dataminds/
├── app.py                   # Main Streamlit application
├── fake_job_postings.csv    # Dataset (download separately from Kaggle)
├── model.pkl                # Trained model (auto-generated on first run)
├── requirements.txt         # Python dependencies
├── README.md
└── .streamlit/
    └── config.toml          # Theme configuration
```

---

## 🧠 How It Works

### Pipeline

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
│                         │  sublinear_tf=True · English stop words removed
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. Logistic Regression │  class_weight='balanced' (handles 20:1 imbalance)
│                         │  Outputs calibrated fraud probability [0–1]
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

The model is tuned for **high recall on fake jobs** — it is better to flag a real job as suspicious than to miss a scam.

---

## 📦 Dataset

| Property | Details |
|---|---|
| Source | [Kaggle — EMSCAD Real or Fake Job Postings](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) |
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
| Model persistence | joblib |
| Data processing | pandas |
| Language | Python 3.9+ |

---

## 👨‍💻 Team

| Name | Enrollment No. |
|---|---|
| Naman Joshi | 2501730415 |
| Vedansh Rawat | 2501730364 |
| Vansh Sihag | 2501730387 |
| Pranav Yadav | 2501730390 |
| Dhruv Jaiswal | 2501730362 |
| V.R. Adikrishna | 2501730397 |

**Supervisor:** # 🛡️ JobShield — Fake Job Detection System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Accuracy](https://img.shields.io/badge/Accuracy-98.4%25-2a4d3e?style=for-the-badge)

**An AI-powered web app that detects fraudulent job postings in real time.**

*B.Tech Minor Project · Semester II · CSE AI & ML (Section F)*
*K.R. Mangalam University, Gurugram · January 2026*

---

## 📌 Overview

Millions of fake job postings target students and freshers every year — causing financial loss, identity theft, and psychological distress. **JobShield** is a free, accessible tool that analyzes any job description and instantly flags it as legitimate or fraudulent using a machine learning model trained on 17,880 real-world postings.

Paste a job description → click **Run Diagnostics** → get a trust score with verdict.

---

## ✨ Features

- 🔍 **Real-time analysis** — instant fraud probability score for any job posting
- 📊 **Trust score meter** — visual confidence bar with color-coded verdict
- 🧪 **Sample loader** — one-click scam and real job examples to test the model
- ⚙️ **Auto model training** — trains and caches the model on first run if no `.pkl` found
- 🎨 **Clean UI** — custom-designed Streamlit interface with DM Sans + DM Serif Display

---

## 🖥️ Demo

| Legitimate Posting | Fraudulent Posting |
|---|---|
| ✓ Likely Legitimate · High trust score | ✕ High Risk · Low trust score |
| Professional tone, official apply link | Urgency language, WhatsApp contact, fees |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/jobshield.git
cd jobshield/dataminds

# 2. Install dependencies
pip install -r requirements.txt

# 3. Place the dataset (download from Kaggle — link below)
#    Put fake_job_postings.csv in the same folder as app.py

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

> **Note:** On first run, if `model.pkl` is not found, the model trains automatically from the CSV (~30 seconds). It is cached for all future runs.

---

## 📂 Project Structure

```
dataminds/
├── app.py                   # Main Streamlit application
├── fake_job_postings.csv    # Dataset (download separately from Kaggle)
├── model.pkl                # Trained model (auto-generated on first run)
├── requirements.txt         # Python dependencies
├── README.md
└── .streamlit/
    └── config.toml          # Theme configuration
```

---

## 🧠 How It Works

### Pipeline

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
│                         │  sublinear_tf=True · English stop words removed
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. Logistic Regression │  class_weight='balanced' (handles 20:1 imbalance)
│                         │  Outputs calibrated fraud probability [0–1]
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

The model is tuned for **high recall on fake jobs** — it is better to flag a real job as suspicious than to miss a scam.

---

## 📦 Dataset

| Property | Details |
|---|---|
| Source | [Kaggle — EMSCAD Real or Fake Job Postings](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) |
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
| Model persistence | joblib |
| Data processing | pandas |
| Language | Python 3.9+ |

---

## 👨‍💻 Team

| Name | Enrollment No. |
|---|---|
| Naman Joshi | 2501730415 |
| Vedansh Rawat | 2501730364 |
| Vansh Sihag | 2501730387 |
| Pranav Yadav | 2501730390 |
| Dhruv Jaiswal | 2501730362 |
| V.R. Adikrishna | 2501730397 |

**Supervisor:** Atisha Dahiya **
**School:** School of Engineering & Technology, K.R. Mangalam University
**Projexa Team ID:** 26E1022

---

## 📄 License

This project was developed for academic purposes as part of a B.Tech minor project.
Dataset credit: [Kaggle EMSCAD](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) — used for research and educational use only.

---

*Made with ❤️ by DataMinds Engineering · K.R. Mangalam University · 2026
**School:** School of Engineering & Technology, K.R. Mangalam University
**Projexa Team ID:** 26E1022

---

## 📄 License

This project was developed for academic purposes as part of a B.Tech minor project.
Dataset credit: [Kaggle EMSCAD](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) — used for research and educational use only.

---

*Made with ❤️ by DataMinds Engineering · K.R. Mangalam University · 2026*
**School:** School of Engineering & Technology, K.R. Mangalam University
**Projexa Team ID:** 26E1022

---

## 📄 License

This project was developed for academic purposes as part of a B.Tech minor project.
Dataset credit: [Kaggle EMSCAD](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobpostingprediction) — used for research and educational use only.

---

*Made with ❤️ by DataMinds Engineering · K.R. Mangalam University · 2026*
