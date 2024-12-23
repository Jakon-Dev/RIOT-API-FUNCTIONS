import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajusta según tu sistema
from PIL import Image, ImageEnhance, ImageFilter
import os

def preprocess_image(image_path):
    # Open the image
    img = Image.open(image_path)
    # Convert to grayscale
    img = img.convert("L")
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3)  # Increase contrast
    # Apply a slight blur filter to reduce noise
    img = img.filter(ImageFilter.MedianFilter(size=3))
    # Optionally, sharpen the image
    img = img.filter(ImageFilter.SHARPEN)
    return img

def read_text_from_image(image_path):
    try:
        # Check if the image file exists
        if not os.path.exists(image_path):
            print(f"Error: The file {image_path} does not exist.")
            return

        # Preprocess the image
        img = preprocess_image(image_path)

        # Perform OCR using Tesseract
        # Use --psm 6 for a single block of text, and --oem 3 for the best OCR engine mode
        custom_config = r"--oem 3 --psm 6 -c tessedit_char_whitelist='0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'"
        text = pytesseract.image_to_string(img, config=custom_config)

        # Print the extracted text
        print("Extracted Text:")
        print(text)

        # Optionally, save the text to a file
        output_file = os.path.splitext(image_path)[0] + "_output.txt"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Extracted text saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the image path
image_path = "VALORANT/VOD_Scanner/TAB_Reader/INPUT/image.png"
read_text_from_image(image_path)

