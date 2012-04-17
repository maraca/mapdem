"""Encodes our frames in a video oO w00t"""

__author__ = 'cozzi.martin@gmail.com'

import os

from opencv import cv
from opencv import highgui
import cv as cv2

class Video:

    def __init__(self, width, height, fps=30):
       codec = cv2.CV_FOURCC('X', 'V', 'I', 'D') 
       codec = cv2.CV_FOURCC('M','J','P','G')
       codec = cv2.CV_FOURCC('F', 'L', 'V', '1') 
       codec = cv2.CV_FOURCC('P','I','M','1')
       self.video_writer = cv2.CreateVideoWriter(
               'out.mpg', codec, fps, (1080, 720), True)

    def build(self, folder):
        pictures = os.listdir(folder)
        for picture in sorted(pictures, reverse=True):
            picture_path = '%s/%s' % (folder, picture)
            image = cv2.LoadImage(picture_path)
            cv2.WriteFrame(self.video_writer, image)
            

class Video2:
    """Build yo video."""

    def __init__(self, width, height, fps=25):
        fps = fps
        codec = highgui.CV_FOURCC('F', 'L', 'V', '1') 
        codec = highgui.CV_FOURCC('X', 'V', 'I', 'D') 
        colored = 1
        size = (float(width), float(height))
        size = cv.cvSize(width, height)
        self.video_writer = highgui.cvCreateVideoWriter(
                'out.mpg', codec, fps, cv.cvSize(1440, 553), True)

    def build(self, folder):
        """Builds a video from the files located in @folder."""
        pictures = os.listdir(folder)
        if not pictures:
            raise Exception('No files duh.')

        for picture in pictures:
            # img = highgui.cvLoadImage(frame)
            # highgui.cvShowImage('mahMovie', img)
            picture = '%s/%s' % (folder, picture)
            # picture_ipl = cv.IplImage(picture)
            highgui.cvWriteFrame(self.video_writer, picture)
            # self.video_writer.write(frame)

        return True

