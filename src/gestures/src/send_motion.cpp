#include <ros/ros.h>
#include "gesture_sender.h"

int main(int argc, char** argv){
	ros::init(argc, argv, "gesture_tester");
	//super simple; read args, make a GestureSender and send a gesture
	//Make sure to test send_motion and send_motion_free
	GestureSender sendo;
ROS_INFO("Regular sending motion: arms_t");
	sendo.send_motion("arms_t");
ROS_INFO("Sending motion with timeout: strong_arms");
	sendo.send_motion_timeout("strong_arms", 5.0);
ROS_INFO("Free motion sent: aok");
	sendo.send_motion_free("aok");
	sleep(6);
ROS_INFO("Sending motion then cancelling: rewind");
	sendo.send_motion_free("rewind");
	sleep(1);
	sendo.quitIt();
//note to self: consider randomizing poses and timeout time for these tests, rosservice call /play_motion/list (or something like that) tells us the pose names
ROS_INFO("Test complete.");
	return 0;
}
