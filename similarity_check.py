__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project"
__credits__ = []
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

import os

import numpy as np
from sewar.full_ref import ssim, msssim


class Similarity:
    def __init__(self):
        self.font_list = []
        self.ssim = ssim
        self.msssim = msssim

    def ssim(self):
        self.ssim()


if __name__ == '__main__':
    similarity = Similarity
