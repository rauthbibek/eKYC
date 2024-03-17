import os
import easyocr


# def extract_text(image_path, confidence_threshold=0.8):
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])

#     # Read the image and extract text
#     result = reader.readtext(image_path)

#     # Filter the extracted text based on confidence score
#     filtered_texts = {}
#     for text in result:
#         bounding_box, recognized_text, confidence = text
#         if confidence > confidence_threshold:
#             filtered_texts[recognized_text] = bounding_box

#     return filtered_texts


def extract_text(image_path, confidence_threshold=0.3):

    print("Text Extraction Started...")
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    # Read the image and extract text
    # result = reader.readtext(image_pa th)
    try:
        print("Inside Try-Catch...")
        result = reader.readtext(image_path)
        filtered_text = "|"  # Initialize an empty string to store filtered text
        for text in result:
            bounding_box, recognized_text, confidence = text
            if confidence > confidence_threshold:
                filtered_text += recognized_text + "|"  # Append filtered text with newline

        return filtered_text 
    except Exception as e:
        print("An error occurred during text extraction:", e)
        return ""


    # Filter the extracted text based on confidence score
    