import streamlit as st
import base64
import time

# --- UI and Styling ---
# This section contains the raw HTML and CSS from the UI prototype.
# It is injected into the Streamlit app using st.markdown.
# We are placing it here at the top for clarity and to keep the styling together.
# This approach allows us to use custom, non-Streamlit UI components while
# still leveraging the Streamlit backend.

custom_ui_html = """
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Praix Tech — OCR UI Prototype</title>
<!-- Chart.js CDN for pie chart -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>

<style>
  :root {
    --bg-1: #ffffff;
    --bg-2: #fff5eb;
    --bg-3: #ffe7cc;
    --card-bg: rgba(255, 255, 255, 0.24);
    --card-border: rgba(255, 255, 255, 0.36);
    --card-shadow: 0 18px 44px rgba(0, 0, 0, 0.28);
    --text-1: #1f1f1f;
    --text-2: #5a5a5a;
    --brand: #ff7a18;
    --brand-2: #ff4d00;
    --muted: #e9e9e9;
    --success: #0aa574;
    --warning: #d97a00;
    --radius-xl: 22px;
    --radius-lg: 18px;
    --radius-md: 14px;
    --radius-sm: 8px;
  }
  
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: "Inter", sans-serif;
  }
  
  body {
    background-color: var(--bg-1);
    background-image: radial-gradient(circle at 12% 16%, var(--bg-2) 10%, transparent 60%),
                     radial-gradient(circle at 86% 83%, var(--bg-3) 20%, transparent 60%);
    min-height: 100vh;
    padding: 24px;
    color: var(--text-1);
    font-size: 14px;
    line-height: 1.4;
  }
  
  .main-wrapper {
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }
  
  .grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 24px;
  }

  .col-12 { grid-column: span 12; }
  .col-8 { grid-column: span 8; }
  .col-4 { grid-column: span 4; }
  .col-6 { grid-column: span 6; }
  .col-5 { grid-column: span 5; }
  .col-7 { grid-column: span 7; }
  
  @media (max-width: 768px) {
    .grid { gap: 16px; }
    .col-12, .col-8, .col-6, .col-5, .col-4, .col-7 {
      grid-column: span 12;
    }
  }
  
  .card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-xl);
    padding: 24px;
    box-shadow: var(--card-shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 22px 50px rgba(0,0,0,0.35);
  }
  
  .head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .head h3 {
    font-size: 18px;
    font-weight: 600;
  }
  
  .soft-accent {
    color: var(--text-2);
    font-size: 13px;
  }
  
  .drop {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px dashed var(--muted);
    border-radius: var(--radius-lg);
    padding: 40px 20px;
    text-align: center;
    color: var(--text-2);
    transition: border-color 0.3s ease;
  }
  
  .drop.dragover {
    border-color: var(--brand);
    background-color: rgba(255, 122, 24, 0.08);
  }
  
  .btn {
    background-color: var(--brand);
    color: white;
    padding: 10px 20px;
    border-radius: var(--radius-md);
    border: none;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background-color 0.2s ease, transform 0.2s ease;
  }
  
  .btn:hover {
    background-color: var(--brand-2);
    transform: translateY(-1px);
  }
  
  .btn.start-demo {
    padding: 12px 28px;
    border-radius: var(--radius-lg);
    font-size: 16px;
    margin-top: 24px;
  }
  
  .hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 60px 24px;
    border-radius: var(--radius-xl);
    border: 1px solid var(--card-border);
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    box-shadow: var(--card-shadow);
  }
  
  .brand {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .brand .logo {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: var(--brand);
    position: relative;
    box-shadow: 0 0 15px rgba(255, 122, 24, 0.6);
  }
  
  .brand .title {
    font-size: 24px;
    font-weight: 700;
  }
  
  .brand .subtitle {
    font-size: 14px;
    color: var(--text-2);
    margin-top: 4px;
  }
  
  .result {
    margin-bottom: 24px;
  }
  
  .result .tag {
    display: inline-block;
    background-color: var(--muted);
    padding: 4px 10px;
    border-radius: var(--radius-sm);
    margin-bottom: 8px;
    font-size: 12px;
  }
  
  .mono {
    font-family: monospace;
    font-size: 16px;
    background-color: #f5f5f5;
    padding: 16px;
    border-radius: var(--radius-md);
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  
  .image-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: var(--radius-md);
    padding: 20px;
  }
  
  .responsive-image {
    max-width: 100%;
    height: auto;
    border-radius: var(--radius-sm);
  }
  
  .metrics, .confidence {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .bar {
    height: 8px;
    background-color: var(--muted);
    border-radius: 4px;
  }
  
  .bar i {
    display: block;
    height: 100%;
    background-color: var(--brand);
    border-radius: 4px;
    transition: width 0.5s ease;
  }
  
  .fade-in {
    opacity: 0;
    animation: fadeIn 0.8s forwards;
  }
  
  .fade-in.delay {
    animation-delay: 0.3s;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(5px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s forwards;
  }
  
  .modal {
    background: var(--card-bg);
    backdrop-filter: blur(15px);
    border: 1px solid var(--card-border);
    border-radius: var(--radius-xl);
    padding: 32px;
    box-shadow: var(--card-shadow);
    max-width: 500px;
    width: 90%;
    animation: scaleIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .modal-header h3 {
    font-size: 20px;
    font-weight: 700;
  }
  
  .modal-close-btn {
    font-size: 28px;
    color: var(--text-2);
    cursor: pointer;
  }
  
  .modal-body p {
    margin-bottom: 12px;
  }
  
  .animated-dots span {
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: var(--brand);
    border-radius: 50%;
    margin: 0 4px;
    animation: pulse 1.4s infinite ease-in-out both;
  }
  
  .animated-dots span:nth-child(1) { animation-delay: -0.32s; }
  .animated-dots span:nth-child(2) { animation-delay: -0.16s; }
  .animated-dots span:nth-child(3) { animation-delay: 0s; }
  
  @keyframes pulse {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
  }

  .chart-container {
      position: relative;
      height: 200px;
      margin-bottom: 24px;
  }

</style>
"""

