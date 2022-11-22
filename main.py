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
        self.segment = Segmentation()
        self.similarity = Similarity()

    def check_similarity(self, image=Image.open("data/test3.png")):
        roi = self.segment.segment(image)
        similar_fonts = self.similarity.get_similarity(roi)

        '''
        roi = [
            ['가', Image()],
            ['나', Image()],
            ['다', Image()]
        ] 
        similar_fonts = [
            {'font1': 0.93, 'font2': 0.8, 'font3': 0.7, 'font4': 0.5, 'font5': 0.3},
            {'font2': 0.99, 'font3': 0.8, 'font4': 0.7, 'font5': 0.5, 'font6': 0.3},
            {'font2': 0.83, 'font4': 0.7, 'font6': 0.6, 'font8': 0.3, 'font9': 0.2}
        ]
        '''

        return roi, similar_fonts


if __name__ == '__main__':
    similarity_checker = SimilarityCheck()
    roi, similar_fonts = similarity_checker.check_similarity()
    print(similar_fonts)

