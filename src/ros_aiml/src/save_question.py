# Author: Cristhian Azuero
# Date: 11-10-2016

#!/usr/bin/env python
import sys

#content = ' '.join(sys.argv[1:])
content = sys.argv[1]
f = open('questions', 'a')
f.write(content+"." + "\n")
f.close()
