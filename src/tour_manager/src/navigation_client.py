#!/usr/bin/env python

"""
A wrapper script to send the robot to a location by calling the service with
the right format of arguments.
"""

import sys

import rospy
from tour_manager.srv import *


def usage():
    print "%s <location name> " % sys.argv[0]
    sys.exit(1)


def go_to_location(location_name):
    rospy.wait_for_service('navigate_to')

    try:
        navigate_to_service = rospy.ServiceProxy('navigate_to', stdService)
        response = navigate_to_service(location_name)
        if response.result:
            rospy.loginfo("Successfully navigated to " + location_name)
            return True

        else:
            rospy.loginfo("Unsuccessful, can not navigate to " + location_name)
            return False

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
        return False


if __name__ == "__main__":

    if len(sys.argv) == 2:
        go_to_location(sys.argv[1])

    else:
        usage()
