# InvigilateAI – Smart Exam Supervision System

InvigilateAI is an AI-based exam supervision system designed to monitor candidates during online examinations using real-time face detection.  
The system focuses on **clean monitoring**, **absence detection**, and **session logging**, following real-world proctoring principles.

---

## 🚀 Features

- Real-time face detection using OpenCV DNN
- Movement tolerance to avoid false absence alerts
- Automatic absence detection after continuous face loss
- Evidence capture through automatic screenshots
- Session-wise CSV logging for monitoring records
- Minimal and distraction-free exam-style interface
- Separate Exam Mode and Debug Mode

---

## 🧠 How It Works

1. Start monitoring from the Admin Console  
2. The system continuously checks face presence  
3. Small movements are ignored using tolerance logic  
4. Continuous absence is marked as a violation  
5. Screenshots are captured as evidence  
6. Session data is saved automatically in CSV format  

---

## 🛠 Tech Stack

- Python  
- OpenCV (DNN Face Detector)  
- Streamlit  
- NumPy  
- Pandas  

---

## 📂 Project Structure
InvigilateAI/ │ ├── app.py ├── dnn_detector.py ├── requirements.txt ├── README.md ├── .gitignore │ ├── models/ │   ├── deploy.prototxt │   └── res10_300x300_ssd_iter_140000.caffemodel
Copy code

---

## ▶️ How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Run the application
Copy code
Bash
streamlit run app.py
3. Usage
Click Start Monitoring to begin supervision
Monitor face presence in real time
Click End Monitoring to generate session logs
📊 Output
Session logs are saved automatically as CSV files
Screenshots are captured during absence violations
Logs and screenshots are excluded from GitHub for privacy
☁️ Deployment Note
Due to browser security restrictions, direct webcam access is not supported on public cloud platforms.
The application can be deployed publicly for UI and workflow demonstration
Real-time camera monitoring is intended for local or controlled environments
This reflects real-world exam proctoring system constraints.
🎯 Use Cases
Online examinations
Interview monitoring
Controlled remote assessments
AI-based supervision demonstrations
🔮 Future Enhancements
Candidate identity verification
Multi-face detection alerts
Advanced analytics dashboard
Cloud-based evidence storage
👨‍💻 Author
Developed as an academic and portfolio project to demonstrate applied computer vision and system design.
📜 License
This project is intended for educational and demonstration purposes.
