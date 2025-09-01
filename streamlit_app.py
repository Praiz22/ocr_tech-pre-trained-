import streamlit as st
import numpy as np
from PIL import Image
import pandas as pd
import altair as alt
import time
from utils import clean_image, guess_image_type

# Initialize session state for UI management
if 'status_pre' not in st.session_state:
    st.session_state.status_pre = "Waiting for input"
if 'status_pred' not in st.session_state:
    st.session_state.status_pred = "Waiting for input"
if 'ocr_text' not in st.session_state:
    st.session_state.ocr_text = "—"
if 'pred_label' not in st.session_state:
    st.session_state.pred_label = "—"
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'threshold_value' not in st.session_state:
    st.session_state.threshold_value = 0

# Load the app’s style from an external CSS file
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="glow"></div>
    <div class="shell">
        <div class="hero fade-in">
            <div class="brand">
                <div class="logo"></div>
                <div>
                    <div class="title">Praix Tech — OCR Lab</div>
                    <div class="subtitle">Futuristic UI Prototype • Upload → Preprocess → Predict</div>
                </div>
            </div>
            <button class="btn start-demo">Start Demo</button>
        </div>
    </div>
""", unsafe_allow_html=True)

# Grid layout
st.markdown('<div class="grid">', unsafe_allow_html=True)

# Upload Panel (Column 12)
with st.container():
    st.markdown("""
        <section class="card col-12 fade-in">
            <div class="head">
                <h3>Upload Image</h3>
                <span class="soft-accent">10s processing budget</span>
            </div>
            <div class="drop">
                <p><strong>Drag & Drop</strong> an image here or <button class="btn pick-file">Choose File</button></p>
            </div>
        </section>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

# Preprocessing Panel (Column 8)
with st.container():
    st.markdown(f"""
        <section class="card col-8 fade-in delay">
            <div class="head">
                <h3>Data Preprocessing</h3>
                <span class="soft-accent" id="preStatus">{st.session_state.status_pre}</span>
            </div>
    """, unsafe_allow_html=True)

    st.session_state.status_container = st.empty()
    
    # Placeholder for displaying the processed image
    if st.session_state.uploaded_file:
        image = Image.open(st.session_state.uploaded_file).convert('RGB')
        
        with st.spinner("Processing..."):
            cleaned_img_array = clean_image(image)
        
        chart_data = pd.DataFrame({
            "Applied": [st.session_state.threshold_value],
            "Remaining": [100 - st.session_state.threshold_value]
        })
        
        chart = alt.Chart(chart_data).mark_arc(outerRadius=50).encode(
            theta=alt.Theta("value", stack=True),
            color=alt.Color("variable", scale=alt.Scale(range=["#ff7a18", "#f0f0f0"])),
        ).properties(width=120, height=120)
        
        st.markdown(f"""
            <div class="metrics">
                <div class="metric">
                    <div class="row"><span class="label">Noise Removal</span><span class="value">100%</span></div>
                    <div class="bar"><i style="width: 100%;"></i></div>
                </div>
                <div class="metric chart-card">
                    <div class="row" style="width:100%;justify-content:space-between;align-items:center;">
                        <span class="label">Thresholding</span><span class="value">{st.session_state.threshold_value}%</span>
                    </div>
                    <div class="chart-wrap">
                        <div id="thresholdChart"></div>
                    </div>
                </div>
                <div class="metric">
                    <div class="row"><span class="label">Deskew</span><span class="value">100%</span></div>
                    <div class="bar"><i style="width: 100%;"></i></div>
                </div>
                <div class="metric">
                    <div class="row"><span class="label">Normalization</span><span class="value">100%</span></div>
                    <div class="bar"><i style="width: 100%;"></i></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.altair_chart(chart)

        st.image(cleaned_img_array, caption="Processed Image", use_column_width=True)
    
    st.markdown('</section>', unsafe_allow_html=True)

# Prediction Results Panel (Column 12)
with st.container():
    st.markdown(f"""
        <section class="card col-12 fade-in delay">
            <div class="head">
                <h3>Prediction Results</h3>
                <span class="soft-accent" id="predStatus">{st.session_state.status_pred}</span>
            </div>
            <div class="grid" style="gap:16px">
                <div class="col-8">
                    <div class="result">
                        <span class="tag soft-accent">Extracted Text</span>
                        <div class="mono" id="ocrText">{st.session_state.ocr_text}</div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="result">
                        <span class="tag soft-accent">Prediction</span>
                        <div class="mono"><strong id="predLabel">{st.session_state.pred_label}</strong></div>
                        <div class="confidence">
                            <div class="row"><span class="label">Confidence</span><span class="value" id="confVal">{st.session_state.confidence}%</span></div>
                            <div class="bar"><i id="confBar" style="width: {st.session_state.confidence}%;"></i></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    """, unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# Run the prediction pipeline on file upload
if st.session_state.uploaded_file:
    with st.spinner("Running inference..."):
        image = Image.open(st.session_state.uploaded_file).convert('RGB')
        cleaned_img_array = clean_image(image)
        
        # Get predictions without a model
        text = "Hello Praix - Futuristic OCR UI 💫"
        label = "Document"
        confidence = 0.93
        
        # Update session state with results
        st.session_state.status_pred = "Finished"
        st.session_state.ocr_text = text
        st.session_state.pred_label = label
        st.session_state.confidence = int(confidence * 100)

    st.rerun()
