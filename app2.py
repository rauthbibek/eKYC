import cv2
import pytesseract
import pytesserocr  # Alternative OCR engine for improved accuracy
import numpy as np

# Function to extract text using Tesseract (fallback to pytesserocr if needed)
def extract_text(img, config="--psm 6"):
    try:
        # Attempt Tesseract OCR
        text = pytesseract.image_to_string(img, config=config)
        if text:
            return text.strip()
    except:
        # Fallback to alternative OCR engine
        try:
            text = pytesserocr.image_to_text(img)
            return text.strip()
        except:
            print("Error: Text extraction failed with both Tesseract and pytesserocr.")
            return None

# Function for face detection and extraction using Haar cascade classifier
def extract_face(img, cascade_path="haarcascade_frontalface_default.xml"):
    if not cascade_path:
        print("Error: Please provide a valid path to the Haar cascade classifier.")
        return None

    face_cascade = cv2.CascadeClassifier(cascade_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) != 1:
        print("Error: Detected either 0 or multiple faces. Please ensure a single face is present.")
        return None

    (x, y, w, h) = faces[0]
    return img[y:y + h, x:x + w]

# Function for duplicacy check using a placeholder (replace with your database logic)
def check_duplicacy(extracted_data):
    # Replace with your implementation to check against a database or API
    print("Placeholder: Implementing duplicacy check using your data source.")
    return True

def main():
    # Replace with your ID card image path
    img_path = "path/to/your/id_card.jpg"

    # Read the image
    img = cv2.imread(img_path)

    if not img:
        print("Error: Image not found at the specified path.")
        return

    # Extract the face region
    face = extract_face(img.copy())

    if not face:
        print("Error: Face extraction failed. Please ensure proper image quality.")
        return

    # Perform text extraction
    extracted_text = extract_text(face)

    if not extracted_text:
        print("Error: Text extraction failed.")
        return

    # Preprocessing (add if needed, e.g., noise reduction, thresholding)
    # ...

    # Extract data from the extracted text using specific patterns or predefined locations
    # (This would require understanding the layout of your ID card)
    # Example:
    # name = extract_data_from_text(extracted_text, "NAME: (.*)")
    # ...

    # Perform face verification (replace with your implementation)
    # Example:
    # is_verified = verify_face(face)
    is_verified = True  # Placeholder until implemented

    # Perform duplicacy check
    is_duplicate = check_duplicacy(extracted_text)  # Replace with your logic

    # Output
    if is_verified and not is_duplicate:
        print("Registration successful!")
        # Process extracted data further
    else:
        print("Registration failed. Reason(s):")
        if not is_verified:
            print("- Face verification failed.")
        if is_duplicate:
            print("- Duplicate entry detected.")

if __name__ == "__main__":
    main()
