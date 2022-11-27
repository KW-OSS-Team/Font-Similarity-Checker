__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project"
__credits__ = []
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

import os

import numpy as np
from SSIM_PIL import compare_ssim
from PIL import Image
from PIL.ImageOps import invert

from preprocessing import resize, find_white_background
font_dir = ''
try:
    from Font_Copyright_Checker_Web.settings import BASE_DIR
    font_dir = os.path.join(BASE_DIR, 'analyzer/font_similiarity_checker/data/images/가/')
except:
    font_dir = 'images/가/'
location = 'images/'
fonts_to_output = 5


class Similarity:
    def __init__(self):
        self.font_list = [font.replace('.png', '') for font in os.listdir('images/가/')]
        self.ssim = compare_ssim

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
            resized_input = np.array(resize(glyph[1]).convert("L"))

            try:
                font_db = np.load(glyph_dir + glyph[0] + '_data.npy')
                fontname_db = np.load(glyph_dir + glyph[0] + '_label.npy')

                for font_it, name_it in zip(font_db, fontname_db):
                    similarity[name_it] = self.ssim(Image.fromarray(resized_input, "L"), Image.fromarray(font_it, "L"))
            except:
                print(f'failed to read {glyph[0]}: font file is not available')

            sim_fonts = dict(sorted(similarity.items(), key=lambda item: item[1], reverse=True)[:fonts_to_output])
            similar_fonts.append(sim_fonts)

        return similar_fonts


if __name__ == '__main__':
    similarity = Similarity
