__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project"
__credits__ = [
    "https://stackoverflow.com/a/1963146",
    "https://stackoverflow.com/a/9459208",
    "https://stackoverflow.com/a/1963146",
    "https://stackoverflow.com/a/8720632",
    "https://stackoverflow.com/a/62414364",
    "https://yunwoong.tistory.com/58"
]
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

import os
import fnmatch

import re
import numpy as np

import cv2
import pytesseract
from PIL import Image


# Remove Background Transparency
def remove_transparency(im, bg_colour=(255, 255, 255)):
    # Only process if image has transparency ()
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        # Need to convert to RGBA if LA format due to a bug in PIL
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im


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
    def __init__(self, filename):
        with open('whitelist.txt', encoding='utf-8') as f:
            temp = f.readlines()[0]
        self.whitelist = [char for char in temp]  # Unpack strings
        self.file = f'data/{filename}'      # image file
        self.image = cv2.imread(self.file)  # image (opencv)
        self.box = []

    @staticmethod
    def save_image(image, name):
        files = fnmatch.filter((f for f in os.listdir('extracted/')), f'{name}*.')

        if not files:  # is empty
            num = ''
        elif len(files) == 1:
            num = '(1)'
        else:
            # files is supposed to contain 'somefile.jpg'
            files.remove(f'{name}.jpg')
            num = '(%i)' % (int(re.search(r'\((\d+)\)', max(files)).group(1)) + 1)

        filename = r'extracted/' + name + num + '.jpg'
        try:
            with open(filename, mode='w+b') as f:
                _, encoded_img = cv2.imencode('.jpg', image)
                encoded_img.tofile(f)
            print(f"Saved {filename}")
        except:
            print(f'Failed to save {filename}')

    def segment(self):
        # Load image and remove transparent background
        image = np.asarray(remove_transparency(Image.fromarray(cv2.imread(self.file))))

        # Change image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Discretize and remove noise
        image = image_threshold(gray)

        # Transform morphology and get edged image
        image = morphology(image)

        """
        # For Debug
        cv2.imshow('gray', gray)
        cv2.imshow('blurred', blurred)
        cv2.imshow('edged', edged)
        cv2.waitKey(0)
        """

        hImg, wImg = image.shape
        boxes = pytesseract.image_to_boxes(image, lang='kor')

        ROI_number = 0
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
            self.box.append(b)

            # ROI is a box
            roi = self.image[x1:y1, x2:y2]

            # For Debug
            # cv2.imshow('roi', roi)
            # cv2.waitKey(0)

            try:
                self.save_image(roi, b[0])
            except cv2.error:
                print(f'Error in saving {b[0]}')
                print(f'ROI number: {ROI_number}')
                continue
            ROI_number += 1

        return ROI_number


if __name__ == "__main__":
    segment = Segmentation('test3.png')
    segment.segment()
