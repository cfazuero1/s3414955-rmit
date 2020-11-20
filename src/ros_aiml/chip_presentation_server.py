#!/usr/bin/env python

import sys
from pathlib import Path
import roslib; roslib.load_manifest('sound_play')
import rospy
import rosnode
import actionlib
import re
import ast
from gesture_sender import GestureSender
from text_to_speech import *

from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from StringIO import StringIO
from ros_aiml.srv import *
from diagnostic_msgs.msg import DiagnosticArray
from pal_interaction_msgs.msg import TtsAction, TtsGoal, TtsFeedback

import os
import struct

_sound_running = None

# Counting the duration of the wave file
# Thanks Rico!
def wave_counter(fhandle):
	path = str(Path(fhandle.name).resolve())
	f = open(path, 'rb')
	# read the ByteRate field from file (see the Microsoft RIFF WAVE file format)
	# https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
	# ByteRate is located at the first 28th byte
	f.seek(28)
	a = f.read(4)
	# convert string a into integer/longint value
	# a is little endian, so proper conversion is required
	byterate = struct.unpack_from("<l", a)
	# get the file size in bytes
	filesize = os.path.getsize(path)
	# the duration of the data, in milliseconds, is given by
	ms = ((filesize - 44) * 1000) / int(byterate[0])
	f.close()
	return ms

#Constructs the wave file and gesture file used in presentations,
#overwriting any files that already exist
def make_wavs(loc_name, level):
	if not rospy.has_param("/speech_root"):
		rospy.loginfo("Error: speech location parameter not set")
		exit(0)
	_root = rospy.get_param("/speech_root")
	_fol = _root+'/'+loc_name+'/'+level+'/'
	files = find_pres_files(loc_name, level)
	if len(files) == 4:
		time_txt = os.path.getmtime(files[1].name)
		time_wav = os.path.getmtime(files[2].name)
		if time_wav > time_txt:
			#rospy.loginfo("Files found and up to date, not generating new wav files!")
			return
	#rospy.loginfo("Files need to be generated!")
	wholetext = open(_fol+'speech.txt', 'r').read()
	wholetext.replace("\n", " ")
	splittext = re.split(r'[{}]', wholetext)
	#if wholetext[0] is a {, then we open wth a gesture. Else, open with speech
	#protip: splitting at the first character puts an empty string at the start of the list. Ditto on the last character
	speeches = []
	gestures = []
	doinggest = False #see comment on split() above
	#for all elements in splittext
	for elem in splittext:
		#move element to its new list
		if doinggest == True:
			gestures.append(elem)
		else:
			speeches.append(elem)
		#toggle control bool
		doinggest = not doinggest

	map(str.strip, gestures)
	allwords = reduce(lambda x, y: x+y, speeches)
	preso = get_watson_file(allwords, _fol+"speech.wav")
	if preso is None: #error generating wavs (probably no internet), bail out!
		rospy.loginfo("Error creating speech.wav, aborting whole process")
		return
	#generate list of gesture timings
	timlist = []
	j=0

	for i in range(len(gestures)):
		filename = _fol + "tmp" + str(i) 
		filehandle = get_watson_file(speeches[i], filename) #if the call above worked, we assume these ones will too.
		timlist.append((gestures[i], wave_counter(filehandle)))
		os.remove(filename)

	with open(_fol+"gests.txt", 'w') as f:
		f.write(str(timlist))

#Checks for all three presentation files: raw text, wave and gestures
#Returns file handles for all three if found, an empty tuple if not
#WARNING: the file handles returned will be closed, because Python
#Should this check the timestamps? Or is that another function's problem?
def find_pres_files(loc_name, level):
	_root = rospy.get_param("/speech_root")
	_fol = _root+'/'+loc_name+'/'+level+'/'
	if not os.path.exists(_fol):
		return ()
	try:
		f0 = open(_fol+"speech.txt", 'r')
	except IOError:
		rospy.loginfo("Speech text file not found for location %s level %s."%(loc_name, level))
		return (_fol)
	else:
		f0.close()
	try:
		f2 = open(_fol+"gests.txt", 'r')
	except IOError:
		rospy.loginfo("Speech wave and gesture files not found for location %s level %s."%(loc_name, level))
		return (_fol, f0)
	else:
		f2.close()
	try:
		f1 = open(_fol+"speech.wav", 'r')
	except IOError:
		rospy.loginfo("Speech wave removed, but the gesture timings are still there. What are you doing to me human?!")
		return (_fol, f0, f2)
	else:
		f1.close()
		return (_fol, f0, f1, f2)

