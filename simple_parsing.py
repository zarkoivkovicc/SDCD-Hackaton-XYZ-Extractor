from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageFilter

# Path to the PDF file
pdf_path = '/Users/annakelmanson/Downloads/paper-1-transformed-1.pdf'

# Convert PDF to images with high DPI
images = convert_from_path(pdf_path, dpi=600)

# Iterate over each image (page)
for i, image in enumerate(images):
    # Apply preprocessing to enhance image quality
    image = image.convert('L')  # Convert to grayscale
    image = image.filter(ImageFilter.SHARPEN)  
    image = image.filter(ImageFilter.)

    # Save the preprocessed image as a JPEG file
    image_path = f'page_{i+1}.jpg'
    image.save(image_path, 'JPEG')

    # Use pytesseract to do OCR on the preprocessed image
    text = pytesseract.image_to_string(f'./enhanced_image.jpg', lang='eng')  # Specify language if needed

    # Print or save the extracted text
    print(f"Text from page {i+1}:\n{text}\n")
