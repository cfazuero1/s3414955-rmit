#!/usr/bin/env python

"""
Script for command processing. This script will accept text input and convert
them to arguments which will be used to call the appropriate services based
text received.
"""

import play_sound
import rospy
import sound_file
from tour_manager.srv import *

import do_tour_client
import navigation_client
import save_location_client
import save_tour_client

PAUSED = False

keywords_to_command = {
    'stop': ['stop', 'halt', 'abort', 'kill', 'panic', 'off', 'freeze',
             'shut down', 'turn off', 'help', 'help me'],
    'slower': ['slow down', 'slower'], 'faster': ['speed up', 'faster'],
    'forward': ['forward', 'ahead', 'straight'],
    'backward': ['back', 'backward', 'back up'], 'rotate left': ['rotate left'],
    'rotate right': ['rotate right'], 'turn left': ['turn left'],
    'turn right': ['turn right'], 'quarter': ['quarter speed'],
    'half': ['half speed'], 'full': ['full speed'], 'pause': ['pause speech'],
    'continue': ['continue speech']
}


def get_command(data):
    # Attempt to match the recognized word or phrase to the
    # keywords_to_command dictionary and return the appropriate
    # command
    for (command, keywords) in keywords_to_command.iteritems():
        for word in keywords:
            if data.find(word) > -1:
                return command


def handle_request(req):
    global PAUSED

    command_received = req.data

    move_command = get_command(command_received)

    if move_command is not None:

        # If the user has asked to pause/continue voice control,
        # set the flag accordingly
        if move_command == 'pause':
            PAUSED = True

        elif move_command == 'continue':
            PAUSED = False
            return stdServiceResponse(True)

        # If voice control is paused, simply return without
        # performing any action
        if PAUSED:
            rospy.loginfo("Speech input is paused")
            return stdServiceResponse(True)

        rospy.wait_for_service('motion_service')
        motion_service = rospy.ServiceProxy('motion_service', stdService)
        response = motion_service(move_command)

        if response.result:
            rospy.loginfo("Successfully executed command: " + move_command)

        else:
            rospy.loginfo(
                "Unsuccessfully: unable to executed command " + move_command)

        return stdServiceResponse(response.result)

    else:

        # If voice control is paused, simply return without
        # performing any action
        if PAUSED:
            rospy.loginfo("Speech input is paused")
            return stdServiceResponse(True)

        rospy.wait_for_service('motion_service')
        motion_service = rospy.ServiceProxy('motion_service', stdService)
        response = motion_service('stop')

        if response.result:
            rospy.loginfo("Successfully stopped all motion services")

        else:
            rospy.loginfo(
                "Unable to stop motion services before executing command")
            return stdServiceResponse(False)

        is_to_do_tour, is_do_tour_success = do_tour(command_received)
        if is_to_do_tour:
            return stdServiceResponse(is_do_tour_success)

        is_to_go_to_loc, is_go_to_loc_success = go_to_location(command_received)
        if is_to_go_to_loc:
            return stdServiceResponse(is_go_to_loc_success)

        is_to_save_tour, is_save_tour_success = save_tour(command_received)
        if is_to_save_tour:
            return stdServiceResponse(is_save_tour_success)

        is_to_save_loc, is_save_loc_success = save_location(command_received)
        if is_to_save_loc:
            return stdServiceResponse(is_save_loc_success)

        return stdServiceResponse(False)


def save_location(msg):
    index = msg.lower().find("save this location as")

    if index > -1:
        loc_name = msg[index:].lower().replace("save this location as ", "", 1)

        is_save_loc_success = save_location_client.save_location(loc_name)

        if is_save_loc_success:
            text_to_speak = "Location saved as " + loc_name
            sound_file.create_wave(text_to_speak, loc_name)
            play_sound.play("Location_saved")
            # play_sound.speak_text(text_to_speak)
            # play_sound.play("Location_saved_as")
            play_sound.play(loc_name)
            sound_file.delete_wave(loc_name)

        else:
            play_sound.play("Location_not_saved")

        return True, is_save_loc_success

    return False, False


def go_to_location(msg):
    loc = msg.lower().find("go to")

    if loc > -1:
        location_name = msg[loc:].lower().replace("go to ", "", 1)

        return True, navigation_client.go_to_location(location_name)

    return False, False


def save_tour(msg):
    loc = msg.lower().find("add location")

    if loc > -1:
        input_string = msg[loc:].lower().replace("add location ", "", 1)

        if " to tour " in input_string:
            location_name, tour_name = input_string.split(" to tour ", 1)

            is_save_tour_success = save_tour_client.save_tour(tour_name,
                                                              [location_name])

            if is_save_tour_success:
                to_say = location_name + " added to " + tour_name
                sound_file.create_wave(to_say, tour_name)
                play_sound.play("Tour_saved")
                # play_sound.speak_text(to_say)
                play_sound.play(tour_name)
                sound_file.delete_wave(tour_name)
            else:
                play_sound.play("Tour_not_saved")

            return True, is_save_tour_success

    return False, False


def do_tour(msg):
    loc = msg.lower().find("execute tour")

    if loc > -1:
        msg = msg[loc:].lower().replace("execute tour ", "", 1)
        tour_name, tour_level = msg.split(" in ", 1)
        tour_level = tour_level.replace(" mode", "")

        return True, do_tour_client.do_tour(tour_name, tour_level)

    return False, False


if __name__ == "__main__":
    rospy.init_node('command_brain')
    rospy.Service('command_processing', stdService, handle_request)
    rospy.spin()
