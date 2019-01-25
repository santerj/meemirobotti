# how to use opencv with python 3:
# https://solarianprogrammer.com/2016/09/17/install-opencv-3-with-python-3-on-windows/

import numpy as np
import cv2
from PIL import Image


def new_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    frame = np.rot90(frame, k=1)  # rotation

    img = Image.fromarray(frame)
    img.save('tumppi.jpeg')

    # for debugging : show image
    # cv2.imshow('frame', frame)
    # cv2.waitKey(0)
