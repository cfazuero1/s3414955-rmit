# Author: Cristhian Azuero
# Date: 11-10-2016

#!/usr/bin/env python

import os

path = ""
for root, dirs, files in os.walk("/media"):
    for file in files:
        if file.endswith(".qtns"):
             print(os.path.join(root, file))
             path = os.path.join(root, file)

f = open('alice/test.aiml', 'r')
lines = f.readlines()
f.close()
f = open('alice/test.aiml', 'w')
f.writelines([item for item in lines[:-1]])
f.close()

f = open(path, 'r')
fp = open('alice/test.aiml', 'a')
question = ""
answer = ""
for line in f:
     if len(line.split("question:")) == 2:
       question = line.split("question:")[1].strip()
     if len(line.split("answer:")) == 2:
       answer = line.split("answer:")[1].strip()
       if len(answer) > 0:
          print question
          print answer
	  fp.write("<category>" + "\n")
	  fp.write("<pattern>"+question.upper()+"</pattern>" + "\n")
	  fp.write("<template>"+answer+"</template>" + "\n")
	  fp.write("</category>" + "\n")
fp.write("</aiml>" + "\n")
fp.close()
f.close()
os.remove("standard.brn")
print "please reboot the app, record have been saved successfully!!!"

