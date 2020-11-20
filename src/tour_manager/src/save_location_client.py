#!/usr/bin/env python

"""
A wrapper script to save the location coordinates by calling the service with
the right format of arguments.
"""

import sys

import rospy
from tour_manager.srv import *


def save_location(location_name):
    rospy.wait_for_service('save_location')

    try:
        poi_service = rospy.ServiceProxy('save_location', stdService)
        response = poi_service(location_name)
        if response.result:
            rospy.loginfo("Successfully saved location as " + location_name)
            return True

        else:
            rospy.loginfo(
                "Unsuccessful, could not save the location as " + location_name)
            return False

    except rospy.ServiceException, e:
        rospy.loginfo("Service call failed: %s" % e)
        return False


def usage():
    print "%s <location name> " % sys.argv[0]
    sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        save_location(sys.argv[1])

    else:
        usage()
