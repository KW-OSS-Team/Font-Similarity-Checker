__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project Team"
__credits__ = "hamoci"
__license__ = "GPL 3.0  License"
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


def find_white_background(image, threshold=0.3):
    """remove images with transparent or white background"""
    w, h = image.shape

    total = w * h
    background = np.array([255, 255])

    cnt = 0
    for row in image:
        for pixel in row:
            if np.array_equal(pixel, background):
                cnt += 1

    percent = cnt / total
    if percent >= threshold:
        return True
    else:
        return False


# Image resize to 128*128
def resize(im: Image) -> Image:
    resized = im.resize((128, 128))
    return resized


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


def _process_glyph(glyph_name):
    # Directory that file will be saved
    savedir = 'images/'+glyph_name+'/'

    # Get list of fonts.png
    files = os.listdir(location+glyph_name+'/')

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    for name in files:
        img = Image.fromarray(_image_filter(location+glyph_name+'/'+name))
        img.save(savedir+name)


def _process_glyph_to_array(glyph_name):
    # Directory that file will be saved
    savedir = 'images/' + glyph_name + '/'

    # Get list of fonts.png
    files = os.listdir(location + glyph_name + '/')
    img_list = []
    font_name_list = []

    if not os.path.exists(savedir):
        os.makedirs(savedir)

    for name in files:
        # Add font name to font_name_list
        font_name_list.append(name.replace('.png', ''))
        img = np.uint8(np.asarray(Image.fromarray(_image_filter(location+glyph_name+'/'+name)).convert("L")))
        img_list.append(img)
    np.save(savedir+glyph_name+'_label', np.array(font_name_list))
    np.save(savedir+glyph_name+'_data', np.array(img_list))


def _process_dl(glyph_name):
    # Directory that file will be saved
    savedir = 'data_for_dl/'+glyph_name+'/'

    # Get list of fonts.png
    files = os.listdir(location+glyph_name+'/')

    for name in files:
        if not os.path.exists(savedir+name+'/'):
            os.makedirs(savedir+name+'/')
            img = Image.fromarray(_image_filter(location+glyph_name+'/'+name))
            img.save(savedir+name+'/'+name)


def _image_filter(file_name):
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

    num_process = 6

    print("Start Preprocessing")
    
    with Pool(num_process) as p:
        p.map(_process_glyph_to_array, glyphs)

    # process_glyph(glyphs)

    print("Finished Preprocessing")
