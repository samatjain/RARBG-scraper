import os
import pytesseract
import requests
from PIL import Image


# Get CAPTCHA image & extract text
class CaptchaHandler:
    def __init__(self):
        self.filename = "solved_captcha.png"

    def get_captcha(self, img_data) -> str:
        solution: str = ""
        with open(self.filename, "wb") as captcha_image:
            captcha_image.write(img_data)
            solution = pytesseract.image_to_string(Image.open(self.filename))
        os.remove(self.filename)
        return solution.strip()
