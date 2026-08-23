import streamlit as st
import cv2
import time
import os
import pandas as pd
from datetime import datetime

from dnn_detector import detect_faces

st.set_page_config(
    page_title="InvigilateAI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: #080d14;
}

[data-testid="stSidebar"] {
    background: #0d141d;
    border-right: 1px solid #263342;
}

.hero {
    padding: 18px 0 22px 0;
    border-bottom: 1px solid #263342;
    margin-bottom: 22px;
}

.hero h1 {
    margin: 0;
    font-size: 2.4rem;
    font-weight: 750;
    letter-spacing: -1px;
}

.hero p {
    color: #91a0af;
    margin: 5px 0 0 0;
}

.live {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 20px;
    background: #10251d;
    color: #5ee59a;
    border: 1px solid #245d43;
    font-size: 0.78rem;
    font-weight: 700;
}

.card {
    background: #101720;
    border: 1px solid #263342;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 14px;
}

.card-title {
    color: #91a0af;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.card-value {
    font-size: 1.55rem;
    font-weight: 750;
    margin-top: 4px;
}

.present {
    color: #5ee59a;
}

.recovering {
    color: #f5b84b;
}

.absent {
    color: #ff6b6b;
}

.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin: 12px 0 8px 0;
}

[data-testid="stMetric"] {
    background: #101720;
    border: 1px solid #263342;
    padding: 14px;
    border-radius: 12px;
}

