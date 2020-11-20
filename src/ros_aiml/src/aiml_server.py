# Name:   aiml_server.py
# Author: Lentin Joseph
# Book:   Learning Robotics using Python 
# Date:   11-10-2016

#!/usr/bin/env python
import rospy
import aiml
import os
import sys
from tour_manager.srv import *
from std_msgs.msg import String


class AimlServer:

	def __init__(self):
		rospy.init_node('aiml_server')
		self.mybot = aiml.Kernel()
		# Creating a ROS publisher for the /response topic
		rospy.Service("aiml_client_to_aiml_server", speech, self.get_speech)
		self.xml_file = 'startup.xml'

		# Load AIML files using bootstrap() method
		data_path = rospy.get_param("aiml_path")
		os.chdir(data_path)
		if os.path.isfile("standard.brn"):
			self.mybot.bootstrap(brainFile = "standard.brn")
		else:
			self.mybot.bootstrap(learnFiles = self.xml_file, commands = "load aiml b")
			self.mybot.saveBrain("standard.brn")
		rospy.spin()

	# It will receive input from user
	# and feed to respond() method of Kernel() object. and print the results
	def callback(self, data):
		input = data
		response = self.mybot.respond(input)
		rospy.loginfo("I heard:: %s", data)
		rospy.loginfo("I spoke:: %s", response)
		rospy.wait_for_service('aiml_to_watson')
		try:
			recognizer = rospy.ServiceProxy('aiml_to_watson', speech)
			recognizer(response)
		except rospy.ServiceException, e:
			print "Service call failed: %s" % e

	def get_speech(self, req):
		chatter = req.data
		self.callback(chatter)

	def stop_recognizer(self):
		rospy.wait_for_service('recognizer_service')
		try:
			recognizer = rospy.ServiceProxy('recognizer_service', Empty)
			response = recognizer(False)
			if response.result:
				rospy.loginfo('Stop recognizer')
			else:
				rospy.loginfo('Start recognizer')
			return response.result
		except rospy.ServiceException, e:
			print "Service call failed: %s" % e

if __name__ == '__main__':
	AimlServer()
