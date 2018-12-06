import numpy as np
import cv2
import time
"""
a = cv2.imread("C:/dhj-learning/berkeley/robotic/EE106AProject/trace_ball/1-1.avi(600).jpg")
a = a/255
d = a[:, :, 2]
x1 = np.ones((640, 1))
x2 = np.ones((1, 480))
y1 = (3*np.matmul(d, x1)/4)
y2 = (np.matmul(x2, d))

print(y1.max())
print(y2.max())
"""

def f(a):
    #a = cv2.imread("C:/dhj-learning/berkeley/robotic/EE106AProject/trace_ball/1-1.avi(600).jpg")
    a = a/255
    d = a[:, :, 2]
    x1 = np.ones((640, 1))
    x2 = np.ones((1, 480))
    y1 = (3*np.matmul(d, x1)/4)
    y2 = (np.matmul(x2, d))

    if y1.max() > 4 * y2.max():
        return 1#横
    elif y2.max() > 4 * y1.max():
        return -1#竖
    elif y2.max() < 5 and y1.max() < 5:
        return 0
    else:
        return 2
