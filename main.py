import sys
import pytesseract
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt
from PIL import Image

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image-to-Text Converter")

        # Set Tesseract path (make sure this is correct for your installation)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path

        # Set up layout
        self.layout = QVBoxLayout()
        
        # Text area to display and edit extracted text
        self.text_area = QTextEdit(self)
        self.text_area.setPlaceholderText("Drag and drop an image here")
        self.layout.addWidget(self.text_area)

        # Button to save edited text
        self.save_button = QPushButton("Save Text", self)
        self.save_button.clicked.connect(self.save_text)
        self.layout.addWidget(self.save_button)

        # Set up window layout
        self.setLayout(self.layout)

        # Enable drag and drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        # Accept the dragged file
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the dropped file and process it
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.extract_text(file_path)

    def extract_text(self, image_path):
        try:
            # Open the image using PIL
            image = Image.open(image_path)
            print(f"Processing image: {image_path}")

            # Use Tesseract to extract text from the image
            text = pytesseract.image_to_string(image)
            print(f"Extracted text: {text}")

            # Set the extracted text to the text area
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
