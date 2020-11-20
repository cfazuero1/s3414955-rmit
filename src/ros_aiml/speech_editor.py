#!/usr/bin/env python
import sys
from pathlib import Path
import rospy
import re
from text_to_speech import *
from StringIO import StringIO
import os
import struct
from presentation_server import make_wavs

#args: exhibit, level, [location of txt file]
#if txt file given, read txt file
#else read from stdin
if len(sys.argv) == 4:
	try:
		with open(sys.argv[3], 'r') as f:
			wholetext = f.read()
	except IOError:
		print "Please give a valid path to a file!"
		exit(0)
elif len(sys.argv) == 3:
	print "Type the text for the speech (remember gestures are surrounded by { and }). <Enter> to finish writing."
	wholetext = sys.stdin.readline()
else:
	print "Usage: speech_editor.py <location> <level> [<file>]"
	exit(0)

#dump into location+level speech.txt
	#make folders if they aren't there
if not rospy.has_param("/speech_root"):
	_root = rospy.get_param("/speech_root")
else:
	_root = os.path.dirname(os.path.realpath(__file__))+"/speeches"
_fol = _root+"/"
loc_name = sys.argv[1]
level = sys.argv[2]
print "Debug: writing folders/files to " + _fol
if not os.path.exists(_fol+loc_name):
	os.mkdir(_fol+loc_name)
	os.mkdir(_fol+loc_name+"/bas")
	os.mkdir(_fol+loc_name+"/int")
	os.mkdir(_fol+loc_name+"/adv")
_fol += loc_name+"/"
if not os.path.exists(_fol+level):
	os.mkdir(_fol+level)
_fol += level+"/"
print "Now writing to: " + _fol

if os.path.exists(_fol+"speech.txt"):
	print "This presentation already exists. Are you sure you want to overwrite? <yes/no>"
	res = sys.stdin.readline()
	if re.match(r'[nN]o?.*', res):
		print "Aborting."
		exit(0)
with open(_fol+"speech.txt", 'w') as f:
#	if(f.readline() != ""):
	f.write(wholetext)
	
#generate extra files: speech.wav, gests.txt (and gests_off.txt?)
make_wavs(loc_name, level)

