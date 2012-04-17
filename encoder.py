"""Encodes our frames in a video oO w00t"""

__author__ = 'cozzi.martin@gmail.com'

import cv
import os

class Video:

    def __init__(self, width, height, fps=20):
       codec = cv.CV_FOURCC('P','I','M','1')
       self.video_writer = cv.CreateVideoWriter(
               'out.mpg', codec, fps, (1080, 720), True)

    def build(self, folder):
        pictures = os.listdir(folder)
        for picture in sorted(pictures, reverse=True):
            picture_path = '%s/%s' % (folder, picture)
            image = cv.LoadImage(picture_path)
            cv.WriteFrame(self.video_writer, image)
            os.remove(picture_path)
