#! /usr/bin/env python

"""
Script to navigate the robot to a location coordinate and an orientation.
"""

###############################################################################
# A part of this code was adapted from the script found at:                   #
# https://github.com/reem-utils/reem_snippets/blob/master/scripts             #
# /navigation.py                                                              #
###############################################################################

from math import radians

import actionlib
import rospy
from geometry_msgs.msg import Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from tour_manager.srv import *

import file_access

FILE_NAME = "savedLocations.txt"

locations = None


def handle_request(req):
    if req.data in locations:
        result = navigate_to(locations[req.data])

        if result == 3:
            rospy.loginfo("Destination Arrived")
            return stdServiceResponse(True)

        else:
            if result == 4:
                rospy.loginfo("Request Aborted: couldn't get there")

            else:
                rospy.loginfo("Request Rejected")

    else:
        rospy.loginfo("Location does not exist")

    return stdServiceResponse(False)


def create_nav_goal(x, y, yaw):
    """Create a MoveBaseGoal with x, y position and yaw rotation (in degrees).
    Returns a MoveBaseGoal"""
    mb_goal = MoveBaseGoal()
    mb_goal.target_pose.header.frame_id = '/map'  # Note: the frame_id must be
    #  map
    mb_goal.target_pose.pose.position.x = x
    mb_goal.target_pose.pose.position.y = y
    mb_goal.target_pose.pose.position.z = 0.0  # z must be 0.0 (no height in
    # the map)

    # Orientation of the robot is expressed in the yaw value of euler angles
    angle = radians(yaw)  # angles are expressed in radians
    quat = quaternion_from_euler(0.0, 0.0, angle)  # roll, pitch, yaw
    mb_goal.target_pose.pose.orientation = Quaternion(*quat.tolist())

    return mb_goal


def navigate_to(position):
    """
    Function to navigate to robot.
    :param position: Location coordinates
    :return: State of navigation:   3 is SUCCESS,
                                    4 is ABORTED (couldn't get there),
                                    5 REJECTED (the goal is not attainable)
    """
    # Connect to the navigation action server
    nav_as = actionlib.SimpleActionClient('/move_base', MoveBaseAction)
    rospy.loginfo("Connecting to /move_base AS...")
    nav_as.wait_for_server()
    rospy.loginfo("Connected.")

    rospy.loginfo("Creating navigation goal...")
    nav_goal = create_nav_goal(float(position[0]), float(position[1]),
                               float(position[2]))
    rospy.loginfo("Sending goal...")
    nav_as.send_goal(nav_goal)
    rospy.loginfo("Waiting for result...")
    nav_as.wait_for_result()
    nav_res = nav_as.get_result()
    nav_state = nav_as.get_state()
    rospy.loginfo("Done!")
    print "Result: ", str(nav_res)  # always empty, be careful
    # use this, 3 is SUCCESS, 4 is ABORTED (couldn't get there), 5 REJECTED (
    # the goal is not attainable)
    print "Nav state: ", str(nav_state)
    return nav_state


def initiate_navigate_to_service(locations_dict=None):
    """
    Function to start the 'navigate_to' service with the with the right
    locations dictionary
    :param locations_dict: The dictionary that must be used. If this node is run
    by itself, the locations would be read from the file.
    :return:
    """
    global locations

    if locations_dict is None:
        locations = file_access.read_as_dictionary(FILE_NAME)
    else:
        locations = locations_dict

    rospy.Service('navigate_to', stdService, handle_request)


if __name__ == '__main__':
    rospy.init_node('navigate_to_server')

    initiate_navigate_to_service()
    rospy.spin()
