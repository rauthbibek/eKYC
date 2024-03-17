import streamlit as st
from preprocess import read_image, extract_id_card, save_image
from ocr_engine import extract_text
from postprocess import extract_information
from face_verification import detect_and_extract_face, face_comparison 


# Sidebar
option = st.sidebar.selectbox("Select ID Card Type", ("Adhar", "PAN"))

if option == "Adhar":
    st.title("Extract Information From Adhar Card")
elif option == "PAN":
    st.title("Extract Information From PAN Card")

# Main content
image_file = st.file_uploader("Upload ID Card")

if image_file is not None:
    face_image_file = st.file_uploader("Upload Face Image")
    if face_image_file is not None:

        image = read_image(image_file, is_uploaded=True)
        face_image = read_image(face_image_file, is_uploaded=True)
        image_roi, _ = extract_id_card(image)
        detect_and_extract_face(img=image_roi)
        if face_image is not None:
            save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")
            is_face_verified = face_comparison()
            if is_face_verified:
                extracted_text = extract_text(image_roi)
                st.write(extracted_text)
                text_df = extract_information(extracted_text)
                col1, col2 = st.columns(2)

                # Displaying images in the first column
                with col1:
                    st.image(image_roi, caption="ID card")

                # Displaying images in the second column
                with col2:
                    st.image(face_image, caption="Uploaded Face")
                st.dataframe(text_df)

            else:
                st.write("Not able to verify the face, please try again...")
