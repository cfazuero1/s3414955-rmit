##Build and Run instructions

###Installation:

1. Install dependencies listed in the REEM/dependencies folder

2. Append `source /path/to/repo/REEM/devel/setup.bash` to ~/.bashrc. Restart terminal session.

3. Perform:

	`git pull origin branch`

	`rm -rf package_name`
 
	`catkin_create_pkg package_name rospy` (or with roscpp)

	`git reset --hard`

	`catkin_make` in the REEM directory

	`rosrun package_name code_name code_name_args` (or roslaunch if contains launch file)

####Sphinxbase for updating pocketsphinx speech recogniser's dictionary and grammar files

1. Install it following this link: http://jrmeyer.github.io/installation/2016/01/09/Installing-CMU-Sphinx-on-Ubuntu.html

2. Go to the location of the dictionary and grammar file (ros_aiml/src)

3. Use command: sphinx_jsgf -jsgf <name.jsgf> -fsg <name.fsg>

###Running AIML on ROS REEM:

1. `roslaunch reem_gazebo reem_empty_world.launch`

2. New terminal `roslaunch pocketsphinx test.launch`

3. New terminal `roslaunch ros_aiml start_speech_chat.launch`
