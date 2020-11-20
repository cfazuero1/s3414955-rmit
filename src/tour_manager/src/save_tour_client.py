#!/usr/bin/env python

"""
A wrapper script to add locations to tours by calling the service with the
right format of arguments.
"""

import sys

import rospy
from tour_manager.srv import *


def usage():
    print "%s <tour name> <location names>" % sys.argv[0]
    sys.exit(1)


def save_tour(tour_name, locations):
    rospy.wait_for_service('check_location')

    try:
        location_exist = rospy.ServiceProxy('check_location', stdService)
        for location in locations:
            if not location_exist(location).result:
                rospy.loginfo("Location " + location + " does not exist")
                return False

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
        return False

    rospy.wait_for_service('save_tour')

    try:
        save_tour_service = rospy.ServiceProxy('save_tour', tour)
        response = save_tour_service(tour_name, locations)
        if response.result:
            rospy.loginfo("Successfully saved tour: " + tour_name)
            return True

        else:
            rospy.loginfo("Unsuccessful, could not save tour: " + tour_name)
            return False

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
        return False


if __name__ == "__main__":

    if len(sys.argv) > 2:
        save_tour(sys.argv[1], sys.argv[2:])

    else:
        usage()
