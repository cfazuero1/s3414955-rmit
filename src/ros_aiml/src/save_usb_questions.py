# Author: Cristhian Azuero
# Date: 11-10-2016

#!/usr/bin/env python

import os

dirlist = os.listdir("/media")
print(dirlist[0])

f = open('questions', 'r')
lines = f.readlines()
f.close()
f = open('/media/'+dirlist[0]+'/default.qtns', 'w')
for elem in lines:
    f.write("question: "+elem.strip()+" \n")
    f.write("answer: "+"\n")
f.close()
print "All the question are in your USB..."