#namespace holder hack, fixed by 'nonlocal' keyword in python 3
class FbHolder: pass
def run_pres(loc_name, level):
	gsender = GestureSender()
	ssender = SoundClient()
	rospy.sleep(1)
	if(loc_name == "secret"):
		play_bonus(ssender, level)
		return
	#how will this whole process deal with no internet? Need to look into the return from Watson if there's no connection
	#make_wavs will abort early if it can't make the files, thus find_pres_files will return None...or just get the old files!
	make_wavs(loc_name, level)
	files = find_pres_files(loc_name, level)
	#need to fork here, based on whether all files are found
	if len(files) == 0: #missing speech: new location with no speech written yet, perhaps
		files = find_pres_files("default", level)
	
	if len(files) == 4:
		#do we start with a gesture? If the first entry of the gestures file has a time of 0.0, yes!
		gestures = []
		with open(files[3].name, 'r') as gfile:
			gestures = ast.literal_eval(gfile.read())

		if len(gestures)>0:
			doinggest = gestures[0][1] == 0.0
		else:
			doinggest = None

		ssender.stopAll()
		gests = len(gestures)
		gestures.reverse()

		if doinggest:
			#print("Firing opening gesture")
			curgest = gestures.pop()
			gsender.send_motion_free(curgest[0])
			gests -= 1
		ssender.playWave(files[2].name)
		#while presentation lists are not empty
		if doinggest is not None:
			while gests > 0:
				curgest = gestures.pop()
				rospy.sleep((curgest[1]/1000)-0.2)#need to account for the sleep in quitIt()
				if gsender.running():
					gsender.quitIt()
				#gsender.send_motion_timeout(gestures.pop(), wavlist.pop()[1]/1000)
				gsender.send_motion_free(curgest[0])
				gests -= 1
	elif len(files) == 3: #script and gesture timings
		with open(files[1].name, 'r') as script:
			speech_srv = actionlib.SimpleActionClient("/tts", TtsAction)

			with open(files[3].name, 'r') as gfile:
				gestures = ast.literal_eval(gfile.read())
			
			wholetext = script.read()
			splittext = re.split(r'[{}]', wholetext)
			doinggest = 1

			for i in range(1, -1, 2):
				if(doinggest<len(gestures)):
					mstime = int(gestures[i][1] * 1000)
				else:
					mstime = 0
				gesttag = "<mark name=\"doTrick trickName="+splittext[i]+" checkSafety=0\"/><break time'\""+str(mstime)+"\">"
				splittext[i] = gesttag

			speechgoal = TtsGoal()
			speechgoal.rawtext.lang_id = "en_US"
			speechgoal.rawtext.text = reduce(lambda x, y: x+y , splittext)
			speech_srv.wait_for_server()
			speech_srv.send_goal(goal)

	elif len(files) == 2:
		with open(files[1].name, 'r') as script:

			#translate gesture tags in {} into <mark name="doTrick trickName=gesture checkSafety=0"/><break time="???"/>
#<mark name="doTrick trickName=wave checkSafety=0"/> <break time="300ms"/> hello, my name is CHIP
			speech_srv = actionlib.SimpleActionClient("/tts", TtsAction)

			wholetext = script.read()
			splittext = re.split(r'[{}]', wholetext)
			doinggest = False

			for i in range(1, -1, 2):
				gesttag = "<mark name=\"doTrick trickName="+splittext[i]+" checkSafety=0\"/>"
				splittext[i] = gesttag

			speechgoal = TtsGoal()
			speechgoal.rawtext.lang_id = "en_US"
			speechgoal.rawtext.text = reduce(lambda x, y: x+y , splittext)
			speech_srv.wait_for_server()
			speech_srv.send_goal(goal)

	elif len(files) == 0:
		#nothing found!
		rospy.loginfo("No speech found for that location/level combination.")
		return
	else:
		#unknown combination; define some error maybe
		#play_bonus(ssender, "cantdo")
		return

	#print("Gestures complete, is the sound still going? %s"%(str(_sound_running)))
	while _sound_running:
		rospy.sleep(0.2)
		pass
		#rospy.loginfo(str(_sound_running))

def pres_handle(req):
	run_pres(req.loc_name, req.level)
	rospy.loginfo("Presentation %s/%s finished execution."%(req.loc_name, req.level))
	return PresentationResponse(True)

def make_handle(req):
	make_wavs(req.loc_name, req.level)
	return PresentationResponse(True)

#do I want to implement a service to change the speech root? There's no std_msgs/String equivalent service =/

def sound_status(data):
	for submsg in data.status:
		if submsg.name == "sound_play: Node State":
			#print("Message on sound found, number of running sounds (field %s) = %d"%(submsg.values[0].key, int(submsg.values[0].value)))
			if len(submsg.values) > 0:
				global _sound_running
				_sound_running = (int(submsg.values[0].value) > 0)

def play_bonus(sender, sound):
	_fol = rospy.get_param("/speech_root")+"/.extra/"
	if os.path.exists(_fol+sound+".wav"):
		sender.playWave(_fol+sound+".wav")
	elif os.path.exists(_fol+sound+".mp3"):
		sender.playWave(_fol+sound+".mp3")
	else:
		pass

if __name__ == "__main__":
	rospy.init_node("presentation")
	if not rospy.has_param("/speech_root"):
		rospy.set_param("/speech_root", os.path.dirname(os.path.realpath(__file__))+"/speeches")
	makesrv = rospy.Service("make_presentation_waves", Presentation, make_handle)
	runsrv = rospy.Service("do_presentation", Presentation, pres_handle)
	soundstatus = rospy.Subscriber("diagnostics", DiagnosticArray, sound_status)
	#wait for sound service to be operational (take 1)
	#while _sound_running is None:
	#	pass
	#	rospy.
	#Need to spin to fire the subscriber callback, but python doesn't have spinOnce(). Because it's a bad language
	#take 2
#	while not rosnode.rosnode_ping("sound_play", 1, False):
#		rospy.sleep(1)
#		pass
	rospy.loginfo("Presentation server running")
	rospy.spin()
