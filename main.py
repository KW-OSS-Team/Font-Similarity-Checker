__author__ = "Jiwoon Lee"
__copyright__ = "Copyright 2022, Kwangwoon University 2022-2 Open Source Project Team"
__credits__ = [
]
__license__ = "MIT License"
__maintainer__ = "Jiwoon Lee"
__email__ = ["webmaster@kw.ac.kr", "metr0jw@naver.com"]

from segmentation import Segmentation
from similarity_check import Similarity

# Debug
from PIL import Image


class SimilarityCheck:
    def __init__(self):
        self.image = None
        self.segment = Segmentation()
        self.similarity = Similarity()

    def check_similarity(self, image=Image.open("data/test3.png")):
        self.image = image
        roi = self.segment.segment(self.image)
        # TODO: Something cool
        similar_fonts = {
            "NanumGothic": 0.7,
            "NanumSquare": 0.5
        }
        return roi, similar_fonts


if __name__ == '__main__':
    similarity_checker = SimilarityCheck()
    test = similarity_checker.check_similarity()

