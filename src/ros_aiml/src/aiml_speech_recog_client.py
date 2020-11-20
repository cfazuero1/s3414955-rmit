#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from tour_manager.srv import *


class AimlClient:

	def __init__(self):
		rospy.init_node('aiml_speech_recog_client')
		rospy.Service("recognizer_to_aiml_client", speech, self.get_speech)
		self.r = rospy.Rate(1) # 10hz
		rospy.loginfo("Starting Speech Recognition")
		rospy.spin()

	# The output of pocketsphinx package is sending converted text to aiml_client_to_aiml_server service.
	# The following function is the callback of this service.
	# The text will receive and send through the service, which is received by AIML server
	def get_speech(self, req):
		speech_text = req.data
		rospy.loginfo("I said:: %s",speech_text)
		# pub.publish(speech_text)
		rospy.wait_for_service('aiml_client_to_aiml_server')
		try:
			recognizer = rospy.ServiceProxy('aiml_client_to_aiml_server', speech)
			recognizer(speech_text)
		except rospy.ServiceException, e:
			print "Service call failed: %s" % e


if __name__ == '__main__':
	AimlClient()
