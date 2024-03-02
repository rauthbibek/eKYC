import os
import easyocr


def extract_text(image_path, confidence_threshold=0.8):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Read the image and extract text
    result = reader.readtext(image_path)

    # Filter the extracted text based on confidence score
    filtered_texts = {}
    for text in result:
        bounding_box, recognized_text, confidence = text
        if confidence > confidence_threshold:
            filtered_texts[recognized_text] = bounding_box

    return filtered_texts