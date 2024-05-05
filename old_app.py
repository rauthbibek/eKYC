import cv2
import streamlit as st
from sqlalchemy import text
from preprocess import read_image, extract_id_card, save_image
from ocr_engine import extract_text
from postprocess import extract_information
from face_verification import detect_and_extract_face, face_comparison, get_face_embeddings
from mysqldb_operations import insert_records, fetch_records, check_duplicacy

# {
#   "ID": "CCNPA",
#   "Name": "BIBEK RAUTH",
#   "Father's Name": "AJAY RAUTH",
#   "DOB": "14/09/1994",
#   "ID Type": "PAN"
# }

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
    option = st.sidebar.selectbox("", ("PAN", " "))
    return option

# Header
def header_section(option):
    if option == "Aadhar":
        st.title("Registration Using Aadhar Card")
    elif option == "PAN":
        st.title("Registration Using PAN Card")

# Main content
def main_content(image_file, face_image_file, conn):
    if image_file is not None:
        face_image = read_image(face_image_file, is_uploaded=True)
        if face_image is not None:
            image = read_image(image_file, is_uploaded=True)
            image_roi, _ = extract_id_card(image)
            face_image_path2 = detect_and_extract_face(img=image_roi)
            face_image_path1 = save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")
            is_face_verified = face_comparison(image1_path=face_image_path1, image2_path=face_image_path2)

            if is_face_verified:
                extracted_text = extract_text(image_roi)
                text_info = extract_information(extracted_text)
                records = fetch_records(text_info)
                if records.shape[0] > 0:
                    st.write(records.shape)
                    st.write(records)
                is_duplicate = check_duplicacy(text_info)
                if is_duplicate:
                    st.write(f"User already present with ID {text_info['ID']}")
                else: 
                    st.write(text_info)
                    # Convert the DOB to string in format MySQL expects
                    text_info['DOB'] = text_info['DOB'].strftime('%Y-%m-%d')
                    text_info['Embedding'] =  get_face_embeddings(face_image_path1)
                    st.write(text_info)
                    insert_records(text_info)
                    # DB Operations
                    # with conn.session as s:
                        # s.execute(
                        #     'INSERT INTO users (id, name, father_name, dob, id_type, embedding) VALUES (:id, :name, :father_name, :dob,:id_type, :embedding );',
                        #     params=dict(id=text_info['ID'], name=text_info['Name'], father_name=text_info["Father's Name"],
                        #                 dob=text_info['DOB'], id_type=text_info['ID Type'])
                        # )
                        # s.execute(
                        #     text('INSERT INTO users (id, name, father_name, dob, id_type, embedding) VALUES (:id, :name, :father_name, :dob, :id_type, :embedding);'),
                        #     {
                        #         'id': text_info['ID'],
                        #         'name': text_info['Name'],
                        #         'father_name': text_info["Father's Name"],
                        #         'dob': text_info['DOB'],  # Make sure this is formatted as a string 'YYYY-MM-DD'
                        #         'id_type': text_info['ID Type'],
                        #         'embedding': str(text_info['Embedding'])
                        #     }
                        #     )
                        # s.commit()
    


                # col1, col2 = st.columns(2)

                # # Display ID card image
                # with col1:
                #     st.header("ID Card Image")
                #     image_roi = cv2.cvtColor(image_roi, cv2.COLOR_BGR2RGB)
                #     st.image(image_roi, use_column_width=True, caption="ID card")

                # # Display uploaded face image
                # with col2:
                #     st.header("Uploaded Face Image")
                #     face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
                #     st.image(face_image, use_column_width=True, caption="Uploaded Face")

                # # Display extracted information
                # st.header("Extracted Information")
                # st.dataframe(text_df)

            else:
                st.error("Face verification failed. Please try again.")

        else:
            st.error("Face image not uploaded. Please upload a face image.")

    else:
        st.warning("Please upload an ID card image.")

def main():
    # Initialize connection.
    conn = st.connection('mysql', type='sql')
    wider_page()
    set_custom_theme()
    option = sidebar_section()
    header_section(option)
    image_file = st.file_uploader("Upload ID Card")
    if image_file is not None:
        face_image_file = st.file_uploader("Upload Face Image")
        main_content(image_file, face_image_file, conn)

if __name__ == "__main__":
    main()
