# Name:   aiml_server.py
# Author: Lentin Joseph
# Book:   Learning Robotics using Python 
# Date:   11-10-2016

#!/usr/bin/env python
import rospy
from std_msgs.msg import String
#Creating a publisher for chatter topic
pub = rospy.Publisher('chatter', String,queue_size=10)
rospy.init_node('aiml_client')
r = rospy.Rate(1) # 10hz
while not rospy.is_shutdown():
#Receiving text input from user
	input = raw_input("Enter your text :> ")
#Publishing to chatter topic
	pub.publish(input)
	r.sleep()
