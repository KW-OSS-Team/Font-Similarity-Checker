__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project"
__credits__ = [
]
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

from segmentation import Segmentation


class SimilarityCheck:
    def __init__(self):
        self.image = 'test3.png'
        self.segment = Segmentation(self.image)

    def check_similarity(self):
        raise NotImplementedError

    def get_segment(self):
        raise NotImplementedError
