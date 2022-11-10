__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project Team"
__credits__ = []
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

import os
import glob
from multiprocessing.pool import Pool

import cv2
import numpy as np
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator

# Directory of fonts
location = 'dataset/'
datagen = ImageDataGenerator(rotation_range=5,
                             width_shift_range=0.1,
                             height_shift_range=0.1,
                             shear_range=0.2,
                             zoom_range=0.2)


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


def process_glyph(glyph_name):
    # Directory that file will be saved
    savedir = 'images/'+glyph_name+'/'
    # Get list of fonts.png
    files = os.listdir(location+glyph_name+'/')
    for name in files:
        if not os.path.exists(savedir):
            os.makedirs(savedir)
        img = Image.fromarray(image_filter(location+glyph_name+'/'+name))
        img.save(savedir+name)


def image_filter(file_name):
    image = Image.open(file_name)
    # Load image and remove transparent background
    image = np.asarray(remove_transparency(image))
    '''
    # Change image to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    '''
    return image


if __name__ == '__main__':
    # Get list of glyphs
    glyphs = os.listdir(location)

    num_process = 4
    with Pool(num_process) as p:
        p.map(process_glyph, glyphs)

    # process_glyph(glyphs)
