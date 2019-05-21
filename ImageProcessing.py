import cv2
import numpy as np
import pyscreenshot as ImageGrab
from time import sleep
from pytesseract import image_to_string


class ImgProcessor():
    """
    Those are the coordinates for different image fragments
    that will help us take a decision for the next move
    """
    TEXT_THRESHOLD = 150

    fragments = {
        "COORDINATES" : (35, 70, 220, 100)
    }

    def __init__(self, resolution=(1920,1080)):
        print("Image Processing module initialized")
        self.resolution = resolution
        self.coordinates = []

    def grab_frame(self, box):
        im = ImageGrab.grab(bbox=box)
        im2 = np.asanyarray(im)
        screen = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        for i in range(len(screen)):
            for j in range(len(screen[i])):
                if screen[i][j] < ImgProcessor.TEXT_THRESHOLD:
                    screen[i][j] = 0

        im2 = cv2.threshold(screen, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return im2

    def display_frame(self):

        for key in ImgProcessor.fragments:
            screen = self.grab_frame(ImgProcessor.fragments[key])
            text = image_to_string(screen)
            cv2.imshow(key, cv2.cvtColor(screen, cv2.COLOR_GRAY2RGB))
            print(text)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
