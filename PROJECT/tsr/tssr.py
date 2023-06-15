import pytesseract
import cv2
from PIL import Image
image = cv2.imread("123.jpg")
# получаем строку
string = pytesseract.image_to_string(image, lang='rus+eng')
# печатаем
print(string)