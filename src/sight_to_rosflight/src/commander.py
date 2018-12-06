#!/usr/bin/env python
import rospy
from rosflight_msgs.msg import Command
from trace_ball.get_trace_of_ball_function import get_trace_of_ball
from camera_color import capture_image, get_direction

import os
import signal
import numpy as np

def handler(signum, frame):
    raise Exception("Timeout handler")

def call_computer_vision():
    # return [1, 2, 3, 4][np.random.randint(4)]
    signal.alarm(30)
    
    d = -1
    try:
        d = get_trace_of_ball()
        signal.alarm(0)
    except Exception, exc:
         pass
    
    print("Direction: " + str(d))
     
    return d
    # d = -1
    # capture_image()
    # 
    # while not os.path.exists("image.jpg"):
    #     rospy.sleep(1)
    # 
    # d = get_direction()
    # rospy.sleep(5)
    # os.system("rm image.jpg")
    # 
    # return d

def commander():
    rospy.init_node('drone_commander')
    pub = rospy.Publisher('command', Command, queue_size=10)
    r = rospy.Rate(10)

    while not rospy.is_shutdown():
        direction = call_computer_vision()

        command = Command()
        command.mode = Command.MODE_ROLL_PITCH_YAWRATE_THROTTLE
        command.ignore = Command.IGNORE_NONE
        
        if direction == 0:
            command.F = 0.1
        elif direction == 1:
            command.x = 0.1
            command.F = 0.1
        elif direction == 2:
            command.F = -0.1
        elif direction == 3:
            command.x = -0.1
            command.F = 0.1
        else:
            print("No direction returned")
        
        if direction != -1:
            pub.publish(command)
        
        rospy.sleep(5)



if __name__ == '__main__':
    signal.signal(signal.SIGALRM, handler)
    commander()
