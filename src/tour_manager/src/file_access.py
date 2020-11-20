#!/usr/bin/env python

"""
A helper script to read and write contents from and to files.
"""

import os
import sys
import tempfile

from shutil import move

KEY_DELIMITER = "->"
VALUE_DELIMITER = ":"
COMMENT_STRING = "#"
FILE_LOCATION = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))),
    'savedFiles')


def read_as_dictionary(name_of_file, file_location=None):
    if file_location is None:
        file_location = FILE_LOCATION

    file_name = os.path.join(file_location, name_of_file)

    dictionary = dict()
    try:
        if os.path.exists(file_name):
            with open(file_name, 'r') as fh:
                for line in fh:
                    if not line.startswith(COMMENT_STRING):
                        key_value_pair = line.strip().split(KEY_DELIMITER)
                        dictionary[key_value_pair[0]] = key_value_pair[1].split(
                            VALUE_DELIMITER)
        return dictionary

    except IOError:

        print "cannot open" + name_of_file
        sys.exit()


def write_dictionary(dictionary, name_of_file, file_location=None):
    if file_location is None:
        file_location = FILE_LOCATION

    file_name = os.path.join(file_location, name_of_file)

    try:
        if not os.path.exists(file_location):
            os.mkdir(file_location)

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_filename = temp_file.name
            for key, values in dictionary.iteritems():
                temp_file.write(key + KEY_DELIMITER + values[0])

                for item in values[1:]:
                    temp_file.write(VALUE_DELIMITER + str(item))

                temp_file.write("\n")

        if os.path.exists(file_name):
            os.remove(file_name)

        move(temp_filename, file_name)
        return True

    except IOError:
        rospy.loginfo("cannot open " + name_of_file)
        return False


def append_dictionary_item(key, values, name_of_file, file_location=None):
    if file_location is None:
        file_location = FILE_LOCATION

    file_name = os.path.join(file_location, name_of_file)

    try:
        if not os.path.exists(file_location):
            os.mkdir(file_location)

        with open(file_name, 'a') as fh:
            fh.write(key + KEY_DELIMITER + values[0])

            for item in values[1:]:
                fh.write(VALUE_DELIMITER + str(item))

            fh.write("\n")

        return True

    except IOError:
        rospy.loginfo("cannot open " + name_of_file)
        return False


def search_for_key(key, name_of_file, file_location=None):
    if file_location is None:
        file_location = FILE_LOCATION

    file_name = os.path.join(file_location, name_of_file)

    value = None

    try:
        if os.path.exists(file_name):
            with open(file_name, 'r') as fh:
                for line in fh:
                    if not line.startswith(COMMENT_STRING):
                        key_value_pair = line.strip().split(KEY_DELIMITER)
                        if key_value_pair[0] == key:
                            value = key_value_pair[1].split(VALUE_DELIMITER)
                            break

    except IOError:
        print "cannot open" + name_of_file
        sys.exit()

    return value


def read_data(name_of_file, folder_name=None, file_location=None):

    if file_location is None:
        file_location = FILE_LOCATION
        if folder_name is not None:
            file_location = os.path.join(file_location, folder_name)

    file_name = os.path.join(file_location, name_of_file)

    data = None

    try:
        if os.path.exists(file_name):
            with open(file_name, 'r') as fh:
                data = fh.read().strip()

    except IOError:
        print "cannot open" + name_of_file
        sys.exit()

    return data
