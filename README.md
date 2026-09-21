# InvigilateAI

> AI-Based Smart Exam Supervision System using Computer Vision.

InvigilateAI is a computer-vision based examination monitoring system designed to monitor candidate face presence during online or controlled examinations.

## Features

- Real-time webcam monitoring
- Face detection using OpenCV DNN
- Present, Recovering and Absent status detection
- Automatic evidence screenshots
- Session-wise CSV logging
- Exam Mode and Debug Mode
- Configurable monitoring sensitivity
- Downloadable session reports

## Tech Stack

- Python
- OpenCV
- OpenCV DNN
- Streamlit
- NumPy
- Pandas

## How It Works

Webcam -> Frame Capture -> Face Detection -> Presence Analysis -> Evidence Capture -> Session Logging.

## Project Structure

``text
InvigilateAi/
|-- app.py
|-- dnn_detector.py
|-- requirements.txt
|-- README.md
|-- .gitignore

`` 

## Installation

``bash
git clone https://github.com/adi03-oist/InvigilateAi.git
cd InvigilateAi
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
`` 

## Monitoring Workflow

1. Launch InvigilateAI.
2. Select monitoring mode.
3. Adjust sensitivity and evidence interval.
4. Start monitoring.
5. The system analyzes webcam frames.
6. Face presence is classified as Present, Recovering or Absent.
7. Continuous absence can trigger evidence capture.
8. End the session to generate the summary.
9. Download the session CSV.

## Outputs

Runtime logs are saved inside the logs folder and evidence screenshots inside the screenshots folder. These files are excluded from GitHub using .gitignore.

## Limitations

InvigilateAI is designed primarily for local or controlled environments where webcam access is available. Public cloud deployment may have browser webcam limitations.

This project is an academic and portfolio prototype and should not be considered a certified examination proctoring system.

## Monitoring Events

The current system records:

- Candidate presence
- Temporary face loss / recovery
- Continuous absence
- Multiple-face detection
- Evidence capture
- Session-wise event timestamps

Each monitoring session receives a unique Session ID for traceability.

## Future Scope

- Candidate identity verification
- Multi-face detection and alerts
- Head-pose and gaze analysis
- Advanced suspicious-activity detection
- Analytics dashboard
- Database-backed session management
- Role-based administrator access

## Project Status

Active Development

## Author

Aaditya Jain - CSE (Data Science), OIST Bhopal

## License

Educational and demonstration purposes.

