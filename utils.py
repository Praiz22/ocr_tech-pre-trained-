import numpy as np
import easyocr
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification
import torch
import streamlit as st

# Initialize EasyOCR reader. It will download the model the first time it's run.
# The `@st.cache_resource` decorator caches the resource to prevent re-initializing
# the reader every time the app reruns.
@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(['en'])

reader = get_ocr_reader()

# Load the pre-trained model and processor from Hugging Face
# This model is pre-trained on a large dataset and does not require training.
processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

# A dictionary to map the model's predicted ID to a human-readable label
# The labels here are simplified for the purpose of the demo
# In a real-world scenario, you would inspect the model's labels and create a comprehensive map
LABEL_MAP = {
    'document': ['notebook', 'paper', 'textbook'],
    'photo': ['photo', 'image', 'picture'],
    'diagram': ['diagram', 'chart', 'graph'],
    'unknown': ['n04522168', 'n04522292', 'n04522378', 'n04522409', 'n04522533', 'n04522568', 'n04522618', 'n04522650', 'n04522695', 'n04522730']
}

def clean_image(image: Image.Image):
    """
    Cleans up the image by converting it to grayscale and applying a threshold.
    This improves OCR accuracy.
    """
    # Convert to grayscale
    grayscale_image = image.convert('L')
    
    # Calculate an automatic threshold value
    # You can also use a fixed value like 128
    threshold = np.mean(np.array(grayscale_image))
    
    # Apply thresholding
    binarized_image = grayscale_image.point(lambda x: 0 if x < threshold else 255, '1')
    
    return binarized_image, threshold / 255.0

def perform_ocr(image: Image.Image) -> str:
    """
    Performs OCR on the given image using EasyOCR.
    """
    try:
        results = reader.readtext(np.array(image))
        text = " ".join([result[1] for result in results])
        return text.strip()
    except Exception as e:
        return f"An error occurred during OCR: {e}"

def guess_image_type(image: Image.Image):
    """
    Classifies the image using a pre-trained Vision Transformer model.
    """
    try:
        # Resize image to model's expected input size
        inputs = processor(images=image, return_tensors="pt")
        
        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Get predicted class ID and confidence
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        confidence = torch.nn.functional.softmax(logits, dim=-1)[0][predicted_class_idx].item()
        
        # Get the label from the model's vocabulary
        predicted_label = model.config.id2label[predicted_class_idx]
        
        # Map to a simplified label for the UI
        for key, labels in LABEL_MAP.items():
            if any(l in predicted_label for l in labels):
                return key.capitalize(), confidence
        
        # Return the original label if no match is found
        return predicted_label, confidence
    except Exception as e:
        return "Error", 0.0
