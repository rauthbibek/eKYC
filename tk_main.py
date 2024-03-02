import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import easyocr

class ImageTextExtractorApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Text Extractor")

        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.extract_button = tk.Button(master, text="Extract Text", command=self.extract_text)
        self.extract_button.pack()

        self.text_output = tk.Text(master, height=10, width=50)
        self.text_output.pack()

        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR with English language

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo

    def extract_text(self):
        if hasattr(self, 'image'):
            try:
                extracted_text = self.reader.readtext(self.image)
                self.text_output.delete('1.0', tk.END)
                for text in extracted_text:
                    self.text_output.insert(tk.END, f"{text[1]}\n")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Error", "Please upload an image first.")

def main():
    root = tk.Tk()
    app = ImageTextExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
