#!/usr/bin/env python

"""
A wrapper script to do tours by calling the service with the right format of
arguments.
"""

import sys

import rospy
from tour_manager.srv import doTour


def usage():
    print "%s <tour name> \n" % sys.argv[0]
    sys.exit(1)


def do_tour(tour_name, tour_level):
    rospy.wait_for_service('do_tour')
    tour_level = tour_level.lower()

    if tour_level in ["advance", "intermediate", "basic"]:
        level = tour_level[:3]
    else:
        rospy.loginfo("Incorrect tour level: " + tour_level)
        rospy.loginfo("Choose between 'advance', 'intermediate' or 'basic' ")
        return False

    try:
        do_tour_service = rospy.ServiceProxy('do_tour', doTour)
        response = do_tour_service(tour_name, level)
        if response.result:
            rospy.loginfo("Successfully completed tour: " + tour_name)
            return True

        else:
            rospy.loginfo("Unsuccessful, can not do tour: " + tour_name)
            return False

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e
        return False


if __name__ == "__main__":

    if len(sys.argv) == 3:
        do_tour(sys.argv[1], sys.argv[2])

    else:
        usage()
