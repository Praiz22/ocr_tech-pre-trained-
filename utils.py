import cv2
import numpy as np
import easyocr
from PIL import Image

def clean_image(image: Image):
    """
    Cleans an image for OCR by converting to grayscale, applying a binary threshold,
    and performing noise removal. Returns the processed image as a NumPy array.
    """
    # Convert PIL Image to a NumPy array for OpenCV
    np_image = np.array(image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    
    # Apply a binary threshold
    _, thresholded = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Simple noise removal (optional but can help)
    denoised = cv2.fastNlMeansDenoising(thresholded, None, 10, 7, 21)
    
    return denoised, 0.9 # Return a mock threshold value for the UI

def perform_ocr(image_array: np.ndarray):
    """
    Performs OCR on a pre-processed image array using EasyOCR.
    """
    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(image_array)
    
    # Extract text from results
    extracted_text = " ".join([result[1] for result in results])
    
    return extracted_text

def guess_image_type(text: str):
    """
    Classifies the document type based on extracted text using a keyword-based scoring system.
    """
    text_lower = text.lower()
    
    # Define a dictionary of keywords for common document types
    document_keywords = {
        'Invoice': ['invoice', 'bill to', 'due date', 'subtotal', 'total'],
        'Receipt': ['receipt', 'thank you', 'total', 'tax', 'cash', 'credit'],
        'Report': ['report', 'summary', 'data analysis', 'conclusion', 'introduction'],
        'Form': ['name', 'address', 'date', 'signature', 'form'],
        'ID Card': ['id card', 'passport', 'date of birth', 'id number', 'nationality'],
    }
    
    # Initialize classification result
    best_match = 'Text Document'
    highest_score = 0
    
    # Count keyword occurrences and determine confidence
    for doc_type, keywords in document_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        
        if score > highest_score:
            highest_score = score
            best_match = doc_type
            
    # Calculate confidence based on keyword matches
    # This is a heuristic, not a true confidence score
    confidence = highest_score / len(text_lower.split()) if text_lower and len(text_lower.split()) > 0 else 0
    confidence = min(0.99, confidence * 10) # Scale and cap the confidence for better UI representation
    
    return best_match, confidence
