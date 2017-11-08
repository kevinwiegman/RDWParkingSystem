from PIL import Image
import pytesseract

def extract(file_path):
    return pytesseract.image_to_string(Image.open(file_path), lang='eng')
