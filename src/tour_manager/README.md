In order to convert speech to text, the SpeechRecognition library for python must be installed.
A tutorial for the same can be found at https://pypi.python.org/pypi/SpeechRecognition/

Once it is installed, speech.py script in this package will import this library to convert any speech to text.

Overview of package:

speech.py:
	Node -> speech
	Publish to -> speech_to_text
	Subscribed to -> <None>
	Use -> Convert speech to text and publish the recognised text to "speech_to_text" topic

speak_to_navigate.py:
	Node -> navigation_command_interpreter
	Publish to -> /bosstheturtle, saveLocation
	Subscribed to -> speech_to_text
	Use -> Map text received from "speech_to_text" topic to commands. If command was to save a location, publish location name to "saveLocation" topic.

save_current_location.py:
	Node -> save_current_location
	Publish to -> <None>
	Subscribed to -> /amcl_pose, saveLocation
	Use -> Write REEM's current location with the location name when a name is published on the "saveLocation" topic.

It is also necessary to to run controlled_move.cpp from the motion_tests package inorder to map command to motion in a simulation.
		rosrun motion_tests controlled_move

There is no perticular order of execution. Preferably execute speech.py at last so that when it recognises speech, other nodes are ready.

		rosrun speech speak_to_navigate.py
		rosrun speech save_current_location.py
		rosrun motion_tests controlled_move
		rosrun speech speech.py
