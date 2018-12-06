import subprocess
import numpy as np
import cv2

def capture_image():
    subprocess.call("fswebcam image.jpg")

def get_image_average():
    img = cv2.imread("image.jpg", mode='RGB')
    print(img)
