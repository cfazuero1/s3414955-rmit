#!/usr/bin/env python

"""
Script to perform a tour by calling the right services in the right order.
"""

import time

import play_sound
import rospy
from ros_aiml.srv import *
from tour_manager.srv import *

import file_access

FILE_NAME = "tours.txt"

tours = None


def handle_request(req):

    """
    Function to handle requests when a client requests a tour service.
    :param req: The request consists of a tour name as well as a tour level.
    :return:
    """

    result = True

    if req.tourName in tours:

        play_sound.play("Welcome")

        i = 0

        for location_name in tours[req.tourName]:

            rospy.wait_for_service('navigate_to')
            rospy.wait_for_service('do_presentation')
            rospy.wait_for_service('google_recognizer_service')

            # Check if wav file exists

            try:
                poi_service = rospy.ServiceProxy('navigate_to', stdService)
                response = poi_service(location_name)
                if response.result:
                    rospy.loginfo("Successfully reached " + location_name)

                else:
                    rospy.loginfo(
                        "Unsuccessfully: unable to reach " + location_name)
                    result = False
                    break

            except rospy.ServiceException, e:
                print "Service call failed: %s" % e
                result = False

            try:
                presentation_service = rospy.ServiceProxy('do_presentation',
                                                          Presentation)
                response = presentation_service(location_name, req.tourLevel)

                if response.success:
                    rospy.loginfo("Successfully presented " + location_name)

                else:
                    rospy.loginfo(
                        "Unsuccessfully: unable find presentation for " +
                        location_name)

            except rospy.ServiceException, e:
                print "Presentation Service call failed: %s" % e

            time.sleep(1)

            try:

                play_sound.play("Any_Questions")
                qna_service = rospy.ServiceProxy('google_recognizer_service',
                                                 Empty)
                qna_service(True)

            except rospy.ServiceException, e:
                print "Service call failed: %s" % e

            i += 1
            if i < len(tours[req.tourName]):
                play_sound.play("Move_On")

            else:
                play_sound.play("End")

    else:
        rospy.loginfo(
            "Tour does not exist" + req.tourName + " : " + req.tourLevel)
        result = False

    return doTourResponse(result)


def initiate_do_tour_service(tours_dict=None):
    """
    Function to start the 'do_tour' service with the with the right tour
    dictionary
    :param tours_dict: The dictionary that must be used. If this node is run
    by itself, the tours would be read from the file.
    :return:
    """

    global tours

    if tours_dict is None:
        tours = file_access.read_as_dictionary(FILE_NAME)
    else:
        tours = tours_dict

    rospy.Service('do_tour', doTour, handle_request)


if __name__ == "__main__":
    rospy.init_node('do_tour_server')
    initiate_do_tour_service()
    rospy.spin()
