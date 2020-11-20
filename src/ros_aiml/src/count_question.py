# Author: Cristhian Azuero
# Date: 11-10-2016

#!/usr/bin/env python
import sys

def text2int(textnum, numwords={}):
  #current = int(textnum)
  current = 0
  result = 0
  if not textnum.isdigit():
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
  else:
      current = int(textnum)
  return result + current

num = sys.argv[1]
count=text2int(num)

fp = open('questions', 'r')
for i, line in enumerate(fp):
    if i == count:
       print line.strip()

fp.close()
