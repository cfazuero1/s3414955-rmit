#!/usr/bin/env python
import rospy
import time
import speech_recognition as sr
from std_msgs.msg import String

rospy.init_node('aiml_speech_recog_client')
pub = rospy.Publisher('chatter', String,queue_size=10)
r = sr.Recognizer()
m = sr.Microphone()

#The output of pocketsphinx package is sending converted text to /recognizer/output topic. The following function is the callback of this topic. The text will receive and send through /chatter topic, which is received by AIML server
def get_speech(data):
   speech_text=data
   rospy.loginfo("I said:: %s",speech_text)
   pub.publish(speech_text)
   time.sleep(1)
#Creating a subscriber for pocketsphinx output topic /recognizer/output
def listener():
   rospy.loginfo("Starting Speech Recognition")
   try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}")
    r.energy_threshold
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            # we need some special handling here to correctly print unicode characters to standard output
            if str is bytes: # this version of Python uses bytes for strings (Python 2)
                print(u"You said (Google) {}".format(value).encode("utf-8"))
                data=u"{}".format(value).encode("utf-8")
                get_speech(data)
            else: # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
           # print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
	    value2 = r.recognize_sphinx(audio)
	    if str is bytes: # this version of Python uses bytes for strings (Python 2)
                #print(u"You said (Internal) {}".format(value2).encode("utf-8"))
                print("ERROR")
            else: # this version of Python uses unicode for strings (Python 3+)
                #print("You also said {}".format(value2))
                print("ERROR")

   except KeyboardInterrupt:
    	  pass

if __name__ == '__main__':
   listener()
