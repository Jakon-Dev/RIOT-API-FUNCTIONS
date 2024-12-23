import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajusta según tu sistema
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os


def preprocess_image(image_path):
    # Open the image
    img = Image.open(image_path)
    # Convert to grayscale
    img = img.convert("L")
    # Invert the image (light text on dark background becomes dark text on light background)
    img = ImageOps.invert(img)
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3)  # Increase contrast
    # Apply a slight blur filter to reduce noise
    img = img.filter(ImageFilter.MedianFilter(size=3))
    # Optionally, sharpen the image
    img = img.filter(ImageFilter.SHARPEN)
    # Apply thresholding to further improve text clarity
    img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Binary thresholding
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
        custom_config = r'--psm 6'  # Assume a single uniform block of text
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

