# Author: Cristhian Azuero
# Date: 11-10-2016

#!/usr/bin/env python
import sys

count = 1
f = open('questions', 'r')
for line in f:
    print str(count) + ". " + line,
    count += 1
f.close()
print "Please select a question"
