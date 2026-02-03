# 🚀 AI-Powered Task Optimizer

## 📌 Project Overview
The **AI-Powered Task Optimizer** is a Python-based application designed to
improve **productivity and employee well-being** by analyzing emotional input
and recommending suitable tasks.

The system performs **emotion detection from text**, maintains **historical
mood records**, generates **stress alerts**, and provides **employee and HR
dashboards** for monitoring emotional trends.


## 🗂 Features

### 1️⃣ Emotion Detection (Text-Based)
- Detects emotions from employee text input
- Supported emotions:
  - Joy
  - Sadness
  - Anger
  - Stress
  - Disappointment
  - Embarrassed
  - Neutral
- Implemented using keyword-based NLP logic (no external APIs)

### 2️⃣ Task Recommendation
- Suggests tasks based on detected emotions
- Helps reduce burnout by adapting workload
- Encourages productivity during positive emotional states

### 3️⃣ Historical Mood Tracking
- Stores employee emotion data with:
  - Timestamp
  - Employee ID
  - Employee Name
  - Input sentence
  - Detected emotions
- Enables long-term emotional trend analysis

### 4️⃣ Stress Management Alerts
- Automatically analyzes recent emotional history
- Triggers alerts when repeated negative emotions are detected
- Helps HR and managers take preventive action

### 5️⃣ Employee & HR Management
- Employee account creation and login
- HR account creation and login
- HR dashboard to:
  - View employee emotion alerts
  - Monitor emotional patterns
  - Identify stressed employees


## 🗂 CSV-Based Data Storage

All application data is stored locally using CSV files:
### employee_mood_history.csv
Stores complete emotion logs:

## ⚡ Tech Stack

- **Python** – Core AI & real-time emotion detection  
- **OpenCV / MediaPipe / Face Recognition** – Real-time emotion detection  
- **Pandas / Matplotlib / Seaborn** – Mood tracking & visualization  
- **Flask** - Web framework for routing, authentication, and dashboards
- **HTML and CSS - Frontend

## 📈 How to Use

1. **Clone the repository**
git clone https://github.com/Srinidhikt/Amdox_AI_Powered-_task_Optimizer.git



**Note:** Full datasets are too large for GitHub. Download them [here] https://drive.google.com/drive/folders/1QdvAGOadpfy0QMciGfNxTH2oFKJHnoBv.

