# -*- coding: utf-8 -*-
from __future__ import print_function 
import cv2
import numpy as np
from collections import deque
import argparse
#import analys_trace
# for debug
import time


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(0)
# 网球 color of tennis ball
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
"""
# 黑色
blackLower = (0, 0, 0)
blackUpper = (180, 255, 10)
"""
pts = deque(maxlen=args["buffer"])
inst_cache = deque(maxlen=50)
NUM = 0
"""
# old version 1
num = 0
RESULT = np.zeros((2, 1))
RESULT_count = 0
ZERO_count = 0
#Statistics = np.zeros((100, 1))
Count = np.zeros((3, 1))
"""
"""
# old version 2
ins_queue = deque(maxlen=100)
signal = []
zero_count = 0
plus_count = 0
minus_count = 0
"""
# file for write log
f = open("./updown.txt", "w+")
while True:
    """ used for analysis ball trace
    black = np.zeros((480, 640, 3), np.uint8)
    black.fill(0)
    """
    # create background picture
    # Capture frame-by-frame
    ret, frame = cap.read()
    # 第一个参数ret为True 或者False,代表有没有读取到图片，
    # 第二个参数frame表示截取到一帧的图片
    # Display the resulting frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#图片格式转换，RGB转换为HSV

    green_mask = cv2.inRange(hsv, greenLower, greenUpper)#可实现二值化功能
    green_mask = cv2.erode(green_mask, None, iterations=2)##腐蚀图像
    green_mask = cv2.dilate(green_mask, None, iterations=2)#膨胀图像
    """
    图像的开运算
    先进性腐蚀再进行膨胀就叫做开运算。
    就像我们上面介绍的那样，它被用来去除噪声。
    """
    #cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图）
    """
    返回值为3个，第一个image，和输入图像差别不大
    第二个得到图中的轮廓 cnts
    第三个  相应轮廓之间的关系
    """
    _, cnts, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # print(cnts)
    # time.sleep(100)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)#原代码直接就是cv2.findCountours返回的值
        # cv2.countourArea 按照默认方向计算轮廓面积（顺时针或逆时针）
        """
        图像的矩可以帮助我们计算图像的质心，面积等。
        函数cv2.moments()会将计算得到的矩以一个字典的形式返回。
        """
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10: #仅在半径满足最小尺寸时才进行
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    pts.appendleft(center)
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)#加拖尾特效的线
        # cv2.line(black, pts[i - 1], pts[i], (0, 0, 225), thickness)
        #print("pts",pts[i])
    cv2.imshow("Frame", frame)
    print(np.size(frame[1]))
    time.sleep(100)
    # new added
    print(pts)
    print(pts.count(None))
    points = []
    if pts.count(None) < 60:
        for item in pts:
            if item != None:
                points.append(item)
    first_sum_x = first_sum_y = 0
    second_sum_x = second_sum_y = 0
    for x, y in points[:int(len(points)/3)]:
        first_sum_x = first_sum_x + x
        first_sum_y = first_sum_y + y
    for x, y in points[int(len(points)*2/3):]:
        second_sum_x = second_sum_x + x
        second_sum_y = second_sum_y + y
   # print >> f, "old x", first_sum_x
    print("old x", first_sum_x)
  # print("new x", second_sum_x, file=f)
    print("new x", second_sum_x)
  #  print("old y", first_sum_y, file=f)
    print("old y", first_sum_y)
 #   print("new y", second_sum_y, file=f)
    print("new y", second_sum_y)
    if 100 < 3 * first_sum_x < second_sum_x:
       # print("****** right *************", file=f)
        print("****** right *************")
        inst_cache.append("right")
    elif first_sum_x > 3 * second_sum_x > 100:
      #  print("****** left *************", file=f)
        print("****** left *************")
        inst_cache.append("left")
    else:
      #  print("***** x no action *****************", file=f)
        print("***** x no action *****************")
        inst_cache.append(None)
    if 50 < 2 * first_sum_y < second_sum_y:
      #  print("****** up *************", file=f)
        print("****** up *************")
        inst_cache.append("up")
    elif first_sum_y > 2 * second_sum_y > 50:
        print("****** down *************", file=f)
        print("****** down *************")
        inst_cache.append("down")
    else:
      #  print("******** y no action **************", file=f)
        print("******** y no action **************")
        inst_cache.append(None)
    print("inst_cache", inst_cache, file=f)
    print("inst_cache", inst_cache)
    NUM = NUM + 1
    if NUM == 75:
        NUM = 0
        if inst_cache.count(None) < 40:
            final_instruction = max(["up", "down", "right", "left"], key=inst_cache.count)
            print("8888888888888888final_ins", final_instruction)
       #     print("8888888888888888final_ins", final_instruction, file=f)
            inst_cache = deque(maxlen=50)
            time.sleep(5)

    """
    # old version 2
    result = analys_trace.f(black)
    ins_queue.append(result)
    print(ins_queue)
    new_result = 2
    if len(ins_queue) == 100:
        new_result = max([0, 1, -1, 2], key=ins_queue.count)
    print("new_result", new_result)
    while new_result == 0 and zero_count < 1500:
        zero_count += 1
    print("zero_count", zero_count)
    if zero_count > 1000:
        # clear all
        zero_count = 0
        signal[0] = 0
        signal[1] = 0
    elif 10 < zero_count <= 100:
        # a space
        zero_count = 0
        signal[new_result] = True
    """

    """
    # old version 1
    num = num + 1
    #if num % 100 == 0:
        #cv2.imwrite("C:/dhj-learning/berkeley/robotic/EE106AProject/trace_ball/1-1.avi(%d).jpg" % num, black)
    result = analys_trace.f(black)
    #Statistics[(num-1) % 100] = result
    if result == -1:
        Count[0] = Count[0] + 1
    elif result == 0:
        Count[1] = Count[1] + 1
    elif result == 1:
        Count[2] = Count[2] + 1
    if num % 100 == 0:# and num != 1:
        print("num/100:", num / 100)
        if Count[0] >= Count[1] and Count[0] >= Count[2]:
            if ZERO_count > 0 or num == 100:
                RESULT[RESULT_count] = -1
                RESULT_count = RESULT_count + 1
                ZERO_count = 0
        elif Count[1] >= Count[2]:
                ZERO_count = ZERO_count + 1
                if ZERO_count > 2:
                    if RESULT[0] == 1 and RESULT[1] == 1:
                        print('up')
                    elif RESULT[0] == -1 and RESULT[1] == -1:
                        print('down')
                    elif RESULT[0] == 1 and RESULT[1] == -1:
                        print('left')
                    elif RESULT[0] == -1 and RESULT[1] == 1:
                        print('right')
                    ZERO_count = 0
                    RESULT[0] = 0
                    RESULT[1] = 0
                    RESULT_count = 0
        else:
            if ZERO_count > 0 or num == 100:
                RESULT[RESULT_count] = 1
                RESULT_count = RESULT_count + 1
                ZERO_count = 0
       # Statistics = np.zeros((100, 1))
        Count = np.zeros((3, 1))
        print("RESULT:", RESULT[0], RESULT[1])
        print("Zero_count:", ZERO_count)
        """

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ## 按'q'健退出循环
        break
cap.release()
cv2.destroyAllWindows()
