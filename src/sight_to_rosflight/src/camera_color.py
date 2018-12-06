import os
import subprocess
import numpy as np
import cv2

def capture_image():
    os.system("fswebcam image.jpg")

def get_image_average():
    img = cv2.imread("image.jpg")
    average_color = np.mean(img, axis=(0, 1))
    print(average_color)

def get_direction():
    color = get_image_average()
    
    if color == 'red':
        return 0
    elif color == 'green':
        return 1
    elif color == 'blue':
        return 2
    elif color == 'yellow':
        return 3
    else:
        return -1
