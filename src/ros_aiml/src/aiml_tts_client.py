# Name:   aiml_server.py
# Author: Lentin Joseph
# Book:   Learning Robotics using Python 
# Date:   11-10-2016

#!/usr/bin/env python
import rospy, os, sys
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
rospy.init_node('aiml_soundplay_client', anonymous = True)
soundhandle = SoundClient()
rospy.sleep(1)
soundhandle.stopAll()
print 'Starting TTS'
#Call back method to receive text from /response topic and convert to speech
def get_response(data):
	response = data.data
	rospy.loginfo("Response ::%s",response)
	soundhandle.say(response)
#Method to create a subscriber for /response topic.
def listener():
	rospy.loginfo("Starting listening to response")
	rospy.Subscriber("response",String, get_response,queue_size=10)
	rospy.spin()
if __name__ == '__main__':
	listener()
