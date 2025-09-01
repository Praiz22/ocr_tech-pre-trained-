import streamlit as st
import numpy as np
from PIL import Image
import time
from utils import clean_image, guess_image_type, perform_ocr

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
if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False
if 'show_upload' not in st.session_state:
    st.session_state.show_upload = False

# Load the app’s style from an external CSS file
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main wrapper for the gradient background
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="glow"></div>', unsafe_allow_html=True)

# Hero Section
st.markdown("""
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

# Main app grid layout
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

# Placeholder for the uploaded image preview
if st.session_state.uploaded_file:
    st.markdown('<section class="card col-12 fade-in"><h3>Image Preview</h3></section>', unsafe_allow_html=True)
    image = Image.open(st.session_state.uploaded_file)
    st.image(image, caption="Your Uploaded Image", use_column_width=True)

# Preprocessing Panel (Column 8)
with st.container():
    st.markdown(f"""
        <section class="card col-8 fade-in delay">
            <div class="head">
                <h3>Data Preprocessing</h3>
                <span class="soft-accent" id="preStatus">{st.session_state.status_pre}</span>
            </div>
    """, unsafe_allow_html=True)

    status_placeholder = st.empty()
    image_placeholder = st.empty()
    
    if st.session_state.uploaded_file:
        status_placeholder.markdown("<p>Processing...</p>")
        image = Image.open(st.session_state.uploaded_file).convert('RGB')
        
        # Simulate processing steps with animation
        with st.spinner("Step 1: Noise Removal..."):
            time.sleep(1)
        
        with st.spinner("Step 2: Binarization..."):
            cleaned_img_array, threshold_val = clean_image(image)
        
        st.session_state.threshold_value = int(threshold_val * 100)
        
        status_placeholder.markdown("<p>Ready</p>")
        
        st.markdown(f"""
            <div class="metrics">
                <div class="metric">
                    <div class="row"><span class="label">Noise Removal</span><span class="value">100%</span></div>
                    <div class="bar"><i style="width: 100%;"></i></div>
                </div>
                <div class="metric">
                    <div class="row"><span class="label">Thresholding</span><span class="value">{st.session_state.threshold_value}%</span></div>
                    <div class="bar"><i style="width: {st.session_state.threshold_value}%;"></i></div>
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
        
        # Perform OCR and image classification
        cleaned_img_array, _ = clean_image(image)
        text = perform_ocr(cleaned_img_array)
        label, confidence = guess_image_type(image)
        
        # Update session state with results
        st.session_state.status_pred = "Finished"
        st.session_state.ocr_text = text if text else "No text found."
        st.session_state.pred_label = label
        st.session_state.confidence = int(confidence * 100)

    st.rerun()

# How-to Demo Modal
st.markdown("""
<div class="modal-overlay" id="modal">
    <div class="modal">
        <div class="modal-header">
            <h3>How to Use</h3>
            <span class="modal-close-btn">&times;</span>
        </div>
        <div class="modal-body">
            <p><strong>1. Upload Image:</strong> Click 'Choose File' or drag and drop an image of a document or text.</p>
            <p><strong>2. Watch it Process:</strong> The app will show a live-action stream of data preprocessing and analysis.</p>
            <p><strong>3. See the Results:</strong> The final extracted text, a predicted document type, and a confidence score will be displayed.</p>
            <div class="animated-dots">
                <span></span><span></span><span></span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add JavaScript to link the custom buttons and styling to the Streamlit components
st.markdown("""
<script>
    const filePicker = parent.document.querySelector('.stFileUploader > div > label > button');
    const pickFileButton = document.querySelector('.pick-file');
    const dropZone = document.querySelector('.drop');
    const startDemoButton = document.querySelector('.start-demo');
    const modal = document.getElementById('modal');
    const modalCloseBtn = document.querySelector('.modal-close-btn');

    if (filePicker && pickFileButton) {
        pickFileButton.onclick = () => {
            filePicker.click();
        };
    }

    if (dropZone && filePicker) {
        dropZone.ondragover = (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        };

        dropZone.ondragleave = () => {
            dropZone.classList.remove('dragover');
        };

        dropZone.ondrop = (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            // Streamlit handles the file via the hidden input
        };
    }

    if (startDemoButton) {
        startDemoButton.onclick = () => {
            modal.style.display = "block";
        };
    }

    if (modalCloseBtn) {
        modalCloseBtn.onclick = () => {
            modal.style.display = "none";
        };
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
</script>
""", unsafe_allow_html=True)
