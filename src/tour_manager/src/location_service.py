#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to save the current location of the robot to memory. It also starts
the navigation script which uses these location coordinates to navigate to
the point.
"""

###############################################################################
# A part of this code was adapted from the script found at:                   #
# https://github.com/reem-utils/reem_snippets/blob/master/scripts             #
# /get_current_robot_pose.py                                                  #
###############################################################################

from math import degrees

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion
from tour_manager.srv import *

import file_access
import navigation

FILE_NAME = "savedLocations.txt"

LOCATIONS = file_access.read_as_dictionary(FILE_NAME)


def write_to_file():
    file_access.write_dictionary(LOCATIONS, FILE_NAME)


class SaveLocationService:
    def __init__(self):

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.location_received = False

        rospy.Service('save_location', stdService, self.save_location)

        # Read the current pose topic
        rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped,
                         self.callback_pose)

    def callback_pose(self, data):
        self.x = data.pose.pose.position.x
        self.y = data.pose.pose.position.y
        _, _, self.yaw = euler_from_quaternion(
            [data.pose.pose.orientation.x, data.pose.pose.orientation.y,
             data.pose.pose.orientation.z, data.pose.pose.orientation.w])

        self.yaw = degrees(self.yaw)
        self.location_received = True

    def save_location(self, req):

        while not self.location_received:
            pass

        if req.data not in LOCATIONS:

            coordinates = [str(self.x), str(self.y), str(self.yaw)]

            LOCATIONS[req.data] = coordinates
            write_to_file()
            return stdServiceResponse(True)

        else:
            rospy.loginfo("Location name already exists")

        return stdServiceResponse(False)


def check_location(req):
    """
    Function to check if a location exists in the memory

    :param req: Consists string data that has the name of the location to be
    searched.
    :return: True if location exists else False
    """
    return stdServiceResponse(req.data in LOCATIONS)


if __name__ == '__main__':
    rospy.init_node('location_server')
    rospy.on_shutdown(write_to_file)

    SaveLocationService()
    navigation.initiate_navigate_to_service(LOCATIONS)
    rospy.Service('check_location', stdService, check_location)
    rospy.spin()
