#!/usr/bin/env python

###############################################################################
# A part of this code was adapted from the script found at:                   #
# https://github.com/Uberi/speech_recognition/blob/master/speech_recognition  #
# /__main__.py                                                                #
###############################################################################

import random

import play_sound
import rospy
import speech_recognition as sr
from tour_manager.srv import *


def get_speech(data):
    speech_text = data
    rospy.loginfo("Google said:: %s", speech_text)
    rospy.wait_for_service('recognizer_to_aiml_client')
    try:
        recognizer = rospy.ServiceProxy('recognizer_to_aiml_client', speech)
        recognizer(speech_text)
        print("test....!!!")
    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


class GoogleSpeech:
    def __init__(self):
        rospy.init_node('google_recognizer')
        rospy.Service('google_recognizer_service', Empty, self.listener)
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        rospy.spin()
        # self.started = False

    def listener(self, req):
        rospy.loginfo("Starting Google Speech Recognition")
        is_active = True

        print("A moment of silence, please...")
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
            rospy.loginfo("Set minimum energy threshold to {}".format(
                self.r.energy_threshold))
            self.r.dynamic_energy_threshold = False

        while is_active:
            print("Say something!")

            try:
                with self.m as source:
                    audio = self.r.listen(source, timeout=5)
                print("Got it! Now to recognize it...")

                try:
                    value = self.r.recognize_google(audio)

                    if str is bytes:
                        print(
                        u"You said (Google) {}".format(value).encode("UTF-8"))
                        data = u"{}".format(value).encode("UTF-8")

                        if data.lower() == "no":
                            rospy.loginfo("Exiting Q&A")
                            is_active = False
                            break
                        else:
                            get_speech(data)
                    else:
                        print("You said {}".format(value))

                        if value.lower() == "no":
                            rospy.loginfo("Exiting Q&A")
                            is_active = False
                            break
                        else:
                            get_speech(value)

                    play_sound.play("Any_More_Questions")

                except sr.UnknownValueError:
                    print("Oops! Didn't catch that")
                    play_sound.play(
                        random.choice(["Sorry", "Excuse_Me", "Pardon"]))

                except sr.RequestError as e:
                    print("Uh oh! Couldn't request results from Google "
                          "Speech Recognition service; {0}".format(e))

            except sr.WaitTimeoutError:
                rospy.loginfo("Exiting Q&A")
                is_active = False

        return EmptyResponse(True)


if __name__ == '__main__':
    GoogleSpeech()
