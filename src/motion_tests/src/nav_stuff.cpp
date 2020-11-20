#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"
#include "tf/transform_listener.h"

#include <sstream>
#include <iostream>
#include <fstream>
#include <cstring>


int main(int argc, char **argv){
	ros::init(argc, argv, "navstuff");
	ros::NodeHandle n;

	int count = 0;

	std::ofstream fileout;
	fileout.open("test.txt");

	//std::string source_frame = std::string(argv[1]);
	//std::string target_frame = std::string(argv[2]);
	std::string source_frame = "/map";
	std::string target_frame = "/base_link";

	tf::TransformListener tranlist;
	tranlist.waitForTransform(source_frame, target_frame, ros::Time(), ros::Duration(1.0));
	tf::StampedTransform echo_transform;

	ros::Rate loop_rate(3);

	//ros::spin(); //throw the program into a loop which fires listener callbacks, cancelled by ctrl+c
	while(ros::ok()){
		try{
			tranlist.lookupTransform(source_frame, target_frame, ros::Time(), echo_transform);
			tf::Quaternion rot = echo_transform.getRotation();
			tf::Vector3 pos = echo_transform.getOrigin();
			fileout << echo_transform.stamp_.toSec()
				<< "\t[" << pos.getX() << "," << pos.getY() << "," << pos.getZ()
				<< "]\t[" << rot.getX() << "," << rot.getY() << "," << rot.getZ() << "," << rot.getW() << "]" << std::endl;
		}catch(tf::TransformException& ex){
			std::cout << "Failure at " << ros::Time::now() << std::endl;
			std::cout << "Exception thrown:" << ex.what() << std::endl;
			std::cout << "The current list of frames is:" << std::endl;
			std::cout << tranlist.allFramesAsString() << std::endl;
		}
		loop_rate.sleep();
	}
	fileout.close();
	return 0;
}
