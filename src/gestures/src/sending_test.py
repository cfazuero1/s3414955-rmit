#!/usr/bin/python

import sys
import rospy
from gesture_sender import GestureSender
import time

rospy.init_node("sending_test")
sendo = GestureSender()
sendo.send_motion("arms_t")
sendo.send_motion_timeout("strong_arms", 5.0)
sendo.send_motion_free("aok")
time.sleep(1)
sendo.quitIt
time.sleep(3)
#the next motion seems to fail becaus the previous motion is still in operation?
sendo.send_motion_free("literally")
time.sleep(1)