.stButton button {
    border-radius: 9px;
    font-weight: 700;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <span class="live">● SYSTEM READY</span>
    <h1>🛡️ InvigilateAI</h1>
    <p>Smart Exam Supervision System · Computer Vision Monitoring</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FOLDERS ----------------

os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

# ---------------- SESSION STATE ----------------

defaults = {
    "run": False,
    "cap": None,
    "log": [],
    "absent_frames": 0,
    "last_screenshot": 0,
    "session_start": None,
    "evidence_count": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🎛️ Control Center")
    st.caption("Configure monitoring session")

    MODE = st.radio(
        "Monitoring Mode",
        ["Exam Mode", "Debug Mode"]
    )

    ABSENCE_TOLERANCE = st.slider(
        "Movement Sensitivity",
        10,
        80,
        40
    )

    SCREENSHOT_GAP = st.slider(
        "Evidence Interval (sec)",
        3,
        15,
        6
    )

    st.divider()

    start = st.button(
        "▶ Start Monitoring",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.run
    )

    end = st.button(
        "■ End Monitoring",
        use_container_width=True,
        disabled=not st.session_state.run
    )

    if start:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera could not be opened. Check camera permissions.")
        else:
            st.session_state.cap = cap
            st.session_state.run = True
            st.session_state.log = []
            st.session_state.absent_frames = 0
            st.session_state.last_screenshot = 0
            st.session_state.session_start = datetime.now()
            st.session_state.evidence_count = 0
            st.rerun()

    if end:
        st.session_state.run = False

        if st.session_state.cap:
            st.session_state.cap.release()
            st.session_state.cap = None

        st.rerun()

    st.divider()
    st.caption("InvigilateAI v1.0")
    st.caption("Local / controlled environment")

# ---------------- METRICS ----------------

present_count = sum(
    x["Status"] == "PRESENT"
    for x in st.session_state.log
)

recovering_count = sum(
    x["Status"] == "RECOVERING"
    for x in st.session_state.log
)

absent_count = sum(
    x["Status"] == "ABSENT"
    for x in st.session_state.log
)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Session", "LIVE" if st.session_state.run else "READY")

with m2:
    st.metric("Present Records", present_count)

with m3:
    st.metric("Recovering", recovering_count)

with m4:
    st.metric("Absence Events", absent_count)

st.markdown("### 🎥 Live Monitoring")

left, right = st.columns([2.7, 1])

with left:
    frame_box = st.empty()

with right:
    st.markdown(
        '<div class="section-title">Session Overview</div>',
        unsafe_allow_html=True
    )

    status_box = st.empty()
    info_box = st.empty()

    if not st.session_state.run:
        status_box.info("Monitoring inactive")
        info_box.caption("Start a session from the Control Center.")

# ---------------- MONITORING ----------------

if st.session_state.run and st.session_state.cap:

    cap = st.session_state.cap

    while st.session_state.run:

        ret, frame = cap.read()

        if not ret:
            st.error("Camera is not accessible.")
            st.session_state.run = False
            cap.release()
            st.session_state.cap = None
            break

        faces = detect_faces(frame)

        now = time.time()
        timestamp = datetime.now().strftime("%H:%M:%S")

        # -------- STATUS --------

        if len(faces) > 0:

            status = "PRESENT"
            st.session_state.absent_frames = 0
            color = (0, 190, 90)

        else:

            st.session_state.absent_frames += 1

            if st.session_state.absent_frames > ABSENCE_TOLERANCE:

                status = "ABSENT"
                color = (40, 40, 235)

                if now - st.session_state.last_screenshot > SCREENSHOT_GAP:

                    fname = (
                        f"screenshots/"
                        f"absent_{datetime.now().strftime('%H%M%S')}.jpg"
                    )

                    cv2.imwrite(fname, frame)

                    st.session_state.last_screenshot = now
                    st.session_state.evidence_count += 1

            else:

                status = "RECOVERING"
                color = (255, 170, 0)

        # -------- LOGGING --------

        st.session_state.log.append({
            "Time": timestamp,
            "Status": status,
            "Faces": len(faces)
        })

        # -------- FACE BOXES --------

        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                color,
                2
            )

        # -------- CAMERA STATUS --------

        if status == "PRESENT":
            text = "● PRESENT"

        elif status == "RECOVERING":
            text = "▲ RECOVERING"

        else:
            text = "■ ABSENT"

        cv2.putText(
            frame,
            text,
            (20, 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            2
        )

        if MODE == "Debug Mode":

            cv2.putText(
                frame,
                f"Faces: {len(faces)} | "
                f"Absent Frames: {st.session_state.absent_frames}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1
            )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        frame_box.image(
            frame,
            use_container_width=True
        )

        # -------- RIGHT PANEL --------

        if status == "PRESENT":

            status_box.markdown(
                '<div class="card">'
                '<div class="card-title">Current Status</div>'
                '<div class="card-value present">● PRESENT</div>'
                '</div>',
                unsafe_allow_html=True
            )

        elif status == "RECOVERING":

            status_box.markdown(
                '<div class="card">'
                '<div class="card-title">Current Status</div>'
                '<div class="card-value recovering">▲ RECOVERING</div>'
                '</div>',
                unsafe_allow_html=True
            )

        else:

            status_box.markdown(
                '<div class="card">'
                '<div class="card-title">Current Status</div>'
                '<div class="card-value absent">■ ABSENT</div>'
                '</div>',
                unsafe_allow_html=True
            )

        info_box.metric(
            "Detected Faces",
            len(faces)
        )

        st.session_state.log = st.session_state.log[-5000:]

        time.sleep(0.03)

# ---------------- SESSION SUMMARY ----------------

if (
    not st.session_state.run
    and len(st.session_state.log) > 0
):

    df = pd.DataFrame(
        st.session_state.log
    )

    log_file = (
        f"logs/session_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    df.to_csv(
        log_file,
        index=False
    )

    st.divider()

    st.markdown("### 📊 Session Summary")

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("Records", len(df))

    with s2:
        st.metric(
            "Present",
            int((df["Status"] == "PRESENT").sum())
        )

    with s3:
        st.metric(
            "Recovering",
            int((df["Status"] == "RECOVERING").sum())
        )

    with s4:
        st.metric(
            "Evidence",
            st.session_state.evidence_count
        )

    st.dataframe(
        df.tail(20),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download Session CSV",
        data=df.to_csv(index=False),
        file_name=os.path.basename(log_file),
        mime="text/csv"
    )
