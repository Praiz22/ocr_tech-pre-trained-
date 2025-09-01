import streamlit as st
import numpy as np
from PIL import Image, ImageFilter
import time
import pandas as pd
import altair as alt

# Load the app’s style
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown("""
    <header class="header">
        <div class="branding">Praix Tech — OCR Lab</div>
        <div class="subtitle">Futuristic UI Prototype • Upload → Preprocess → Predict</div>
    </header>
    <button class="start-demo">Start Demo</button>
""", unsafe_allow_html=True)

# Clean up the image
def clean_image(image):
    image = image.convert('L')  # Grayscale
    image = image.filter(ImageFilter.MedianFilter(size=5))  # Smooth noise
    image_array = np.array(image)
    threshold = 128
    image_array = np.where(image_array < threshold, 0, 255).astype(np.uint8)
    image = Image.fromarray(image_array).resize((128, 128))
    return np.array(image) / 255.0

# Guess image type
def guess_image_type(image):
    text_amount = np.mean(image < 0.5)
    if text_amount > 0.3:
        return "documents", 0.9
    elif text_amount > 0.1:
        return "screenshots", 0.85
    return "pictures", 0.8

# Placeholder text detection
def read_text(image):
    image_array = np.array(image.convert('L'))
    text_amount = np.mean(image_array < 128)
    if text_amount > 0.3:
        return "Text detected (basic analysis)", 0.9
    return "No text found", 0.8

# Upload section
st.markdown('<section class="section-upload card fade-in">', unsafe_allow_html=True)
st.markdown("<h2>Upload Image</h2>", unsafe_allow_html=True)
st.markdown("<p>10s processing budget</p>", unsafe_allow_html=True)
st.markdown("<div class='upload-area'>Drag & Drop an image here or Choose File</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Your Image", use_column_width=True)

    start_time = time.time()
    cleaned_img = clean_image(image)

    # Preprocessing section
    st.markdown('<section class="section-preprocess card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Data Preprocessing</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Processing...</p>", unsafe_allow_html=True)

    steps = ["Noise Removal", "Thresholding", "Deskew", "Normalization"]
    for step in steps:
        step_progress = st.progress(0)
        time.sleep(0.1)
        st.markdown(f"<div class='step'>{step}<span>100%</span><div class='progress-bar full'></div></div>", unsafe_allow_html=True)
        step_progress.progress(1.0)

    st.markdown("<p class='chart-label'>Applied vs Remaining</p>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({"Applied": [70], "Remaining": [30]})
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('variable:N', title=None, axis=alt.Axis(labels=False)),
        y=alt.Y('value:Q', title=None),
        color=alt.Color('variable:N', scale=alt.Scale(range=["#00ff00", "#00ff00"]), legend=None)
    ).transform_melt(
        id_vars=[],
        value_vars=["Applied", "Remaining"]
    ).properties(
        width=200,
        height=100
    )
    st.altair_chart(chart, use_container_width=True)

    st.markdown("<p class='status'>Ready</p>", unsafe_allow_html=True)
    st.image(cleaned_img, caption="Processed Image", use_column_width=True)
    st.markdown('</section>', unsafe_allow_html=True)

    # Results section
    st.markdown('<section class="section-prediction card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Prediction Results</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Analyzing...</p>", unsafe_allow_html=True)

    image_type, type_confidence = guess_image_type(cleaned_img)
    text = "None"
    text_confidence = 0.0
    if image_type == "documents":
        text, text_confidence = read_text(image)
    confidence = type_confidence if image_type != "documents" else text_confidence

    st.markdown(f"<div class='result'>Extracted Text<span>{text}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='result'>Prediction<span>{image_type}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric'>Confidence<span>{confidence * 100:.0f}%</span><div class='progress-bar' style='width: {confidence*100}%'></div></div>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Finished</p>", unsafe_allow_html=True)

    if time.time() - start_time > 10:
        st.warning("Took a bit long; try a smaller image.")
    st.markdown('</section>', unsafe_allow_html=True)
else:
    st.markdown('<section class="section-preprocess card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Data Preprocessing</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Idle</p>", unsafe_allow_html=True)
    for step in ["Noise Removal", "Thresholding", "Deskew", "Normalization"]:
        st.markdown(f"<div class='step'>{step}<span>0%</span><div class='progress-bar empty'></div></div>", unsafe_allow_html=True)
    st.markdown("<p class='chart-label'>Applied vs Remaining</p>", unsafe_allow_html=True)
    chart_data = pd.DataFrame({"Applied": [0], "Remaining": [0]})
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('variable:N', title=None, axis=alt.Axis(labels=False)),
        y=alt.Y('value:Q', title=None),
        color=alt.Color('variable:N', scale=alt.Scale(range=["#00ff00", "#00ff00"]), legend=None)
    ).transform_melt(
        id_vars=[],
        value_vars=["Applied", "Remaining"]
    ).properties(
        width=200,
        height=100
    )
    st.altair_chart(chart, use_container_width=True)
    st.markdown("<p class='status'>Ready</p>", unsafe_allow_html=True)
    st.markdown('</section>', unsafe_allow_html=True)

    st.markdown('<section class="section-prediction card fade-in">', unsafe_allow_html=True)
    st.markdown("<h2>Prediction Results</h2>", unsafe_allow_html=True)
    st.markdown("<p class='status'>Waiting for input</p>", unsafe_allow_html=True)
    st.markdown("<div class='result'>Extracted Text<span>—</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='result'>Prediction<span>—</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='metric'>Confidence<span>0%</span><div class='progress-bar empty'></div></div>", unsafe_allow_html=True)
    st.markdown('</section>', unsafe_allow_html=True)
