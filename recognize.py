from PIL import Image
import pytesseract

def extract(file_path):
    im = Image.open(file_path)
    text = pytesseract.image_to_string(im, lang='eng')
    return text
