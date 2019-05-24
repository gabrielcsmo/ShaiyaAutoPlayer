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
        "HP1" : (21, 120, 139, 121),
        "MP1" : (21, 125, 139, 126),
        "SP1" : (21, 135, 139, 136)
    }

    def __init__(self, resolution=(1920,1080)):
        print("Image Processing module initialized")
        self.resolution = resolution
        self.coordinates = []
        self.boxes = {}

    def grab_frame(self, box):
        im = ImageGrab.grab(bbox=box)
        im2 = np.asanyarray(im)
        screen = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
        #screen = cv2.cvtColor(im2, cv2.COLOR_BGR2RGB)
        return screen

    def get_resources_status(self):
        """get all 3 type"""
        for key in ImgProcessor.fragments:
            self.boxes[key] = self.grab_frame(ImgProcessor.fragments[key])

    def get_res(self, res="HP", player = "1"):
        if "{}{}".format(res, player) not in self.boxes:
            print("Missing {} box for player {}".format(res, player))
            return None
        row = self.boxes["{}{}".format(res, player)]
        count = 0
        for i in row[0]:
            if i > 10:
                count += 1
        return count * 100 / len(row[0])

    def display_frame(self, box_name="HP1"):
        screen = self.grab_frame(self.fragments[box_name])
        cv2.imshow(box_name, cv2.cvtColor(screen, cv2.COLOR_GRAY2RGB))
        #cv2.imshow(box_name, cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
