###Installing Dependencies

To install dependencies here using Python pip use:


`pip install --target=\absolute\path package_name`


Then to appropriately get python recognising the path, add the following to your ~/.bashrc:


`export PYTHONPATH=$PYTHONPATH:\absolute\path`

####Currrently installed dependencies
Dependencies will be ignored from git to prevent bloat, as such you will need to install them manually on each machine.

#####The list of relevant dependencies is currently:

`pyaudio`

`SpeechRecognition`

`pocketsphinx`

`aiml`

`pathlib`

`--upgrade pycurl`

Please update this list if you require additional dependencies

#####Other stuff

Additionally, sphinxbase needs to be installed here if any changes need to be made to the dictionary and grammar file
