import cv2
import pytesseract
import json

def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Preprocess the image (e.g., resize, denoise, enhance)
    # Perform any necessary operations using OpenCV
    
    return image

def extract_text(image):
    # Perform OCR using Pytesseract
    text = pytesseract.image_to_string(image)
    return text

def parse_text(text):
    # Implement logic to extract relevant information
    # Use regular expressions or other parsing techniques
    
    # Example parsing logic (you need to refine this):
    data = {
        "name": "John Doe",
        "dob": "01-01-1990",
        "id": "1234 5678 9012",
        "gender": "Male"
    }
    
    return data

def main(image_path):
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Extract text using OCR
    extracted_text = extract_text(preprocessed_image)
    
    # Parse extracted text to get relevant information
    parsed_data = parse_text(extracted_text)
    
    # Convert parsed data to JSON format
    json_data = json.dumps(parsed_data, indent=4)
    print(json_data)

if __name__ == "__main__":
    image_path = "path/to/your/image.jpg"
    main(image_path)