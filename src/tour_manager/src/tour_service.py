#!/usr/bin/env python

"""
Script to save location names to tours. It also starts the do_tours script
which uses this tour dictionary to execute a tour.
"""

import rospy
from tour_manager.srv import *

import do_tours
import file_access

FILE_NAME = "tours.txt"

TOURS = file_access.read_as_dictionary(FILE_NAME)


def handle_save_tour_request(req):
    if req.tourName not in TOURS:
        TOURS[req.tourName] = req.locations

    else:
        TOURS[req.tourName].extend(req.locations)

    write_to_file()

    return tourResponse(True)


def write_to_file():
    file_access.write_dictionary(TOURS, FILE_NAME)


if __name__ == "__main__":
    rospy.init_node('tour_server')
    rospy.on_shutdown(write_to_file)

    rospy.Service('save_tour', tour, handle_save_tour_request)
    do_tours.initiate_do_tour_service(TOURS)

    rospy.spin()
