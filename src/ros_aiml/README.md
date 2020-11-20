#AIML

##To run this package you need to install pyaiml:

apt-get install python-aiml

##You also need to modify lines 2 of the launch/*.launch files to have the absolute path to the ros_aiml/src folder

###If you want to run the chatbot with festival

roslaunch ros_aiml start_tts_chat.launch

###If you want to run the chatbot with text

roslaunch ros_aiml start_chat.launch

###If you want to run the chatbot with watson and having a sexy voice

roslaunch ros_aiml start_watson_chat.launch

###If you want to run the chatbot with gstreamer

roslaunch ros_aiml start_gstreamer_chat.launch

###If you want to run the speech to text tour demo

roslaunch ros_aiml start_speech_chat.launch

roslaunch ros_aiml test.launch

####Speech chat available at the moment

1. Who is ian peake?

2. What is the vxlab?

3. What kind of project are in the vxlab 

####Speech command available at the moment

1. Okay Chip execute tour [number_from_0-9/alphabet] in [basic/intermediate/advanced] mode

2. Okay Chip go to location [number_from_0-9/alphabet]

3. Okay Chip add location [number_from_0-9/alphabet] to tour [number_from_0-9/alphabet]

4. Okay Chip save this location as [number_from_0-9/alphabet]
