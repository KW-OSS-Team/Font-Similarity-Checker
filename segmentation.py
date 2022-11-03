import cv2
import pytesseract
from PIL import Image

file = 'data/BBTreeCB.jpg'

img = cv2.imread(file)
pil = Image.fromarray(img)

text = pytesseract.image_to_string(img, lang='kor+eng')
print(text)

"""
cv2.imshow('font', img)
cv2.waitKey(0)

h, w, _ = img.shape

boxes = pytesseract.image_to_boxes(img)

for b in boxes.splitlines():
    b = b.split(' ')
    img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

print(boxes)
"""
