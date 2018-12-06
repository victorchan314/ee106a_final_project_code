#!/usr/bin/env python
import rospy
from rosflight_msgs import Command

def call_computer_vision():
    '''Placeholder function for a call to the CV module later'''
    return 1
    pass

def commander():
    rospy.init_node('drone_commander')
    pub = rospy.Publisher('command', Command, queue_size=10)
    r = rospy.Rate(10)

    while not rospy.is_shutdown():
        direction = call_computer_vision()

        command = Command()
        command.mode = Command.MODE_ROLL_PITCH_YAWRATE_THROTTLE
        command.ignore = Command.IGNORE_NONE
        
        if direction == 1:
            command.F = 0.1
        elif direction == 2:
            command.x = 0.1
            command.F = 0.1
        elif direction == 3:
            command.F = -0.1
        elif direction == 4:
            command.x = -0.1
            command.F = 0.1

        print(command)
        pub.publish(command)
        rospy.sleep(10000)



if __name__ == '__main__':
    commander()
