# 🎓 Advanced AI-Powered Online Proctoring System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-Machine%20Learning-orange.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)

An intelligent, secure, and robust online proctoring system designed to maintain the integrity of remote examinations. Leveraging modern Web AI and a scalable backend architecture, this system actively monitors students to prevent cheating and unfair practices.

## ✨ Key Features

* **🧠 Real-Time AI Face Monitoring**: Utilizes `blazeface` (TensorFlow.js) to detect if a student is looking away from the screen or if multiple people are present in the camera frame.
* **📱 Object & Device Detection**: Integrates `COCO-SSD` to automatically flag the usage of mobile phones or other restricted devices during the exam.
* **🔊 Audio & Noise Detection**: Uses the Web Audio API to detect suspicious background noise, whispering, or talking.
* **🚫 Anti-Tab Switching**: Tracks browser visibility state. Switching tabs or minimizing the browser triggers an automatic violation log.
* **⏱️ Secure Exam Engine**: Features a live countdown timer with auto-submission capabilities.
* **📊 Comprehensive Dashboard**: A clean UI for students to view assigned exams, performance, and proctoring feedback.
* **⚙️ Scalable API Architecture**: Built with FastAPI, SQLAlchemy, and PostgreSQL for high-performance data processing and authentication.

## 🛠️ Technology Stack

**Frontend:**
* HTML5, CSS3, JavaScript
* TensorFlow.js (BlazeFace, COCO-SSD)
* Web Audio API

**Backend:**
* Python (FastAPI)
* SQLAlchemy (ORM)
* PostgreSQL (Database)
* Uvicorn (ASGI Server)

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* PostgreSQL Server

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/code-by-abrar/online-proctoring-system.git
   cd online-proctoring-system
   ```

2. **Set up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Configuration**
   * Rename `.env.example` to `.env`
   * Update the `DATABASE_URL` inside `.env` with your PostgreSQL credentials:
     ```env
     DATABASE_URL="postgresql://username:password@localhost/proctoring1_db"
     ```

5. **Run the Server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the Application**
   Open `index.html` or `dashboard.html` in your web browser. Ensure the FastAPI backend is running on `http://127.0.0.1:8000`.

