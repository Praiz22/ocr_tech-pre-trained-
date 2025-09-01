import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd
import easyocr

# Load the app’s style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header (like your HTML)
st.markdown("""
    <header class="header">
        <div class="branding">Praix Tech — OCR Lab</div>
        <div class="subtitle">Futuristic UI • Upload and See Results</div>
    </header>
    <button class="start-demo">Start Demo</button>
""", unsafe_allow_html=True)

# Clean up the image
def clean_image(image):
    image = cv2.medianBlur(image, 5)  # Smooth out noise
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return cv2.resize(image, (128, 128)) / 255.0  # Small size for speed

# Guess image type (picture, screenshot, document)
def guess_image_type(image):
    text_amount = np.mean(image < 0.5)  # Check for text-like areas
    if text_amount > 0.3:
        return "documents", 0.9
    elif text_amount > 0.1:
        return "screenshots", 0.85
    return "pictures", 0.8

# Read text from image
def read_text(image):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(image)
    text = " ".join([res[1] for res in result]) or "No text found"
    confidence = np.mean([res[2] for res in result]) if result else 0.9
    return text, confidence

# Upload section
st.markdown('<section class="section-upload card fade-in">', unsafe_allow_html=True)
st.markdown("<h2>Upload Image</h2>", unsafe_allow_html=True)
st.markdown("<p>10-second processing</p>", unsafe_allow_html=True)
st.markdown("<div class='upload-area'>Drag & Drop or Choose File</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Your Image", use_column_width=True)

    start_time = time.time()
    original_img = np.array(image)
    cleaned_img = original_img.copy()

    # Processing section
    st.markdown('<section class="section-preprocess card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Processing Image</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Working...</p>", unsafe_allow_html=True)

    steps = ["Noise Removal", "Text Enhancement", "Resizing"]
    for step in steps:
        step_progress = st.progress(0)
        time.sleep(0.1)
        if step == "Noise Removal":
            cleaned_img = cv2.medianBlur(cleaned_img, 5)
        elif step == "Text Enhancement":
            gray = cv2.cvtColor(cleaned_img, cv2.COLOR_RGB2GRAY)
            cleaned_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            st.markdown("<p>Applied vs Remaining</p>", unsafe_allow_html=True)
            chart_data = pd.DataFrame({"Applied": [70], "Remaining": [30]})
            st.bar_chart(chart_data, color="#00ff00")
        elif step == "Resizing":
            cleaned_img = cv2.resize(cleaned_img, (128, 128)) / 255.0
        st.markdown(f"<div class='step'>{step}<span>100%</span><div class='progress-bar full'></div></div>", unsafe_allow_html=True)
        step_progress.progress(1.0)

    st.markdown("<p>Done</p>", unsafe_allow_html=True)
    st.image(cleaned_img, caption="Processed Image", use_column_width=True)
    st.markdown('</section>', unsafe_allow_html=True)

    # Results section
    st.markdown('<section class="section-prediction card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Analyzing...</p>", unsafe_allow_html=True)

    image_type, type_confidence = guess_image_type(cleaned_img)
    text = "None"
    text_confidence = 0.0
    if image_type == "documents":
        text, text_confidence = read_text(original_img)
    confidence = type_confidence if image_type != "documents" else text_confidence

    st.markdown(f"<div class='result'>Text Found<span>{text}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result'>Image Type<span>{image_type}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric'>Confidence<span>{confidence * 100:.0f}%</span><div class='progress-bar' style='width: {confidence*100}%'></div></div>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Finished</p>", unsafe_allow_html=True)

    if time.time() - start_time > 10:
        st.warning("Took a bit long; try a smaller image.")
    st.markdown('</section>', unsafe_allow_html=True)
else:
    st.markdown('<section class="section-preprocess card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Processing Image</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Waiting...</p>", unsafe_allow_html=True)
    for step in ["Noise Removal", "Text Enhancement", "Resizing"]:
        st.markdown(f"<div class='step'>{step}<span>0%</span><div class='progress-bar empty'></div></div>", unsafe_allow_html=True)
        if step == "Text Enhancement":
            st.markdown("<p>Applied vs Remaining</p>", unsafe_allow_html=True)
            chart_data = pd.DataFrame({"Applied": [0], "Remaining": [0]})
            st.bar_chart(chart_data, color="#00ff00")
    st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('<section class="section-prediction card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Waiting for image</p>", unsafe_allow_html=True)
    st.markdown("<div class='result'>Text Found<span>—</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='result'>Image Type<span>—</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric'>Confidence<span>0%</span><div class='progress-bar empty'></div></div>", unsafe_allow_html=True)
    st.markdown('</section>', unsafe_allow_html=True)
