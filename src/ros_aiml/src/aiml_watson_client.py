# Author: Cristhian Azuero
# Date: 11-10-2016

#!/usr/bin/env python
import rospy, os, sys
import time
import struct
import pycurl
from StringIO import StringIO
import roslib
import play_sound

roslib.load_manifest('sound_play')
from sound_play.libsoundplay import SoundClient
from tour_manager.srv import *


class WatsonClient:
    def __init__(self):
        rospy.init_node('aiml_soundplay_client', anonymous=True)
        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()
        print 'Starting TTS'

        self.SOUND_FILE_PATH = "/opt/ros/hydro/share/sound_play/sounds"

        rospy.Service("aiml_to_watson", speech, self.get_response)
        rospy.loginfo("Starting listening to response")
        rospy.spin()

    # Call back method to receive text from /response topic and convert to speech
    def get_response(self, req):
        response = req.data
        rospy.loginfo("Response ::%s", response)
        # soundhandle.say(response)
        # self.watson(response)
        play_sound.speak_text(response)
        # self.more_question()

    # Method to create a subscriber for /response topic.
    # def listener():
    # 	rospy.loginfo("Starting listening to response")
    # 	rospy.Subscriber("response", String, get_response, queue_size=10)
    # 	rospy.spin()

    # This call a text-to-speech voice from watson
    def watson(self, data):
        # stop_recognizer()
        temp_file_name = "voice.wav"

        url = "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?voice=en-US_AllisonVoice"
        user = "7307c2ab-a19f-4bc1-a793-b00ce1b72b66"
        password = "I5T5cYHyZNeE"
        msg = data.strip()
        storage = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(pycurl.HTTPHEADER,
                 ['Content-Type: application/json', 'Accept: audio/wav'])
        c.setopt(pycurl.USERNAME, user)
        c.setopt(pycurl.PASSWORD, password)
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, '{ "text" : "' + msg + '" }')
        c.setopt(c.WRITEFUNCTION, storage.write)
        c.perform()
        c.close()
        content = storage.getvalue()

        with open(os.path.join(self.SOUND_FILE_PATH, temp_file_name), 'w') as f:
            f.write(content)

        sound_client = SoundClient()
        sound = sound_client.waveSound(temp_file_name)
        sound.play()
        self.wave_counter(temp_file_name)

        os.remove(os.path.join(self.SOUND_FILE_PATH, temp_file_name))

    # Counting the duration of the wave file
    def wave_counter(self, file_name):
        file_path = os.path.join(self.SOUND_FILE_PATH, file_name)

        f = open(file_path, 'rb')
        # read the ByteRate field from file (see the Microsoft RIFF WAVE file format)
        # https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
        # ByteRate is located at the first 28th byte
        f.seek(28)
        a = f.read(4)
        # convert string a into integer/longint value
        # a is little endian, so proper conversion is required
        if len(a) == 4:
            byterate = struct.unpack_from("<l", a)

            # get the file size in bytes
            filesize = os.path.getsize(file_path)

            # the duration of the data, in milliseconds, is given by
            ms = ((filesize - 44) * 1000) / int(byterate[0])
            time.sleep((ms / 1000) + 1)
        f.close()


if __name__ == '__main__':
    WatsonClient()
