import time
from PIL import Image
import io
import random

def preprocess_image(image_bytes: bytes):
    """
    Simulates a series of image preprocessing steps for OCR.

    In a real-world scenario, this function would perform operations
    like binarization, noise reduction, deskewing, etc., to prepare
    the image for optimal OCR performance.

    Args:
        image_bytes (bytes): The raw bytes of the uploaded image file.

    Returns:
        A PIL Image object representing the preprocessed image.
    """
    # Simulate loading the image from bytes
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        # In a real app, you'd handle specific image format errors
        print(f"Error opening image: {e}")
        return None

    print("Simulating image preprocessing...")
    # These steps are placeholders. Real-world implementations would use
    # libraries like OpenCV (cv2) or scikit-image.

    # 1. Simulate noise removal
    print("  - Applying noise removal...")
    time.sleep(random.uniform(0.1, 0.5))

    # 2. Simulate image thresholding
    print("  - Performing thresholding...")
    time.sleep(random.uniform(0.1, 0.5))

    # 3. Simulate deskewing
    print("  - Deskewing the image...")
    time.sleep(random.uniform(0.1, 0.5))

    # 4. Simulate normalization
    print("  - Normalizing the image...")
    time.sleep(random.uniform(0.1, 0.5))

    # Return the processed image (in this case, just the original)
    return image

def perform_ocr(processed_image):
    """
    Simulates the OCR process and document classification.

    This function would use an OCR library (like Tesseract or a commercial
    API) and a document classification model to analyze the image and
    return the results.

    Args:
        processed_image: A PIL Image object (simulating the preprocessed image).

    Returns:
        A dictionary containing the extracted text, predicted label,
        and a confidence score.
    """
    print("Simulating OCR and document classification...")
    # This is where a real OCR engine would run, e.g., pytesseract.image_to_string(processed_image)
    # And a separate model would classify the document.

    # --- Simulated Results ---
    extracted_text = "This is a document containing some text. In a real-world scenario, this would be the actual text extracted by an OCR engine from the image."
    
    # Randomly pick a label and a high confidence score for a realistic feel
    document_labels = ["Invoice", "Receipt", "Business Card", "Text Document", "Handwritten Note"]
    predicted_label = random.choice(document_labels)
    confidence_score = random.randint(85, 99)
    
    return {
        "extracted_text": extracted_text,
        "prediction_label": predicted_label,
        "confidence_score": confidence_score
    }