# The JavaScript from the prototype, adjusted to work with Streamlit.
# Instead of dummy data, it will be used to show/hide sections based on
# Streamlit's session state.
custom_js = """
<script>
  function showSection(selector) {
    const el = document.querySelector(selector);
    if (el) el.style.display = 'block';
  }
  
  function hideSection(selector) {
    const el = document.querySelector(selector);
    if (el) el.style.display = 'none';
  }
  
  function setText(selector, text) {
    const el = document.querySelector(selector);
    if (el) el.innerText = text;
  }
  
  function setBar(selector, value) {
    const el = document.querySelector(selector);
    if (el) el.style.width = `${value}%`;
  }
</script>
"""

# --- Streamlit App Logic ---

# We use st.session_state to persist data across reruns of the app
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
    st.session_state.processing_state = 0 # 0: idle, 1: processing, 2: done
    st.session_state.extracted_text = "—"
    st.session_state.prediction_label = "—"
    st.session_state.confidence_score = 0
    st.session_state.image_bytes = None
    st.session_state.show_hero = True

# We use an empty container to hold all our custom UI components,
# giving us more control over the layout.
main_container = st.container()

with main_container:
    # --- Inject the Hero section with a Streamlit button ---
    st.markdown(custom_ui_html, unsafe_allow_html=True)
    
    if st.session_state.show_hero:
        # We need a Streamlit button to handle state changes reliably
        st.markdown("""
        <div class="hero fade-in">
          <div class="brand">
            <div class="logo"></div>
            <div>
              <div class="title">Praix Tech — OCR Lab</div>
              <div class="subtitle">Futuristic UI Prototype • Upload → Preprocess → Predict</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        
        # We use a button to change the state and hide the hero section
        # The CSS for this button is injected via markdown to match the prototype
        st.markdown("""
        <style>
            div.stButton > button {
                padding: 12px 28px;
                border-radius: var(--radius-lg);
                font-size: 16px;
                margin-top: 24px;
                background-color: var(--brand);
                color: white;
                font-weight: 500;
                transition: background-color 0.2s ease, transform 0.2s ease;
                border: none;
                cursor: pointer;
            }
            div.stButton > button:hover {
                background-color: var(--brand-2);
                transform: translateY(-1px);
            }
        </style>
        """, unsafe_allow_html=True)
        if st.button("Start Demo"):
            st.session_state.show_hero = False
            st.rerun()
    else:
        # --- Upload Panel ---
        st.markdown("""
        <section class="card col-12 fade-in delay">
          <div class="head">
            <h3>Upload Image</h3>
            <span class="soft-accent">10s processing budget</span>
          </div>
        </section>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

        if uploaded_file is not None:
            st.session_state.file_uploaded = True
            st.session_state.processing_state = 1
            st.session_state.image_bytes = uploaded_file.getvalue()
            
            with st.spinner('Processing...'):
                time.sleep(3) 

            # Fake results
            st.session_state.processing_state = 2
            st.session_state.extracted_text = "This is some extracted text from your image. "
            st.session_state.prediction_label = "Text Document"
            st.session_state.confidence_score = 92
            
            st.rerun()

        if st.session_state.file_uploaded:
            # Generate the base64 data URL for the image
            b64_image = base64.b64encode(st.session_state.image_bytes).decode("utf-8")
            image_src = f"data:image/png;base64,{b64_image}"

            # --- Image Preview & Preprocessing Panel ---
            st.markdown(f"""
            <div class="grid">
              <section class="card col-6 fade-in delay" id="preview-section">
                <div class="head">
                  <h3>Image Preview</h3>
                  <span class="soft-accent" id="preview-status">{'Processing...' if st.session_state.processing_state == 1 else 'Complete'}</span>
                </div>
                <div class="image-container">
                  <img id="uploadedImage" class="responsive-image" src="{image_src}" alt="Uploaded Image Preview"/>
                </div>
              </section>

              <section class="card col-6 fade-in delay" id="preprocessing-section">
                <div class="head">
                  <h3>Data Preprocessing</h3>
                  <span class="soft-accent" id="preStatus">{'Processing...' if st.session_state.processing_state == 1 else 'Complete'}</span>
                </div>
                <p>Simulating data preprocessing steps...</p>
                <div class="metrics">
                  <div class="metric">
                    <div class="row"><span class="label">Noise Removal</span><span class="value" id="nrVal">100%</span></div>
                    <div class="bar"><i id="nrBar" style="width: 100%;"></i></div>
                  </div>
                  <div class="metric">
                    <div class="row"><span class="label">Thresholding</span><span class="value" id="threshVal">100%</span></div>
                    <div class="bar"><i id="threshBar" style="width: 100%;"></i></div>
                  </div>
                  <div class="metric">
                    <div class="row"><span class="label">Deskew</span><span class="value" id="deskewVal">100%</span></div>
                    <div class="bar"><i id="deskewBar" style="width: 100%;"></i></div>
                  </div>
                  <div class="metric">
                    <div class="row"><span class="label">Normalization</span><span class="value" id="normVal">100%</span></div>
                    <div class="bar"><i id="normBar" style="width: 100%;"></i></div>
                  </div>
                </div>
              </section>
            </div>
            """, unsafe_allow_html=True)
            
            # Only show results when processing is done
            if st.session_state.processing_state == 2:
                # --- Prediction Results Panel ---
                st.markdown(f"""
                <section class="card col-12 fade-in delay" id="results-section">
                  <div class="head">
                    <h3>Prediction Results</h3>
                    <span class="soft-accent" id="predStatus">Done</span>
                  </div>
                  <div class="grid" style="gap:16px">
                    <div class="col-8">
                      <div class="result">
                        <span class="tag soft-accent">Extracted Text</span>
                        <div class="mono" id="ocrText">{st.session_state.extracted_text}</div>
                      </div>
                    </div>
                    <div class="col-4">
                      <div class="result">
                        <span class="tag soft-accent">Prediction</span>
                        <div class="mono"><strong id="predLabel">{st.session_state.prediction_label}</strong></div>
                        <div class="confidence">
                          <div class="row"><span class="label">Confidence</span><span class="value" id="confVal">{st.session_state.confidence_score}%</span></div>
                          <div class="bar"><i id="confBar" style="width: {st.session_state.confidence_score}%;"></i></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </section>
                """, unsafe_allow_html=True)
            else:
                # Placeholder for results during processing to keep layout stable
                st.markdown("""
                <section class="card col-12 fade-in delay" id="results-section">
                  <div class="head">
                    <h3>Prediction Results</h3>
                    <span class="soft-accent" id="predStatus">Waiting for processing...</span>
                  </div>
                  <div style="height: 200px; display: flex; align-items: center; justify-content: center;">
                    <div class="animated-dots">
                      <span></span><span></span><span></span>
                    </div>
                  </div>
                </section>
                """, unsafe_allow_html=True)
        
        # --- How-to Demo Modal ---
        st.markdown(f"""
        <div class="modal-overlay" id="modal-overlay" style="display:{'flex' if st.session_state.get('show_modal') else 'none'};">
          <div class="modal">
            <div class="modal-header">
              <h3>How to Use</h3>
              <span class="modal-close-btn" onclick="document.getElementById('modal-overlay').style.display='none';">×</span>
            </div>
            <div class="modal-body">
              <p><strong>1. Upload Image:</strong> Click 'Choose File' or drag and drop an image of a document or text.</p>
              <p><strong>2. Watch it Process:</strong> The app will show a live-action stream of data preprocessing and analysis.</p>
              <p><strong>3. See the Results:</strong> The final extracted text, a predicted document type, and a confidence score will be displayed.</p>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(custom_js, unsafe_allow_html=True)
