__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project"
__credits__ = []
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

import os

import numpy as np
from sewar.full_ref import ssim, msssim
from PIL import Image
from PIL.ImageOps import invert

from preprocessing import resize, find_white_background

location = 'images/'
fonts_to_output = 5

class Similarity:
    def __init__(self):
        self.font_list = [font.replace('.png', '') for font in os.listdir('images/가/')]
        self.ssim = ssim
        self.msssim = msssim

    def get_similarity(self, roi: [[str, Image]]) -> list:
        similar_fonts = list()

        for glyph in roi:
            # Directory that contains image
            # glyph[0]: name of glyph
            # glyph[1]: image
            glyph_dir = 'images/' + glyph[0] + '/'

            # Check if input font is white or black
            # If font is white(background is black), invert
            if not find_white_background(glyph[1]):
                glyph[1] = invert(Image.fromarray(glyph[1], "L"))

            similarity = dict()
            fontdir = os.listdir(glyph_dir)
            font_list = [font.replace('.png', '') for font in fontdir]
            resized_input = np.array(resize(glyph[1]).convert("L"))

            for font in fontdir:
                fontname = font.replace('.png', '')
                try:
                    font_db = np.array(Image.open(glyph_dir + font).convert("L"))
                    similarity[fontname] = self.ssim(resized_input, font_db)[0]
                except:
                    print(f'failed to read {font}: font file is not available')

            sim_fonts = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True)[:fonts_to_output])
            similar_fonts.append(sim_fonts)

        return similar_fonts


if __name__ == '__main__':
    similarity = Similarity
