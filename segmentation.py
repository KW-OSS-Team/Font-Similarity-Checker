__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project Team"
__credits__ = [
    "https://stackoverflow.com/a/1963146",
    "https://stackoverflow.com/a/9459208",
    "https://stackoverflow.com/a/1963146",
    "https://stackoverflow.com/a/8720632",
    "https://stackoverflow.com/a/62414364",
    "hamoci"
]
__license__ = "GPL 3.0 License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

import os
import fnmatch

import re
import cv2
import pytesseract
import numpy as np
from PIL import Image

from preprocessing import remove_transparency


# Image Discretization
def image_threshold(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def morphology(image, kernel_size=1):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image = cv2.dilate(image, kernel)    # Dilation
    image = cv2.erode(image, kernel)     # Erosion
    image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)      # Opening
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)     # Closing

    return image


class Segmentation:
    def __init__(self):
        with open('whitelist.txt', encoding='utf-8') as f:
            temp = f.readlines()[0]
        self.whitelist = [char for char in temp]  # Unpack strings

    def segment(self, image_input: Image) -> list:
        box = []

        # Load image and remove transparent background
        image = np.asarray(remove_transparency(image_input))

        # Change image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Discretize and remove noise
        image = image_threshold(gray)

        # Transform morphology and get edged image
        image = morphology(image)

        # For Debug
        # cv2.imshow('gray', gray)
        # cv2.imshow('blurred', blurred)
        # cv2.imshow('edged', image)
        # cv2.waitKey(0)

        hImg, wImg = image.shape
        boxes = pytesseract.image_to_boxes(image, lang='kor')
        text = pytesseract.image_to_string(image, lang='kor')

        ROI_number = 0
        ROI_list = []
        for b in boxes.splitlines():
            b = b.split(' ')
            if b[0] not in self.whitelist:  # Don't save if the recognized character is not Korean
                continue

            # Get positions
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            x1, y1 = hImg - h, hImg - y
            x2, y2 = x, w

            # Save character and box positions
            # to plot boxes on image
            box.append(b)

            # ROI is a box
            roi = image[x1:y1, x2:y2]

            # For Debug
            # cv2.imshow('roi', roi)
            # cv2.waitKey(0)

            try:
                ROI_list.append([b[0], roi])
            except cv2.error:
                print(f'Error in saving {b[0]}')
                print(f'ROI number: {ROI_number}')
                continue
            ROI_number += 1

        return ROI_list


if __name__ == "__main__":
    segment = Segmentation()
    segment.segment(Image.open('data/test3.png'))
