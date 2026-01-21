import streamlit as st
import cv2
import time
import os
import pandas as pd
from datetime import datetime

from dnn_detector import detect_faces

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="InvigilateAI", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>InvigilateAI</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; opacity:0.65;'>Smart Exam Supervision System</p>",
    unsafe_allow_html=True
)

# ---------------- FOLDERS ----------------
os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

# ---------------- SESSION STATE ----------------
if "run" not in st.session_state:
    st.session_state.run = False
if "cap" not in st.session_state:
    st.session_state.cap = None
if "log" not in st.session_state:
    st.session_state.log = []
if "absent_frames" not in st.session_state:
    st.session_state.absent_frames = 0
if "last_screenshot" not in st.session_state:
    st.session_state.last_screenshot = 0

# ---------------- SIDEBAR (ADMIN CONSOLE) ----------------
st.sidebar.markdown("## 🛠 Admin Console")

MODE = st.sidebar.radio(
    "Monitoring Mode",
    ["Exam Mode", "Debug Mode"],
    help="Exam Mode hides technical info. Debug Mode shows internal counters."
)

ABSENCE_TOLERANCE = st.sidebar.slider(
    "Movement Sensitivity", 10, 80, 40
)

SCREENSHOT_GAP = st.sidebar.slider(
    "Violation Evidence Interval (sec)", 3, 15, 6
)

if st.sidebar.button("▶ Start Monitoring"):
    st.session_state.cap = cv2.VideoCapture(0)
    st.session_state.run = True
    st.session_state.log = []
    st.session_state.absent_frames = 0
    st.session_state.last_screenshot = 0

if st.sidebar.button("⏹ End Monitoring"):
    st.session_state.run = False
    if st.session_state.cap:
        st.session_state.cap.release()
        st.session_state.cap = None

# ---------------- MAIN VIEW ----------------
frame_box = st.empty()

if st.session_state.run and st.session_state.cap:
    cap = st.session_state.cap

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.error("Camera not accessible")
            break

        faces = detect_faces(frame)
        now = time.time()
        timestamp = datetime.now().strftime("%H:%M:%S")

        # -------- STATUS LOGIC --------
        if len(faces) > 0:
            status = "PRESENT"
            st.session_state.absent_frames = 0
            color = (0, 180, 0)
        else:
            st.session_state.absent_frames += 1
            if st.session_state.absent_frames > ABSENCE_TOLERANCE:
                status = "ABSENT"
                color = (0, 0, 255)

                if now - st.session_state.last_screenshot > SCREENSHOT_GAP:
                    fname = f"screenshots/absent_{datetime.now().strftime('%H%M%S')}.jpg"
                    cv2.imwrite(fname, frame)
                    st.session_state.last_screenshot = now
            else:
                status = "RECOVERING"
                color = (255, 170, 0)

        # -------- LOGGING --------
        st.session_state.log.append({
            "Time": timestamp,
            "Status": status,
            "Faces": len(faces)
        })

        # -------- DRAWING --------
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)

        # Subtle status indicator (no clutter)
        if status == "PRESENT":
            text = "● Present"
        elif status == "RECOVERING":
            text = "▲ Face temporarily lost"
        else:
            text = "■ Absent"

        cv2.putText(
            frame,
            text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )

        # -------- DEBUG MODE OVERLAY --------
        if MODE == "Debug Mode":
            cv2.putText(
                frame,
                f"Faces: {len(faces)} | Absent Frames: {st.session_state.absent_frames}",
                (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1
            )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_box.image(frame, use_container_width=True)

        time.sleep(0.03)

else:
    st.info("Monitoring inactive. Start session to begin supervision.")

# ---------------- SESSION SUMMARY ----------------
if not st.session_state.run and len(st.session_state.log) > 0:

    df = pd.DataFrame(st.session_state.log)

    log_file = f"logs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(log_file, index=False)

    st.success("✅ Monitoring Session Completed")

    st.subheader("📄 Session Summary")
    st.markdown(f"**Log File:** `{log_file}`")
    st.markdown("**Evidence:** Screenshots saved in `screenshots/` folder")

    st.subheader("📊 Session Log Preview")
    st.dataframe(df.tail(20), use_container_width=True)

    st.download_button(
        label="⬇️ Download Session CSV",
        data=df.to_csv(index=False),
        file_name=os.path.basename(log_file),
        mime="text/csv"
    )