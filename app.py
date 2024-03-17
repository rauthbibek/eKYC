import streamlit as st
from preprocess import read_image, extract_id_card, save_image
from ocr_engine import extract_text
from postprocess import extract_information
from face_verification import detect_and_extract_face, face_comparison 

# Set wider page layout
def wider_page():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{ {max_width_str} }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Customized Streamlit theme
def set_custom_theme():
    st.markdown(
        """
        <style>
            body {
                background-color: #f0f2f6; /* Set background color */
                color: #333333; /* Set text color */
            }
            .sidebar .sidebar-content {
                background-color: #ffffff; /* Set sidebar background color */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Sidebar
def sidebar_section():
    st.sidebar.title("Select ID Card Type")
    option = st.sidebar.selectbox("", ("Aadhar", "PAN"))
    return option

# Header
def header_section(option):
    if option == "Aadhar":
        st.title("Registration Using Aadhar Card")
    elif option == "PAN":
        st.title("Registration Using PAN Card")

# Main content
def main_content(image_file, face_image_file):
    if image_file is not None:
        face_image = read_image(face_image_file, is_uploaded=True)
        if face_image is not None:
            image = read_image(image_file, is_uploaded=True)
            image_roi, _ = extract_id_card(image)
            detect_and_extract_face(img=image_roi)
            save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")
            is_face_verified = face_comparison()

            if is_face_verified:
                extracted_text = extract_text(image_roi)
                text_df = extract_information(extracted_text)

                col1, col2 = st.columns(2)

                # Display ID card image
                with col1:
                    st.header("ID Card Image")
                    st.image(image_roi, use_column_width=True, caption="ID card")

                # Display uploaded face image
                with col2:
                    st.header("Uploaded Face Image")
                    st.image(face_image, use_column_width=True, caption="Uploaded Face")

                # Display extracted information
                st.header("Extracted Information")
                st.dataframe(text_df)

            else:
                st.error("Face verification failed. Please try again.")

        else:
            st.error("Face image not uploaded. Please upload a face image.")

    else:
        st.warning("Please upload an ID card image.")

def main():
    wider_page()
    set_custom_theme()
    option = sidebar_section()
    header_section(option)
    image_file = st.file_uploader("Upload ID Card")
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image")
        main_content(image_file, face_image_file)

if __name__ == "__main__":
    main()
