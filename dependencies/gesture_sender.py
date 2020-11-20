#!/usr/bin/python

import sys
import actionlib
import rospy

from play_motion_msgs.msg import PlayMotionAction, PlayMotionGoal, PlayMotionResult
from actionlib_msgs.msg import *

class GestureSender:
	def __init__(self):
		self.cli_ = actionlib.SimpleActionClient('/play_motion', PlayMotionAction)
		#rospy.loginfo("Gesture sender created.")
		self.cli_.wait_for_server();
		#rospy.loginfo("Server response received.")

	def send_motion_free(self, name): #//Just fire off the command, don't bother waiting for a result
		self.goal_ = PlayMotionGoal()
		self.goal_.motion_name = name
		self.goal_.skip_planning = True
		rospy.loginfo("Freely executing motion: " + name)
		self.cli_.send_goal(self.goal_)
		#rospy.loginfo("Goal sent.")

	def send_motion_timeout(self, name, waittime):
		#rospy.loginfo("motion received: " + name + ", timeout " + str(waittime))
		self.send_motion_free(name)
		self.cli_.wait_for_result(rospy.Duration(waittime))
		#rospy.loginfo("Wait complete, sending result.")
		return self.cli_.get_result()

	def send_motion(self, name):
		#rospy.loginfo("infinite time motion received: " + name)
		return self.send_motion_timeout(name, 0.0)

	def quitIt(self):
		#rospy.loginfo("Cancelling current goal")
		self.cli_.cancel_all_goals()
		rospy.sleep(0.25)
		#self.cli_.cancel_goal()

	def running(self):
		return self.cli_.get_state() != GoalStatus.LOST

if __name__ == "__main__":
	if len(sys.argv) > 1:
		rospy.init_node("gesture_sender")
		sender = GestureSender()
		sender.send_motion_timeout(sys.argv[1], 1.0)
		if len(sys.argv) > 2:
			sender.quitIt()
			sender.send_motion_free(sys.argv[2])
