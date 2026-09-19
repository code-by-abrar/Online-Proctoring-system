# 🛡️ SecureExam AI — Advanced Automated Online Exam Proctoring System

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-Client%20AI-FF6F00.svg?style=for-the-badge&logo=tensorflow)](https://js.tensorflow.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791.svg?style=for-the-badge&logo=postgresql)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

**A secure, intelligent, and scalable online examination proctoring platform actively detecting cheating, unauthorized devices, and eye diversion in real-time.**

</div>

---

## 📌 Overview

**SecureExam AI** combines client-side browser Web AI with a robust asynchronous FastAPI backend to ensure academic integrity during unproctored online assessments.

---

## ⚡ Multimodal Cheating Prevention Suite

- **👀 Real-Time Face & Gaze Tracking**: Powered by `BlazeFace` (TensorFlow.js) detecting when candidates look away or if multiple faces appear in frame.
- **📱 Unauthorized Device Detection**: Uses `COCO-SSD` to flag smartphones, tablets, or unauthorized study materials.
- **🎙️ Background Whispering & Audio Monitor**: Web Audio API frequency analysis flags suspicious voices or background conversations.
- **🔒 Anti-Tab Switch Guard**: Browser visibility API flags tab switching or application minimizing with immediate penalty strikes.
- **👨‍💼 Proctor / Admin Dashboard**: Real-time review portal for invigilators with automated violation logs.

---

## 🛠️ Setup & Execution

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Database & Environment**:
   ```env
   DATABASE_URL=postgresql://postgres:password@localhost:5432/proctoring_db
   ```

3. **Start the Platform**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. Access student portal at `http://localhost:8000/student_login_signup.html`.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.
