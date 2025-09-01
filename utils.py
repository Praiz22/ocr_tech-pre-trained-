import cv2
import numpy as np
import easyocr
from PIL import Image
import re
import streamlit as st
from scipy.ndimage import interpolation as inter

# Initialize EasyOCR reader. The model is cached for faster performance.
@st.cache_resource
def load_ocr_reader():
    """Caches the EasyOCR reader to avoid reloading on every rerun."""
    return easyocr.Reader(['en'], gpu=False)

reader = load_ocr_reader()

def correct_skew(image):
    """
    Corrects the skew of an image to improve OCR accuracy.
    This function uses moments to calculate the skew angle and rotates the image.
    """
    # Convert PIL Image to a NumPy array for OpenCV
    np_image = np.array(image.convert('L'))
    
    # Invert colors for white text on black background
    inverted_img = cv2.bitwise_not(np_image)

    # Calculate moments of the image
    coords = np.column_stack(np.where(inverted_img > 0))
    center = np.mean(coords, axis=0)
    cov = np.cov(coords, rowvar=False)
    
    # Calculate eigenvectors and eigenvalues
    evals, evecs = np.linalg.eig(cov)
    
    # Get the skew angle from the largest eigenvector
    skew_angle = np.arctan2(evecs[0,1], evecs[0,0]) * 180 / np.pi
    
    # Rotate the image
    rotated = inter.rotate(np_image, skew_angle, reshape=False, mode='nearest')
    return Image.fromarray(rotated.astype(np.uint8))

def clean_image_advanced(pil_image: Image):
    """
    Applies a series of advanced image preprocessing techniques for improved OCR.
    1. Skew correction
    2. Conversion to grayscale
    3. Adaptive thresholding
    4. Morphological operations (opening) for noise removal
    """
    # Step 1: Correct skew
    skew_corrected_image = correct_skew(pil_image)
    
    # Step 2: Convert to grayscale for consistent processing
    np_image = np.array(skew_corrected_image.convert('L'))
    
    # Step 3: Adaptive Thresholding for dynamic lighting
    # This is more robust than a single binary threshold
    processed_image = cv2.adaptiveThreshold(np_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Step 4: Morphological Operations for noise reduction
    kernel = np.ones((1,1), np.uint8) # A small kernel for fine-grained noise
    processed_image = cv2.morphologyEx(processed_image, cv2.MORPH_OPEN, kernel)
    
    return processed_image

def perform_ocr(image_array: np.ndarray):
    """
    Performs OCR on a pre-processed image array using EasyOCR.
    """
    # Perform OCR
    results = reader.readtext(image_array, detail=0, paragraph=True)
    
    # Join text from results
    extracted_text = " ".join(results)
    
    return extracted_text

def classify_document(text: str):
    """
    Classifies the document type based on extracted text using an enhanced keyword-based approach.
    This is more robust than a simple keyword search, incorporating regex and scoring.
    """
    text_lower = text.lower()
    
    # Define a dictionary of keywords and their weights for common document types
    document_keywords = {
        'Invoice': {'keywords': ['invoice', 'bill to', 'due date', 'subtotal', 'total', 'amount due', 'payment'], 'weight': 1.5},
        'Receipt': {'keywords': ['receipt', 'thank you', 'total', 'tax', 'cash', 'credit', 'change', 'subtotal'], 'weight': 1.2},
        'Report': {'keywords': ['report', 'summary', 'data analysis', 'conclusion', 'introduction', 'findings', 'abstract'], 'weight': 1.0},
        'Form': {'keywords': ['name', 'address', 'date', 'signature', 'form', 'dob', 'id number'], 'weight': 1.0},
        'ID Card': {'keywords': ['id card', 'passport', 'date of birth', 'id number', 'nationality', 'expiry'], 'weight': 2.0},
        'Letter': {'keywords': ['sincerely', 'regards', 'dear', 'address', 'date', 'subject', 'body'], 'weight': 0.8},
        'Text Document': {'keywords': [], 'weight': 0.5} # Default for non-specific text
    }
    
    best_match = 'Text Document'
    highest_score = 0
    
    # Count keyword occurrences and determine confidence
    for doc_type, data in document_keywords.items():
        score = sum(1 for keyword in data['keywords'] if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower))
        
        # Apply weight to the score
        weighted_score = score * data['weight']
        
        if weighted_score > highest_score:
            highest_score = weighted_score
            best_match = doc_type
            
    # Calculate confidence based on keyword matches and text length
    confidence = 0
    if text_lower and len(text_lower.split()) > 0:
        # A more dynamic confidence calculation
        total_keywords_found = sum(re.findall(r'\b\w+\b', text_lower, re.IGNORECASE)) # Simple word count
        confidence = highest_score / len(document_keywords) * 0.1 # A simple heuristic
    
    if confidence == 0 and highest_score > 0:
        confidence = 0.5 # A baseline if no words are found but a match was made

    # Final confidence normalization
    confidence = max(0.1, min(1.0, confidence * 1.5))
    
    return best_match, confidence
