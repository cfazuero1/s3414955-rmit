#!/usr/bin/env python

################################################################################################
# Script to implement Pocketsphinx speech recogniser using custom Dictionary and Grammar files #
# A part of this code was adapted from the script found at:                                    #
# https://github.com/mikeferguson/pocketsphinx                                                 #
# recognizer.py                                                                                #
# AND                                                                                          #  
# Learing Robotics using Python by Lentin Joseph                                               #  
################################################################################################

import gobject
import sys
import pygst
import rospy
import os
pygst.require('0.10')
gobject.threads_init()
import gst
import signal
import roslib;

roslib.load_manifest('ros_aiml')
import pygtk

pygtk.require('2.0')
import gtk
from std_msgs.msg import String
from tour_manager.srv import *
import commands


# Keyboard signal handling routine
def signal_handle(signal, frame):
    print "You pressed Ctrl+C"
    sys.exit(0)


# Implementation of Speech recognition class
class Speech_Recog(object):
    # Initializing gstreamer pipeline and pocket sphinx element
    def __init__(self):
        # Start node
        rospy.init_node("recognizer")
        # Find the name of your microphone by typing pacmd list-sources in the terminal
        self._device_name_param = "~mic_name"
        self._dic_param = "~dict"
        self._fsg_param = "~fsg"

        # Configure mics with gstreamer launch config
        if rospy.has_param(self._device_name_param):
            self.device_name = rospy.get_param(self._device_name_param)
            self.device_index = pulse_index_from_name(self.device_name)
            self.launch_config = "pulsesrc device=" + str(self.device_index)
            rospy.loginfo("Using: pulsesrc device=%s name=%s",
                          self.device_index, self.device_name)
        elif rospy.has_param('~source'):
            # common sources: 'alsasrc'
            self.launch_config = rospy.get_param('~source')
        else:
            self.launch_config = 'gconfaudiosrc'

        rospy.loginfo("Launch config: %s", self.launch_config)

        self.pipeline = gst.parse_launch(
            'gconfaudiosrc !audioconvert ! audioresample '
            + '! pocketsphinx name=asr ! fakesink')
        # Configure ROS settings
        self.started = False
        rospy.on_shutdown(self.shutdown)
        rospy.Service("recognizer_service", Empty, self.recognizer_service)

        # Accessing pocket sphinx element from gstreamer pipeline
        self.asr = self.pipeline.get_by_name('asr')
        # Connecting to asr_result function when a speech to text conversion is completed
        self.asr.connect('result', self.asr_result)
        # Configure language model
        if rospy.has_param(self._dic_param):
            dic = rospy.get_param(self._dic_param)
        else:
            rospy.logerr('Recognizer not started. Please specify a dictionary.')
            return

        if rospy.has_param(self._fsg_param):
            fsg = rospy.get_param(self._fsg_param)
        else:
            rospy.logerr('Recognizer not started. Please specify a grammar.')
            return
        # User can mention lm and dict for accurate detection
        self.asr.set_property('fsg', fsg)
        self.asr.set_property('dict', dic)
        # This option will set all options are configured well and can start recognition
        self.asr.set_property('configured', True)
        self.asr.set_property('dsratio', 1)

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus_id = self.bus.connect('message::application',
                                       self.application_message)

        # Pausing the GStreamer pipeline at first.
        self.pipeline.set_state(gst.STATE_PLAYING)
        self.started = True

    # Definition of asr_result
    def asr_result(self, asr, text, uttid):
        # Printing the detected text
        struct = gst.Structure('result')
        struct.set_value('hyp', text)
        struct.set_value('uttid', uttid)
        asr.post_message(gst.message_new_application(asr, struct))

    def recognizer_service(self, req):

        self.set_service_status(req.flag)

    def set_service_status(self, is_active):
        if is_active:
            rospy.loginfo("Recognizer starting again")
            self.pipeline.set_state(gst.STATE_PLAYING)
            self.started = True
            rospy.loginfo("Recognizer has started ")

        else:
            rospy.loginfo("Recognizer stopping")
            self.pipeline.set_state(gst.STATE_PAUSED)
            self.started = False
            rospy.loginfo("Recognizer stopped")

        return self.started

    def stop_recognition(self):
        if self.started:
            self.pipeline.set_state(gst.STATE_NULL)
            self.pipeline.remove(self.asr)
            self.bus.disconnect(self.bus_id)
            self.started = False

    def shutdown(self):
        """ Delete any remaining parameters so they don't affect next launch """
        for param in [self._device_name_param, self._fsg_param,
                      self._dic_param]:
            if rospy.has_param(param):
                rospy.delete_param(param)

        """ Shutdown the GTK thread. """
        gtk.main_quit()

    def application_message(self, bus, msg):
        """ Receive application messages from the bus. """
        msgtype = msg.structure.get_name()
        self.final_result(msg.structure['hyp'], msg.structure['uttid'])

    def final_result(self, hyp, uttid):
        """ Insert the final result. """
        msg = String()
        msg.data = str(hyp.lower())
        rospy.loginfo(msg.data)
        # self.pub.publish(msg)
        rospy.wait_for_service('command_processing')
        try:
            self.set_service_status(False)
            recognizer = rospy.ServiceProxy('command_processing', stdService)
            command_received = msg.data.lower().replace("okay chip ", "", 1)
            result = recognizer(command_received)
            rospy.loginfo(result.result)
            self.set_service_status(True)
        except rospy.ServiceException, e:
            print "Service call failed: %s" % e


def pulse_index_from_name(name):
    output = commands.getstatusoutput(
        "pacmd list-sources | grep -B 1 'name: <" + name
        + ">' | grep -o -P '(?<=index: )[0-9]*'")

    if len(output) == 2:
        return output[1]
    else:
        raise Exception(
            "Error. pulse index doesn't exist for name: " + name)


if __name__ == "__main__":
    # Assign keyboard interrupt handler
    signal.signal(signal.SIGINT, signal_handle)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Creating an object of Speech_Recog() class
    app_object = Speech_Recog()
    # Calling Speech recognition routine
    gtk.main()
