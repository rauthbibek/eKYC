import easyocr
import cv2
import streamlit as st
from preprocess import read_image, extract_id_card
from ocr_engine import extract_text

# Function to extract text from an image
# def extract_text(image):
#   reader = easyocr.Reader(['en'])  # Load EasyOCR reader for English
#   result = reader.readtext(image, detail=0)  # Extract text without confidence scores
#   return result

# Streamlit layout with image upload and button
image_file = st.file_uploader("Upload Image")
if image_file is not None:
  
  image = read_image(image_file, is_uploaded = True)

  image_roi = extract_id_card(image)
  # Use the image for text extraction
  extracted_text = extract_text(image)
  st.write("Extracted Text:", extracted_text)
