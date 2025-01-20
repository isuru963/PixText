import sys
import pytesseract
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import Qt
from PIL import Image
import os

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image-to-Text Converter")

        # Set the Tesseract path to the bundled Tesseract executable
        # Update the path to the bundled Tesseract in your project folder
        pytesseract.pytesseract.tesseract_cmd = r'C:\path\to\your\project\tesseract\tesseract.exe'

        # Set up layout
        self.layout = QVBoxLayout()
        
        # Label for file upload area
        self.upload_label = QLabel("No file selected", self)
        self.layout.addWidget(self.upload_label)

        # Button to open file explorer
        self.upload_button = QPushButton("Submit File", self)
        self.upload_button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.upload_button)

        # Text area to display and edit extracted text (Area 2)
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Converted text will appear here")
        self.layout.addWidget(self.text_area)

        # Button to save the converted text
        self.save_button = QPushButton("Save Text", self)
        self.save_button.clicked.connect(self.save_text)
        self.layout.addWidget(self.save_button)

        # Set up window layout
        self.setLayout(self.layout)

    def open_file_dialog(self):
        # Open file dialog to select an image
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        # If a file is selected, process the image
        if file_path:
            self.upload_label.setText(f"Selected file: {file_path}")  # Show selected file path
            self.extract_text(file_path)

    def extract_text(self, image_path):
        try:
            # Open the image using PIL
            print(f"Processing image: {image_path}")
            image = Image.open(image_path)

            # Use Tesseract to extract text from the image
            text = pytesseract.image_to_string(image)
            print(f"Extracted text: {text}")

            # Set the extracted text to the text area (Area 2)
            self.text_area.setText(text)
        except Exception as e:
            self.text_area.setText(f"Error: {str(e)}")
            print(f"Error processing image: {str(e)}")

    def save_text(self):
        # Save the modified text to a file
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_area.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec_())
