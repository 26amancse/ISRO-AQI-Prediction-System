# 🌍 ISRO AQI Prediction System

An AI-powered Air Quality Index (AQI) prediction platform that leverages satellite data, Google Earth Engine, and Machine Learning to estimate air quality through an interactive web dashboard.

---

## 📖 Overview

This project predicts Air Quality Index (AQI) using remotely sensed satellite data and machine learning. It integrates Google Earth Engine for satellite data extraction, FastAPI as the backend framework, and a responsive web interface for users to interact with the prediction system.

The project demonstrates how Earth observation data can be combined with AI to build scalable environmental monitoring applications.

---

## ✨ Features

- 🌍 Satellite-based AQI prediction
- ☁️ Google Earth Engine integration
- 🤖 Machine Learning prediction model
- ⚡ FastAPI backend
- 🎨 Interactive frontend dashboard
- 📊 CPCB data integration
- 📍 Location-based AQI estimation
- 🔄 Real-time prediction workflow

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Uvicorn
- Google Earth Engine API
- Scikit-learn
- Pandas
- NumPy

### Frontend
- HTML5
- CSS3
- JavaScript

### Machine Learning
- Scikit-learn
- Joblib

### Data Sources
- Google Earth Engine
- CPCB Air Quality Data
- Satellite Environmental Data

---

## 📂 Project Structure

```
AQI DATABASE/
│
├── backend/
│   ├── app.py
│   └── latest_features.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── cpcb/
├── data/
├── aqi_model.pkl
├── train_model.py
├── predict_live.py
└── ...
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ISRO-AQI-Prediction-System.git
```

### 2. Navigate to the project

```bash
cd ISRO-AQI-Prediction-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Authenticate Google Earth Engine

```bash
earthengine authenticate
```

Register your Google Cloud Project with Google Earth Engine before running the application.

---

## ▶️ Running the Backend

```bash
cd backend

py -m uvicorn app:app --reload
```

Backend runs on:

```
http://127.0.0.1:8000
```

---

## ▶️ Running the Frontend

```bash
cd frontend

py -m http.server 5500
```

Open your browser:

```
http://localhost:5500
```

---

## 📷 Screenshots

### Home Page

_Add screenshot here_

### Prediction Result

_Add screenshot here_

---

## 📈 Workflow

1. User opens the web dashboard.
2. Backend requests satellite data from Google Earth Engine.
3. Environmental features are extracted.
4. Machine Learning model predicts AQI.
5. Predicted AQI is displayed on the dashboard.

---

## 🌱 Future Improvements

- Live weather integration
- Interactive GIS map
- AQI forecasting
- Mobile responsive UI
- Docker deployment
- Cloud hosting
- Historical AQI visualization

---

## 👥 Team

- **Aman**
- **Vanshil**

---

## 📄 License

This project is intended for educational, research, and hackathon purposes.

---

## ⭐ Acknowledgements

- Google Earth Engine
- Central Pollution Control Board (CPCB)
- FastAPI
- Scikit-learn
- Python Community

---

If you found this project helpful, consider giving it a ⭐ on GitHub.
