#include "ros/ros.h"
#include "actionlib/client/simple_action_client.h"
#include "actionlib/client/terminal_state.h"
#include "move_base_msgs/MoveBaseAction.h"
#include "move_base_msgs/MoveBaseGoal.h"

#include <istream>

int numpoints = 2;

int main(int argc, char** argv){
	ros::init(argc, argv, "patrol_client");

	actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> cli("move_base", true);

	cli.waitForServer();
	ROS_INFO("Server found, running...");

	float points_[2][2][4] = {
		{{1.0, 2.0, 0.0, 0.0}, {0.0,0.0,0.0,1.0}},
		{{2.0, 1.0, 0.0,0.0}, {0.0,0.0,-1.0,0.0}}
	};
	//Future improvement: use cli goal input, or read coordinates from a file

	//ifstream::open
	//figure out how big points array needs to be and allocate it (number of lines? points/8?)
	//use madcore file parsing to dump floats into array
	//close file

	move_base_msgs::MoveBaseGoal mbg;
	mbg.target_pose.header.frame_id = "map";
	
	int pointupto = 0;
	bool goalres;
	while(ros::ok()){
		mbg.target_pose.pose.position.x = points_[pointupto][0][0];
		mbg.target_pose.pose.position.y = points_[pointupto][0][1];
		mbg.target_pose.pose.position.z = points_[pointupto][0][2];
		mbg.target_pose.pose.orientation.x = points_[pointupto][1][0];
		mbg.target_pose.pose.orientation.y = points_[pointupto][1][1];
		mbg.target_pose.pose.orientation.z = points_[pointupto][1][2];
		mbg.target_pose.pose.orientation.w = points_[pointupto][1][3];
		cli.sendGoal(mbg);
		goalres = cli.waitForResult(ros::Duration(30.0));
		if(goalres){
			pointupto = (pointupto + 1) % numpoints;
			ROS_INFO("Switching to goal %i", pointupto);
		}else{
			ROS_INFO("This goal is taking a long time, resending...");
		}
	}
	return 0;
}
