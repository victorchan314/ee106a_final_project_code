# -*- coding: utf-8 -*-
from __future__ import print_function 
import cv2
import numpy as np
from collections import deque
import argparse
#import analys_trace
# for debug
import time

def get_trace_of_ball():
        num = 300
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

	pts = deque(maxlen=args["buffer"])
	inst_cache = deque(maxlen=50)
	NUM = 0

	# file for write log
	#f = open("./updown.txt", "w+")
	while num != 0:
            num = num - 1
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
	    # new added
	    print(pts)
	    print(pts.count(None))
	    points = []
	    if pts.count(None) < 61:
	        for item in pts:
	            if item != None:
	                points.append(item)
	    first_sum_x = first_sum_y = 0
	    second_sum_x = second_sum_y = 0
	    for x, y in points[:int(len(points)/2)]:
	        first_sum_x = first_sum_x + x
	        first_sum_y = first_sum_y + y
	    for x, y in points[int(len(points)*1/2):]:
	        second_sum_x = second_sum_x + x
	        second_sum_y = second_sum_y + y
	    # print >> f, "old x", first_sum_x
	    print("old x", first_sum_x)
	    # print("new x", second_sum_x, file=f)
	    print("new x", second_sum_x)
	    # print("old y", first_sum_y, file=f)
	    print("old y", first_sum_y)
	    # print("new y", second_sum_y, file=f)
	    print("new y", second_sum_y)
	    if 100 <  2.5* first_sum_x < second_sum_x:
	        # prin("****** right *************", file=f)
	        print("****** right *************")
	        inst_cache.append("right")
	    elif first_sum_x > 2.5 * second_sum_x > 100:
	        # print("****** left *************", file=f)
	        print("****** left *************")
	        inst_cache.append("left")
	    else:
	        # print("***** x no action *****************", file=f)
	        print("***** x no action *****************")
	        inst_cache.append(None)
	    if 100 < 2.5 * first_sum_y < second_sum_y:
	        # print("****** up *************", file=f)
	        print("****** up *************")
	        inst_cache.append("up")
	    elif first_sum_y > 2.5 * second_sum_y > 100:
	        # print("****** down *************", file=f)
	        print("****** down *************")
	        inst_cache.append("down")
	    else:
	        # print("******** y no action **************", file=f)
	        print("******** y no action **************")
	        inst_cache.append(None)
	    #print("inst_cache", inst_cache, file=f)
	    print("inst_cache", inst_cache)
	    NUM = NUM + 1
	    if NUM == 75:
	        NUM = 0
	        if inst_cache.count(None) < 40:
	            final_instruction = max(["up", "down", "right", "left"], key=inst_cache.count)
	            print("8888888888888888final_ins", final_instruction)
	            # print("8888888888888888final_ins", final_instruction, file=f)
                    cap.release()
                    cv2.destroyAllWindows()
                    if final_instruction == "up":
                        return 0
                    elif final_instruction == "down":
                        return 1
                    elif final_instruction == "left":
                        return 2
                    elif final_instruction == "right":
                        return 3
	
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
            if num == 0:
                cap.release()
                cv2.destroyAllWindows()

        return -1
