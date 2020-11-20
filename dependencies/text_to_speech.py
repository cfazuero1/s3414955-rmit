#!/usr/bin/env python
import sys
import pycurl
import urllib 
from StringIO import StringIO

def get_watson_file(text, outname):
	url = "https://stream.watsonplatform.net/text-to-speech/api/v1/synthesize?voice=en-US_AllisonVoice" 
	user = "7307c2ab-a19f-4bc1-a793-b00ce1b72b66" 
	password = "I5T5cYHyZNeE" 
	msg = text.strip()
	storage = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, url)
	c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: audio/wav'])
	c.setopt(pycurl.USERNAME, user)
	c.setopt(pycurl.PASSWORD, password)
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, '{ "text" : "'+msg+'" }')
	c.setopt(c.WRITEFUNCTION, storage.write)
	try:
		c.perform()
	except pycurl.error:
		print("Failed to get network resource, no connection.")
		return
	#check also for other network problems, like a 404 code?
	c.close()
	content = storage.getvalue()
	
	with open(outname, 'w') as f:
		f.write(content)
	return f

if __name__ == "__main__":
	f = open(sys.argv[1], 'r')
	get_watson_file(f.readline(), f.name.rstrip(".txt")+".wav")
