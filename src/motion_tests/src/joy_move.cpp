#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"

#include <sstream>
#include <cstring>
#include <cmath>

float traveldir = 0.0;
float travelspeed = 0.0;

void commandCallback(const geometry_msgs::Twist& msg){
	float x = msg.angular.z;
	float y = msg.linear.x;
	traveldir = 3.0 * (x / sqrt(1.0-(pow(y, 2)/2.0)));
	travelspeed = 3.0 * (y / sqrt(1.0-(pow(x, 2)/2.0)));
}

int main(int argc, char **argv){
	ros::init(argc, argv, "joystick_motion");
	ros::NodeHandle n;

	/**
	* The advertise() function is how you tell ROS that you want to
	* publish on a given topic name. This invokes a call to the ROS
	* master node, which keeps a registry of who is publishing and who
	* is subscribing. After this advertise() call is made, the master
	* node will notify anyone who is trying to subscribe to this topic name,
	* and they will in turn negotiate a peer-to-peer connection with this
	* node.  advertise() returns a Publisher object which allows you to
	* publish messages on that topic through a call to publish().  Once
	* all copies of the returned Publisher object are destroyed, the topic
	* will be automatically unadvertised.
	*
	* The second parameter to advertise() is the size of the message queue
	* used for publishing messages.  If messages are published more quickly
	* than we can send them, the number here specifies how many messages to
	* buffer up before throwing some away.
	*/
	int count = 0;

	ros::Publisher turtlego = n.advertise<geometry_msgs::Twist>("mobile_base_controller/cmd_vel", 100); //I really hope this works...
	ros::Subscriber joyin = n.subscribe("input_joy/cmd_vel", 1000, commandCallback);

	ros::Rate loop_rate(3);

	//ros::spin(); //throw the program into a loop which fires listener callbacks, cancelled by ctrl+c
	while(ros::ok()){
		ros::spinOnce(); 
		geometry_msgs::Twist vecout;
		vecout.linear.x=travelspeed;
		vecout.angular.z=traveldir;
		std_msgs::String jib;
		std::stringstream ss;
		ss << "msg " << count++ << ", vel " << travelspeed << ", dir " << traveldir;
		jib.data = ss.str();

		ROS_INFO("%s", jib.data.c_str());

		//publish movement
		turtlego.publish(vecout);

		loop_rate.sleep();
	}

	return 0;
}
