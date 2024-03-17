import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from preprocess import read_image, extract_id_card, save_image
from ocr_engine import extract_text
from postprocess import extract_information
from face_verification import detect_and_extract_face, face_comparison

class IDCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ID Card Information Extraction")
        self.root.geometry("800x600")
        self.root.configure(background="#f0f2f6")

        self.option_var = tk.StringVar()
        self.image_file = None
        self.face_image_file = None

        self.create_widgets()

    def create_widgets(self):
        # Title label
        title_label = tk.Label(self.root, text="Extract Information from ID Card", font=("Arial", 20), background="#f0f2f6")
        title_label.pack(pady=20)

        # ID Card type selection
        id_card_label = tk.Label(self.root, text="Select ID Card Type:", font=("Arial", 12), background="#f0f2f6")
        id_card_label.pack()

        self.option_var.set("Aadhar")  # Default selection
        option_menu = tk.OptionMenu(self.root, self.option_var, "Aadhar", "PAN")
        option_menu.pack()

        # Upload ID Card button
        upload_id_button = tk.Button(self.root, text="Upload ID Card", command=self.upload_id_card)
        upload_id_button.pack(pady=10)

        # Upload Face Image button
        upload_face_button = tk.Button(self.root, text="Upload Face Image", command=self.upload_face_image)
        upload_face_button.pack(pady=10)

        # Process button
        process_button = tk.Button(self.root, text="Process", command=self.process_images)
        process_button.pack(pady=10)

    def upload_id_card(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image_file = file_path
            messagebox.showinfo("Success", "ID Card uploaded successfully!")

    def upload_face_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.face_image_file = file_path
            messagebox.showinfo("Success", "Face image uploaded successfully!")
    def process_images(self):
        if self.image_file is None or self.face_image_file is None:
            messagebox.showerror("Error", "Please upload both ID Card and Face Image.")
            return

        try:
            image = read_image(self.image_file, is_uploaded=True)
            face_image = read_image(self.face_image_file, is_uploaded=True)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading image: {str(e)}")
            return

        image_roi, _ = extract_id_card(image)
        detect_and_extract_face(img=image_roi)
        save_image(face_image, "face_image.jpg", path="data\\02_intermediate_data")
        is_face_verified = face_comparison()

        if is_face_verified:
            extracted_text = extract_text(image_roi)
            text_df = extract_information(extracted_text)
            messagebox.showinfo("Success", "Information extracted successfully!")
            self.display_results(image_roi, face_image, text_df)
        else:
            messagebox.showerror("Error", "Face verification failed. Please try again.")


    def display_results(self, id_card_image, face_image, text_df):
        # Create a new window for displaying results
        result_window = tk.Toplevel(self.root)
        result_window.title("Extraction Results")

        # ID Card image
        id_card_label = tk.Label(result_window, text="ID Card Image", font=("Arial", 12))
        id_card_label.pack()
        id_card_img = ImageTk.PhotoImage(Image.fromarray(id_card_image))
        id_card_img_label = tk.Label(result_window, image=id_card_img)
        id_card_img_label.pack()

        # Uploaded face image
        face_label = tk.Label(result_window, text="Uploaded Face Image", font=("Arial", 12))
        face_label.pack()
        face_img = ImageTk.PhotoImage(Image.fromarray(face_image))
        face_img_label = tk.Label(result_window, image=face_img)
        face_img_label.pack()

        # Extracted information
        text_label = tk.Label(result_window, text="Extracted Information", font=("Arial", 12))
        text_label.pack()
        text_df_str = text_df.to_string(index=False)
        text_df_label = tk.Label(result_window, text=text_df_str, font=("Arial", 10), justify="left")
        text_df_label.pack()

def main():
    root = tk.Tk()
    app = IDCardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
