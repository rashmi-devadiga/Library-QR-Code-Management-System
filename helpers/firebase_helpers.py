import pyrebase
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import cv2
import streamlit as st

from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

def generate_qr_code(book_id):
    qr = qrcode.make(book_id)
    qr_img = qr.convert("RGB")

    width, height = qr_img.size
    new_height = height + 30
    new_img = Image.new("RGB", (width, new_height), "white")
    new_img.paste(qr_img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), book_id, font=font)
    text_width = bbox[2] - bbox[0]
    text_position = ((width - text_width) // 2, height + 5)

    draw.text(text_position, book_id, fill="black", font=font)

    buf = io.BytesIO()
    new_img.save(buf, format="PNG")
    return buf.getvalue()

def get_download_link(image_bytes, filename="qr.png"):
    b64 = base64.b64encode(image_bytes).decode()
    return f'<a href="data:image/png;base64,{b64}" download="{filename}">Download QR</a>'

def scan_qr_code_ui():
    st.write("Initializing scanner. Please hold your QR code in front of the camera...")
    scanned_data = None

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam. Make sure it is connected and not in use by another app.")
        return None

    frame_display = st.empty()
    stop = st.button("Stop Scanner")

    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to grab frame from camera.")
            break

        qr_detector = cv2.QRCodeDetector()
        data, bbox, _ = qr_detector.detectAndDecode(frame)

        if bbox is not None and data:
            n = len(bbox)
            for i in range(n):
                pt1 = tuple(map(int, bbox[i][0]))
                pt2 = tuple(map(int, bbox[(i + 1) % n][0]))
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
            frame_display.image(frame, channels="BGR")
            scanned_data = data
            st.success(f" QR Code Detected: {data}")
            break

        frame_display.image(frame, channels="BGR")

        if stop:
            break

    cap.release()
    cv2.destroyAllWindows()
    return scanned_data
