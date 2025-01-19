import pytesseract
from PIL import Image

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Open an image using Pillow
image = Image.open('your_image.png')

# Use Tesseract to extract text
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
